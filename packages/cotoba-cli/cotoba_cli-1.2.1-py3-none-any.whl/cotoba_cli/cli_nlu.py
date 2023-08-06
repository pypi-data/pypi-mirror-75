import os
import click
import sys

from cotoba_cli.cognito import get_cognito_authorization
from cotoba_cli import config
from cotoba_cli import nlu


@click.group(help='Operate natural language understanding features')
@click.option('--endpoint-url', type=str, help='Endpoint URL', default=None)
@click.pass_context
def cli_nlu(context, endpoint_url):
    if not context.obj:
        context.obj = {}
    if not endpoint_url:
        if os.environ.get('COTOBA_ENDPOINT_URL'):
            endpoint_url = os.environ.get('COTOBA_ENDPOINT_URL')
        elif config.load()['default'].get('endpoint-url'):
            endpoint_url = config.load()['default'].get('endpoint-url')
        else:
            sys.stderr.write('endpoint-url is not set.\n')
            sys.exit(1)

    context.obj['endpoint_url'] = endpoint_url


@cli_nlu.command(help='Create and upload training data.')
@click.option('--name', 'name', type=str, required=True,
              help='Name.')
@click.option('--file', 'file_path', type=str, required=True,
              help='Path to training data file.')
@click.pass_context
def create_training_data(context, name, file_path):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.create_training_data(authorization, name, file_path,
                                   endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Update training data description.')
@click.option('--training-data-id', 'training_data_id',
              type=str, required=True,
              help='Training data name to read.')
@click.option('--name', 'name', type=str, required=False,
              help='Name.')
@click.option('--description', 'description', type=str, required=False,
              help='Description of updated content.')
@click.pass_context
def update_training_data(context, training_data_id, name, description):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.update_training_data(authorization,
                                   training_data_id,
                                   name,
                                   description,
                                   endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Delete training data.')
@click.option('--training-data-id', 'training_data_id',
              type=str, required=True,
              help='Training data name to read.')
@click.pass_context
def delete_training_data(context, training_data_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.delete_training_data(authorization, training_data_id,
                                   endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='List training data.')
@click.pass_context
def list_training_data(context):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.list_training_data(authorization, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read training data.')
@click.option('--training-data-id', 'training_data_id',
              type=str, required=True,
              help='Training data name to read.')
@click.pass_context
def read_training_data(context, training_data_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_training_data(authorization, training_data_id,
                                 endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='List model type.')
@click.pass_context
def list_model_type(context):
    endpoint_url = context.obj['endpoint_url']
    res = nlu.list_model_type(endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read model type.')
@click.option('--model-type-name', 'model_type_name',
              type=str, required=True, help='Model type name.')
@click.pass_context
def read_model_type(context, model_type_name):
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_model_type(model_type_name,
                              endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Create and upload slot dictionary.')
@click.option('--name', 'name', type=str, required=True,
              help='Name.')
@click.option('--file', 'file_path', type=str, required=True,
              help='Path to slot dictionary file.')
@click.pass_context
def create_slot_dictionary(context, name, file_path):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.create_slot_dictionary(authorization, name, file_path,
                                     endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read slot dictionary.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, required=True,
              help='Slot dictionary name to read.')
@click.pass_context
def read_slot_dictionary(context, slot_dictionary_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_slot_dictionary(authorization, slot_dictionary_id,
                                   endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Delete slot dictionary.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, required=True,
              help='Slot dictionary name to delete.')
@click.pass_context
def delete_slot_dictionary(context, slot_dictionary_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.delete_slot_dictionary(authorization, slot_dictionary_id,
                                     endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Update slot dictionary description.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, required=True,
              help='Slot dictionary name to delete.')
@click.option('--name', 'name', type=str, required=False,
              help='Name.')
@click.option('--description', 'description', type=str, required=False,
              help='Description of updated content.')
@click.pass_context
def update_slot_dictionary(context, slot_dictionary_id, name, description):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.update_slot_dictionary(authorization,
                                     slot_dictionary_id,
                                     name,
                                     description,
                                     endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='List slot dictionary.')
@click.pass_context
def list_slot_dictionary(context):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.list_slot_dictionaries(authorization, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Create model.')
@click.option('--training-data-id', 'training_data_id',
              type=str, required=True,
              help='Training data id.')
@click.option('--model-type-name', 'model_type_name',
              type=str, required=True,
              help='Model type name.')
@click.option('--name', 'name',
              type=str, required=True,
              help='Name.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, required=False,
              help='Slot dictionary id.')
@click.option('--description', 'description',
              type=str, required=False,
              help='Description.')
@click.option('--hyper-parameters-file', 'file_path',
              type=str, required=False,
              help='Path to Hyper parameters file.')
@click.option('--hyper-parameters', 'hyper_parameters',
              type=str, required=False,
              help='Hyper parameters. Invalid when option '
                   '--hyper-parameters-file is specified.')
@click.option('--original-model-id', 'original_model_id',
              type=str, required=False,
              help='original model id for continuous learning.')
@click.pass_context
def create_model(context,
                 training_data_id,
                 model_type_name,
                 slot_dictionary_id,
                 name,
                 description,
                 file_path,
                 hyper_parameters,
                 original_model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.create_model(authorization,
                           training_data_id,
                           model_type_name,
                           slot_dictionary_id,
                           name,
                           description,
                           file_path,
                           hyper_parameters,
                           original_model_id,
                           endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Update model description.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.option('--name', 'name', type=str, required=False,
              help='Model name.')
@click.option('--description', 'description',
              type=str, required=False,
              help='Description of updated content.')
@click.pass_context
def update_model(context, model_id, name, description):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.update_model(authorization, model_id, name, description,
                           endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read model.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def read_model(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_model(authorization, model_id, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Delete model.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def delete_model(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.delete_model(authorization, model_id, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='List model.')
@click.pass_context
def list_model(context):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.list_models(authorization, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Create endpoint.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, help='slot dictionary id.')
@click.option('--min-capacity', 'min_capacity',
              type=int, help='min capacity for auto-scaling.',
              default=1)
@click.option('--max-capacity', 'max_capacity',
              type=int, help='max capacity for auto-scaling.',
              default=1)
@click.option('--initial-instance-count', 'initial_instance_count',
              type=int,
              help='initial instance count for creating endpoint.',
              default=1)
@click.pass_context
def create_endpoint(context, model_id, min_capacity, max_capacity,
                    initial_instance_count, slot_dictionary_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.create_endpoint(authorization, model_id,
                              min_capacity, max_capacity,
                              initial_instance_count,
                              slot_dictionary_id,
                              endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Update endpoint.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.option('--min-capacity', 'min_capacity',
              type=int, help='min capacity for auto-scaling.',
              default=1)
@click.option('--max-capacity', 'max_capacity',
              type=int, help='max capacity for auto-scaling.',
              default=1)
@click.option('--desired-instance-count', 'desired_instance_count',
              type=int,
              help='desired instance count for updating endpoint.',
              required=True)
@click.pass_context
def update_endpoint(context, model_id, min_capacity, max_capacity,
                    desired_instance_count):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.update_endpoint(authorization, model_id,
                              min_capacity, max_capacity,
                              desired_instance_count,
                              endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Get inference log.')
@click.option('--start-date', 'start_date',
              type=click.DateTime(['%Y-%m-%d']),
              help='Start date.')
@click.option('--end-date', 'end_date',
              type=click.DateTime(['%Y-%m-%d']),
              help='End date.')
@click.option('--limit', 'limit', type=int, help='Maximum number of log.')
@click.option('--offset', 'offset', type=int, default=0,
              help='Start index of log.')
@click.option('--api-key-id', 'api_key_id',
              type=str, help='Api key id.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def get_inference_logs(context,
                       model_id,
                       api_key_id,
                       start_date,
                       end_date,
                       limit,
                       offset):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.get_inference_logs(authorization,
                                 model_id,
                                 api_key_id,
                                 start_date,
                                 end_date,
                                 limit,
                                 offset,
                                 endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read possitble intents of model.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def read_intent(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_intent(authorization, model_id, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read possible slots of model.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def read_slot(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_slot(authorization, model_id, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read possible dictionary label of model.')
@click.option('--model-id',
              'model_id',
              type=str,
              required=True,
              help='model id.')
@click.pass_context
def read_dictionary_label(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_dictionary_label(
        authorization, model_id, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='delete endpoint.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def delete_endpoint(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.delete_endpoint(authorization, model_id,
                              endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Inference by using endpoint.')
@click.option('--utterance', 'utterance',
              type=str, required=True,
              help='utterance.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.option('--api-key', 'api_key',
              type=str, required=True,
              help='api key.')
@click.option('--slot-dic', 'slot_dic',
              type=str, default='',
              help='slot dic json (file or text).')
@click.pass_context
def inference(context, utterance, model_id, api_key, slot_dic):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.inference(authorization,
                        utterance,
                        model_id,
                        api_key,
                        slot_dic=slot_dic,
                        endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Get endpoint url.')
@click.option('--endpoint-id', 'endpoint_id',
              type=str, required=True,
              help='endpoint_id.')
@click.option('--api-key', 'api_key',
              type=str, required=True,
              help='api_key.')
@click.pass_context
def get_endpoint_url(context, endpoint_id, api_key):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.get_endpoint_url(authorization,
                               endpoint_id,
                               api_key=api_key,
                               endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read remaining resources.')
@click.pass_context
def read_remaining_resources(context):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.read_remaining_resources(authorization,
                                       endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Create api-key.')
@click.option('--model-id', type=str, help='Model id.', required=True)
@click.option('--description',
              'description',
              type=str,
              required=False,
              default='',
              help='Description of created content.')
@click.pass_context
def create_api_key(context,
                   model_id,
                   description):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.create_api_key(authorization,
                             model_id,
                             description,
                             endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='List api-keys.')
@click.option('--model-id', type=str, help='Model id.', required=True)
@click.pass_context
def list_api_keys(context, model_id):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.list_api_keys(authorization,
                            model_id,
                            endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read api-key.')
@click.option('--model-id', type=str, help='Model id.', required=True)
@click.option('--api-key-id', type=str, help='Api key id.', required=True)
@click.pass_context
def read_api_key(context, model_id, api_key_id):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.read_api_key(authorization,
                           model_id,
                           api_key_id=api_key_id,
                           endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Update api-key.')
@click.option('--model-id', type=str, help='Model id.', required=True)
@click.option('--api-key-id', type=str, help='Api key id.', required=True)
@click.option('--description',
              'description',
              type=str,
              required=True,
              help='Description of created content.')
@click.pass_context
def update_api_key(context,
                   model_id,
                   api_key_id,
                   description):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.update_api_key(authorization,
                             model_id,
                             api_key_id,
                             description,
                             endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Delete api-key.')
@click.option('--model-id', type=str, help='Model id.', required=True)
@click.option('--api-key-id', type=str, help='Api key id.', required=True)
@click.pass_context
def delete_api_key(context, model_id, api_key_id):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.delete_api_key(authorization,
                             model_id,
                             api_key_id,
                             endpoint_url=endpoint_url)
    res.print()
