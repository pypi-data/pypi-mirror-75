import sys

import boto3
import click
import logging

from cotoba_cli import session
from cotoba_cli import config
from cotoba_cli import platform
from datetime import datetime
from jose import jwt

ACCESS_KEY = 'dummy'
SECRET_KEY = 'dummy'
USER_POOL_REGION = 'ap-northeast-1'

logger = logging.getLogger(__name__)
client = boto3.client('cognito-idp',
                      region_name=USER_POOL_REGION,
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY, )


class Authorization:
    def __init__(self, id_token, access_token, refresh_token, sub, client_id):
        self.id_token = id_token
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.sub = sub
        self.client_id = client_id

    def renew_token_if_expired(self):
        if not self.access_token:
            click.echo("You are not logged in."
                       " Run 'cotoba login' to login.", err=True)
            sys.exit(1)
        now = datetime.now()
        decoded_access_token = jwt.get_unverified_claims(self.access_token)

        if now > datetime.fromtimestamp(decoded_access_token['exp']):
            self.renew_access_token_using_refresh_token()
            decoded_access_token = jwt.get_unverified_claims(self.access_token)
        self.sub = decoded_access_token['sub']

    def renew_access_token_using_refresh_token(self):
        response = client.initiate_auth(
            AuthFlow='REFRESH_TOKEN',
            AuthParameters={
                'REFRESH_TOKEN': self.refresh_token,
            },
            ClientId=self.client_id
        )
        self.id_token = response['AuthenticationResult']['IdToken']
        self.access_token = response['AuthenticationResult']['AccessToken']


def get_cognito_authorization():
    session_dict = session.load()['default']
    if 'id_token' not in session_dict \
       or 'refresh_token' not in session_dict \
       or 'access_token' not in session_dict:
        click.echo("You are not logged in."
                   " Run 'cotoba login' to login.", err=True)
        sys.exit(1)

    config_dict = config.load()['default']
    if 'authorization' not in config_dict:
        click.echo('Set authorization ID.', err=True)
        sys.exit(1)
    authorization = config_dict['authorization']
    user_pool_id, client_id = platform.decode_cognito_setting(
        authorization)

    auth = Authorization(id_token=session_dict['id_token'],
                         access_token=session_dict['access_token'],
                         refresh_token=session_dict['refresh_token'],
                         sub=None,
                         client_id=client_id)
    auth.renew_token_if_expired()

    if auth.access_token != session_dict['access_token']:
        session.save(
            login_id=None,
            id_token=auth.id_token,
            refresh_token=auth.refresh_token,
            access_token=auth.access_token)

    return auth
