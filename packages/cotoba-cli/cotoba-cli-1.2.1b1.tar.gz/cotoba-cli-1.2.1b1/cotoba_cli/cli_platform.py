import logging
import os
import sys

import click

from cotoba_cli.cognito import get_cognito_authorization
from cotoba_cli import platform

from cotoba_cli import cli_test as test
from cotoba_cli import config

logger = logging.getLogger(__name__)


class PlatformAliasedGroup(click.Group):
    COMMAND_ALIASES = {
        'list-bot': 'list-bots',
        'list-api-key': 'list-api-keys'
    }

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        exec_cmd_name = self.COMMAND_ALIASES.get(cmd_name)
        if exec_cmd_name is None:
            return None
        return click.Group.get_command(self, ctx, exec_cmd_name)


def global_platform_options(func):
    for option in reversed([
        click.option('--output-headers', is_flag=True,
                     help='Output response headers.')
    ]):
        func = option(func)
    return func


@click.group(cls=PlatformAliasedGroup, help='Operate bot features.')
@click.option('--endpoint-url', type=str, help='Endpoint URL', default=None)
@global_platform_options
@click.pass_context
def cli_platform(context, endpoint_url, output_headers):
    if not context.obj:
        context.obj = {}
    if not endpoint_url:
        if os.environ.get('COTOBA_ENDPOINT_URL'):
            endpoint_url = os.environ.get('COTOBA_ENDPOINT_URL')
        elif config.load()['default'].get('endpoint-url'):
            endpoint_url = config.load()['default'].get('endpoint-url')
        else:
            click.echo('endpoint-url is not set.', err=True)
            sys.exit(1)

    context.obj['endpoint_url'] = endpoint_url
    context.obj['output_headers'] = output_headers


@cli_platform.command(help='Create a bot.')
@click.option('--file', 'file_path', type=str, required=True,
              help='Path to zipped bot file.')
@click.option('--name', type=str, default=None)
@click.option('--message', type=str, default=None)
@click.option('--nlu-url', type=str, default=None)
@click.option('--nlu-api-key', type=str, default=None,
              help='Api key to access nlu url.')
