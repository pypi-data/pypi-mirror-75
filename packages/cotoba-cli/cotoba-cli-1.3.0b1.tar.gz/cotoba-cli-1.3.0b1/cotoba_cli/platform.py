import base64
import boto3
import json
import requests
import logging
import os
import re
import pytz
import sys
import click
import http.client

from datetime import datetime
from pytz import timezone

from botocore import exceptions as boto_exceptions
from urllib.parse import urljoin

from cotoba_cli import config
from cotoba_cli import cognito

logger = logging.getLogger(__name__)
client = boto3.client('cognito-idp',
                      region_name=cognito.USER_POOL_REGION,
                      aws_access_key_id=cognito.ACCESS_KEY,
                      aws_secret_access_key=cognito.SECRET_KEY,
                      )

BOT_API_PATH = 'bots/'


class LoginIdNotFoundException(Exception):
    def __init__(self, login_id):
        self.login_id = login_id
        super().__init__(
            'Account with id({}) is not found.'.format(login_id))


class PlatformResponse:
    def __init__(self,
                 response_body_json,
                 http_status_code,
                 message_text,
                 request_body=None,
                 response_headers=None):
        self.__response_body_json = response_body_json
        self.__http_status_code = http_status_code
        self.__message_text = message_text
        self.__response_headers = response_headers
        self.__request_body = request_body

    def get_response_body(self):
        return json.loads(self.__response_body_json)

    @property
    def message(self):
        return self.__message_text

    @message.setter
    def message(self, message):
        self.__message_text = message

    def print_message(self, output_headers):
        if not (self.__message_text or output_headers):
            return
        if output_headers:
            try:
                body = json.loads(self.__message_text)
            except json.decoder.JSONDecodeError:
                body = self.__message_text
            response = {
                'headers': dict(self.__response_headers),
                'body': body
            }
            click.echo(json.dumps(response))
        else:
            click.echo(self.__message_text)

    def print(self, print_status=True, output_headers=False):
        if print_status:
            if 400 <= self.__http_status_code:
                color = 'red'
            else:
                color = 'green'
            status_msg = http.client.responses[self.__http_status_code]
            status_text = str(self.__http_status_code) + ' ' + status_msg
            click.echo(click.style(
                status_text,
                fg=color),
                err=True
            )
        self.print_message(output_headers)

    def get_request_time(self):
        return self.__request_body.get('time')

    @staticmethod
    def build_from_requests_result(result, message=None, request_body=None):
        message = message if message is not None else result.text
        return PlatformResponse(result.text,
                                result.status_code,
                                message,
                                request_body=request_body,
                                response_headers=result.headers)


def login(login_id, password, authorization=None):
    if not authorization:
        authorization = config.load()['default'].get('authorization')
        if not authorization:
            click.echo('Set authorization Id.', err=True)
            sys.exit(1)
    pool_id, client_id = decode_cognito_setting(authorization)

    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': login_id,
                'PASSWORD': password
            },
            ClientId=client_id
        )
    except client.exceptions.NotAuthorizedException:
        click.echo('Incorrect password.', err=True)
        sys.exit(1)
    except boto_exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            login_error = LoginIdNotFoundException(login_id)
            click.echo(str(login_error), err=True)
            sys.exit(1)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            click.echo(str(e.response['Error']['Message']), err=True)
            logger.error(e, exc_info=True)
            sys.exit(1)
        # TODO: Add error for expired refresh token.
        else:
            raise e

    return response