@global_platform_options
@click.pass_context
def create_bot(context,
               file_path,
               name,
               message,
               nlu_url,
               nlu_api_key,
               output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.create_bot(authorization,
                              file_path,
                              name=name,
                              message=message,
                              nlu_url=nlu_url,
                              nlu_api_key=nlu_api_key,
                              endpoint_url=endpoint_url,)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Get a bot by bot id.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@click.option('--output', 'zipfile_path', type=str,
              help='Download a scenario as zip file format.')
@global_platform_options
@click.pass_context
def get_bot(context, bot_id, zipfile_path, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.get_bot(authorization,
                           bot_id,
                           zipfile_path,
                           endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='List bots.')
@global_platform_options
@click.pass_context
def list_bots(context, output_headers):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = platform.list_bots(authorization, endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Update bot.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@click.option('--file', 'filepath', type=str,
              help='File path to scenario zip file.')
@click.option('--name', type=str, default=None)
@click.option('--message', type=str, default=None)
@click.option('--nlu-url', type=str, default=None)
@click.option('--nlu-api-key', type=str, default=None,
              help='Api key to access nlu url.')
@global_platform_options
@click.pass_context
def update_bot(context,
               bot_id,
               filepath,
               name,
               message,
               nlu_url,
               nlu_api_key,
               output_headers):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = platform.update_bot(authorization,
                              bot_id=bot_id,
                              endpoint_url=endpoint_url,
                              filepath=filepath,
                              name=name,
                              message=message,
                              nlu_url=nlu_url,
                              nlu_api_key=nlu_api_key)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Delete bot.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@global_platform_options
@click.pass_context
def delete_bot(context, bot_id, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.delete_bot(authorization, bot_id,
                              endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Run bot.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@click.option('--update', is_flag=True, help='Run running bot.')
@global_platform_options
@click.pass_context
def run_bot(context, bot_id, update, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.run_bot(authorization,
                           bot_id,
                           update,
                           endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Stop bot.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@global_platform_options
@click.pass_context
def stop_bot(context, bot_id, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.stop_bot(authorization, bot_id, endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Ask bot.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@click.option('--api-key', type=str, help='Api key.', required=True)
@click.option('--user-id', type=str, help='User id to keep conversation.',
              required=True)
@click.option('--utterance', type=str, help='Content of utterance.',
              required=True)
@click.option('--topic', type=str, help='Topic of utterance.',
              required=False)
@global_platform_options
@click.pass_context
def ask_bot(context, bot_id, api_key, user_id, utterance, topic, output_headers):
    endpoint_url = context.obj['endpoint_url']
    res = platform.ask_bot(bot_id=bot_id,
                           api_key=api_key,
                           user_id=user_id,
                           utterance=utterance,
                           topic=topic,
                           locale=config.load()['default'].get('locale'),
                           endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Debug bot.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@click.option('--api-key', type=str, help='Api key.', required=True)
@click.option('--user-id', type=str, help='User id to keep conversation.')
@global_platform_options
@click.pass_context
def debug_bot(context, bot_id, api_key, user_id, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.debug_bot(authorization,
                             bot_id=bot_id,
                             api_key=api_key,
                             user_id=user_id,
                             endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Create api-key.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
# NOTE: Hide expiredAt and maxApiCalls in v1.1
# @click.option('--expiration-days',
#               type=int,
#               help='Expiration days. Never expire if not set.',
#               default=None)
# @click.option('--max-api-calls',
#               type=int,
#               help='The number of times you can ask-bot '
#                    'using this api-key.\r'
#                    'Unlimited if not set.',
#               default=None)
@click.option('--description',
              type=str,
              help='Describe the purpose of using api-key.',
              default=None)
@global_platform_options
@click.pass_context
def create_api_key(context,
                   bot_id,
                   # expiration_days,
                   # max_api_calls,
                   description,
                   output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.create_api_key(authorization,
                                  bot_id=bot_id,
                                  # expiration_days=expiration_days,
                                  # max_api_calls=max_api_calls,
                                  expiration_days=None,
                                  max_api_calls=None,
                                  description=description,
                                  endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='List api-keys.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@global_platform_options
@click.pass_context
def list_api_keys(context, bot_id, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.list_api_keys(authorization,
                                 bot_id=bot_id,
                                 endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Get api-key.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@click.option('--api-key-id', type=str, help='Api key id.', required=True)
@global_platform_options
@click.pass_context
def get_api_key(context, bot_id, api_key_id, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.get_api_key(authorization,
                               bot_id=bot_id,
                               api_key=api_key_id,
                               endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Update api-key.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@click.option('--api-key-id', type=str, help='Api key id.', required=True)
# NOTE: Hide expiredAt and maxApiCalls in v1.1
# @click.option('--expiration-days',
#               type=str,
#               help='Expiration days. \rNo updated if not set.'
#                    ' If you set None, it will not expire.',
#               default='')
# @click.option('--max-api-calls',
#               type=str,
#               help='The number of times you can ask-bot '
#                    'using this api-key.\r'
#                    'No updated if not set. '
#                    'If you set None, it will unlimited.',
#               default='')
@click.option('--description',
              type=str,
              help='Describe the purpose of using api-key.',
              default=None)
@global_platform_options
@click.pass_context
def update_api_key(context,
                   bot_id,
                   api_key_id,
                   # expiration_days,
                   # max_api_calls,
                   description,
                   output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.update_api_key(authorization,
                                  bot_id=bot_id,
                                  api_key=api_key_id,
                                  # expiration_days=expiration_days,
                                  # max_api_calls=max_api_calls,
                                  expiration_days=None,
                                  max_api_calls=None,
                                  description=description,
                                  endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Delete api-key.')
@click.option('--bot-id', type=str, help='Bot id.', required=True)
@click.option('--api-key-id', type=str, help='Api key id.', required=True)
@global_platform_options
@click.pass_context
def delete_api_key(context, bot_id, api_key_id, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.delete_api_key(authorization,
                                  bot_id=bot_id,
                                  api_key=api_key_id,
                                  endpoint_url=endpoint_url)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


cli_platform.add_command(test.cli_test, 'test')


@cli_platform.command(help='Get bot logs.')
@click.option('--start-date', type=click.DateTime(['%Y-%m-%d']),
              help='Start date.')
@click.option('--end-date', type=click.DateTime(['%Y-%m-%d']),
              help='End date.')
@click.option('--limit', type=int, help='Maximum number of log.')
@click.option('--offset', type=int, default=0,
              help='Start index of log.')
@click.option('--bot-id', type=str, help='Bot id.')
@click.option('--api-key-id', type=str, help='Api key id.')
@global_platform_options
@click.pass_context
def get_bot_logs(context, start_date, end_date, limit, offset, bot_id,
                 api_key_id, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.get_bot_logs(authorization, endpoint_url,
                                start_date=start_date, end_date=end_date,
                                limit=limit, offset=offset,
                                bot_id=bot_id, api_key_id=api_key_id)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


AGGREGATION_TYPES = ['hours', 'days', 'weeks', 'months', 'byHour']


@cli_platform.command(help='Get bot traffics.')
@click.option('--aggregation', type=click.Choice(AGGREGATION_TYPES),
              required=True, help='Aggregation type of traffics.')
@click.option('--start-date', type=click.DateTime(['%Y-%m-%d']),
              help='Start date.')
@click.option('--end-date', type=click.DateTime(['%Y-%m-%d']),
              help='End date.')
@click.option('--bot-id', type=str, help='Bot id.')
@click.option('--api-key-id', type=str, help='Api key id.')
@global_platform_options
@click.pass_context
def get_bot_traffics(context, aggregation, start_date, end_date, bot_id,
                     api_key_id, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.get_bot_traffics(authorization, endpoint_url, aggregation,
                                    start_date=start_date, end_date=end_date,
                                    bot_id=bot_id, api_key_id=api_key_id)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)


@cli_platform.command(help='Get bot topics.')
@click.option('--aggregation', type=click.Choice(AGGREGATION_TYPES),
              required=True, help='Aggregation type of topics.')
@click.option('--start-date', type=click.DateTime(['%Y-%m-%d']),
              help='Start date.')
@click.option('--end-date', type=click.DateTime(['%Y-%m-%d']),
              help='End date.')
@click.option('--bot-id', type=str, help='Bot id.')
@click.option('--api-key-id', type=str, help='Api key id.')
@global_platform_options
@click.pass_context
def get_bot_topics(context, aggregation, start_date, end_date, bot_id,
                   api_key_id, output_headers):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = platform.get_bot_topics(authorization, endpoint_url, aggregation,
                                  start_date=start_date, end_date=end_date,
                                  bot_id=bot_id, api_key_id=api_key_id)
    if not output_headers:
        output_headers = context.obj['output_headers']
    res.print(output_headers=output_headers)