def change_password(old_password, new_password, access_token):
    try:
        client.change_password(
            PreviousPassword=old_password,
            ProposedPassword=new_password,
            AccessToken=access_token
        )
    except boto_exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidPasswordException':
            show_invalid_password_message_and_exit(e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            click.echo(str(e.response['Error']['Message']), err=True)
            logger.error(e, exc_info=True)
            sys.exit(1)
        elif e.response['Error']['Code'] == 'LimitExceededException':
            click.echo(str(e.response['Error']['Message']), err=True)
            logger.error(e, exc_info=True)
            sys.exit(1)
        else:
            raise e
    except boto_exceptions.ParamValidationError as e:
        click.echo(str(e), err=True)
        logger.error(e, exc_info=True)
        sys.exit(1)


def create_bot(auth,
               filepath,
               endpoint_url,
               name=None,
               message=None,
               nlu_url=None,
               nlu_api_key=None):
    if not os.path.exists(filepath) or os.path.isdir(filepath):
        click.echo(f'File {filepath} not found.', err=True)
        logger.info(f'File {filepath} not found.')
        sys.exit(1)
    with open(filepath, 'rb') as f:
        encoded_file = base64.b64encode(f.read()).decode('utf-8')
    headers = {
        'Authorization': auth.id_token,
        'Content-Type': 'application/json; charset=utf-8'
    }
    body = {
        'file': encoded_file,
        'name': name,
        'message': message,
        'nluUrl': nlu_url,
        'nluApiKey': nlu_api_key
        }
    body = {k: v for k, v in body.items() if v is not None}
    try:
        r = requests.post(
            urljoin(endpoint_url, BOT_API_PATH),
            json.dumps(body),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def update_bot(auth,
               bot_id,
               endpoint_url,
               filepath=None,
               name=None,
               message=None,
               nlu_url=None,
               nlu_api_key=None):
    headers = {
        'Authorization': auth.id_token,
        'Content-Type': 'application/json; charset=utf-8'
    }

    body = {
        'name': name,
        'message': message,
        'nluUrl': nlu_url,
        'nluApiKey': nlu_api_key
    }

    if filepath:
        if not os.path.exists(filepath) or os.path.isdir(filepath):
            click.echo(f'File {filepath} not found.', err=True)
            logger.info(f'File {filepath} not found.')
            sys.exit(1)
        with open(filepath, 'rb') as f:
            body['file'] = base64.b64encode(
                f.read()).decode('utf-8')

    body = {k: v for k, v in body.items() if v is not None}

    try:
        r = requests.put(
            urljoin(endpoint_url, BOT_API_PATH + bot_id),
            json.dumps(body),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def list_bots(auth, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }
    try:
        r = requests.get(
            urljoin(endpoint_url, BOT_API_PATH),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def get_bot(auth, bot_id, zipfile_path, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }
    api_path = urljoin(endpoint_url, BOT_API_PATH + bot_id)
    if zipfile_path:
        api_path = api_path + '?include_scenario=true'
    try:
        r = requests.get(api_path, headers=headers)
        res = PlatformResponse.build_from_requests_result(r)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    if zipfile_path:
        with open(zipfile_path, 'wb') as f:
            f.write(base64.b64decode(res.get_response_body()['file']))
    return res


def delete_bot(auth, bot_id, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }
    try:
        r = requests.delete(
            urljoin(endpoint_url,  BOT_API_PATH + bot_id),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def ask_bot(
        bot_id,
        api_key,
        user_id,
        utterance,
        topic=None,
        metadata=None,
        log_level=None,
        locale=None,
        endpoint_url=None,
        exit_on_error=True,
):
    """
    Returns:
      (decode_response_text, unicode_response_text, request_time)
    """
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-api-key': api_key
    }
    request_time = get_local_time(locale)
    payload = {
        "locale": locale,
        "time": request_time,
        "userId": user_id,
        "utterance": utterance,
    }
    if log_level is not None:
        payload['config'] = {"logLevel": log_level}
    if topic is not None:
        payload['topic'] = topic
    if metadata is not None:
        payload['metadata'] = metadata
    try:
        r = requests.post(
            urljoin(endpoint_url, BOT_API_PATH + bot_id + '/ask'),
            data=json.dumps(payload),
            headers=headers
        )
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    if exit_on_error:
        show_message_and_exit_on_error(r)

    return PlatformResponse.build_from_requests_result(
        r,
        request_body=payload)


def debug_bot(auth, bot_id, api_key, endpoint_url, user_id=None):
    headers = {
        'Authorization': auth.id_token,
        'x-api-key': api_key
    }

    if user_id is None:
        user_id = "None"

    try:
        r = requests.post(
            urljoin(endpoint_url,  BOT_API_PATH + bot_id + '/debug'),
            json.dumps({
                'userId': user_id
            }),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def create_api_key(auth,
                   bot_id,
                   expiration_days,
                   max_api_calls,
                   description,
                   endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }

    request_body = {
        'expirationDays': expiration_days,
        'maxApiCalls': max_api_calls,
        'description': description,
    }

    try:
        r = requests.post(
            urljoin(endpoint_url,  BOT_API_PATH + bot_id + '/api-keys'),
            json.dumps(request_body),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def list_api_keys(auth, bot_id, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }

    try:
        r = requests.get(
            urljoin(endpoint_url,  BOT_API_PATH + bot_id + '/api-keys'),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def get_api_key(auth, bot_id, api_key, endpoint_url):
    headers = {
        'Authorization': auth.id_token,
    }

    try:
        r = requests.get(
            urljoin(
                endpoint_url,
                BOT_API_PATH + bot_id + '/api-keys/' + api_key
            ),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def update_api_key(auth,
                   bot_id,
                   api_key,
                   expiration_days,
                   max_api_calls,
                   description,
                   endpoint_url):
    headers = {
        'Authorization': auth.id_token,
    }

    request_body = {}
    if not expiration_days:
        pass
    elif isinstance(expiration_days, str) and \
            expiration_days.upper() == 'NONE':
        request_body['expirationDays'] = None
    else:
        try:
            request_body['expirationDays'] = int(expiration_days)
        except ValueError:
            sys.stderr.write('--expiration-days must be number or None.\n')
            sys.exit(1)

    if not max_api_calls:
        pass
    elif isinstance(max_api_calls, str) and \
            max_api_calls.upper() == 'NONE':
        request_body['maxApiCalls'] = None
    else:
        try:
            request_body['maxApiCalls'] = int(max_api_calls)
        except ValueError:
            sys.stderr.write('--max-api-calls must be number or None.\n')
            sys.exit(1)
    if description is not None:
        request_body['description'] = description

    try:
        r = requests.put(
            urljoin(
                endpoint_url,
                BOT_API_PATH + bot_id + '/api-keys/' + api_key
            ),
            json.dumps(request_body),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def delete_api_key(auth, bot_id, api_key, endpoint_url):
    headers = {
        'Authorization': auth.id_token,
        'x-api-key': api_key
    }

    try:
        r = requests.delete(
            urljoin(
                endpoint_url,
                BOT_API_PATH + bot_id + '/api-keys/' + api_key
            ),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def run_bot(auth, bot_id, update, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }
    api_path = urljoin(endpoint_url, BOT_API_PATH + bot_id + '/run')
    if update:
        api_path = api_path + '?update=true'
    try:
        r = requests.post(
            api_path,
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def stop_bot(auth, bot_id, endpoint_url):
    headers = {
        'Authorization': auth.id_token
    }
    try:
        r = requests.post(
            urljoin(endpoint_url, BOT_API_PATH + bot_id + '/stop'),
            headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def encode_cognito_setting(pool_id, client):
    connected_text = ','.join([pool_id, client])
    encoded_text = base64.encodebytes(connected_text.encode('ascii'))
    return encoded_text


def decode_cognito_setting(encoded_cognito_setting):
    """
    Returns:
      (pool_id, client_id)
    """
    if type(encoded_cognito_setting) is str:
        encoded_cognito_setting = encoded_cognito_setting.encode('ascii')
    try:
        decoded_text = base64.decodebytes(
            encoded_cognito_setting).decode('ascii')
    except base64.binascii.Error as e:
        click.echo('Authorization Id is invalid.', err=True)
        logger.error(e, exc_info=True)
        sys.exit(1)
    if decoded_text.count(',') != 1:
        click.echo(f'Authorization ID: {decoded_text} does not have comma.',
                   err=True)
        logger.error(f'Authorization ID: {decoded_text} does not have comma.')
        sys.exit(1)
    return tuple(decoded_text.strip().split(','))


def get_local_time(locale):
    result = re.match('(?P<lang>.*)[_|-](?P<code>.*)', locale)
    country_code = result.group('code')
    tz_dict = pytz.country_timezones
    tz = tz_dict.get(country_code)
    return datetime.now(timezone(tz[0])).isoformat(timespec='seconds')


def handle_requests_exception_and_exit(e):
    click.echo('Error while connecting server.'
               ' See the cotoba-cli.log in detail.', err=True)
    logger.error(e, exc_info=True)
    sys.exit(1)


def show_invalid_password_message_and_exit(e):
    """
    For example, e.response['Error']['Message'] is
    "Password did not conform with policy: Password not long enough"
    We only use the last message ("Password not long enough"),
    so we use regular expressions.
    """
    error_message_all = str(e.response['Error']['Message'])
    result = re.match('(.*: )(?P<message>.*$)', error_message_all)
    if result is not None:
        click.echo(result.group('message'), err=True)
    else:
        click.echo('Invalid Password.', err=True)
    sys.exit(1)


def get_bot_logs(auth, endpoint_url,
                 start_date=None,
                 end_date=None,
                 limit=None,
                 offset=None,
                 bot_id=None,
                 api_key_id=None,
                 ):
    headers = {
        'Authorization': auth.id_token
    }
    params = {'start': start_date, 'end': end_date,
              'limit': limit, 'offset': offset,
              'bot_id': bot_id, 'api_key_id': api_key_id}
    try:
        r = requests.get(
            urljoin(endpoint_url, BOT_API_PATH + 'logs/dialogues'),
            params=params, headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def get_bot_traffics(auth, endpoint_url,
                     aggregation,
                     start_date=None,
                     end_date=None,
                     bot_id=None,
                     api_key_id=None,
                     ):
    headers = {
        'Authorization': auth.id_token
    }
    params = {'aggregation': aggregation,
              'start': start_date, 'end': end_date,
              'bot_id': bot_id, 'api_key_id': api_key_id}
    try:
        r = requests.get(
            urljoin(endpoint_url, BOT_API_PATH + 'logs/traffics'),
            params=params, headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)


def show_message_and_exit_on_error(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        click.secho(f'{e}', fg='red', err=True)
        click.secho(response.text, fg='red')
        sys.exit(1)


def get_bot_topics(auth, endpoint_url,
                   aggregation,
                   start_date=None,
                   end_date=None,
                   bot_id=None,
                   api_key_id=None,
                   ):
    headers = {
        'Authorization': auth.id_token
    }
    params = {'aggregation': aggregation,
              'start': start_date, 'end': end_date,
              'bot_id': bot_id, 'api_key_id': api_key_id}
    try:
        r = requests.get(
            urljoin(endpoint_url, BOT_API_PATH + 'logs/topics'),
            params=params, headers=headers)
    except requests.RequestException as e:
        handle_requests_exception_and_exit(e)
    return PlatformResponse.build_from_requests_result(r)
