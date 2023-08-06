import click
import csv
import re
from cotoba_cli import platform
from cotoba_cli.error import InvalidArgumentError


def get_key_command_pair(expected_key):
    if '@' not in expected_key:
        return (expected_key, None)

    splitted_key = expected_key.split('@')
    key = '@'.join(splitted_key[0:-1])
    command = splitted_key[-1]
    return (key, command)


def compare_by_command(actual, expected, command):
    if command is None:
        if type(actual) is dict and type(expected) is dict:
            return compare_traverse(actual, expected)
        else:
            return actual == expected
    elif command == 'regex':
        return re.search(expected, actual) is not None
    elif command == 'any':
        if type(expected) is list:
            for expected_item in expected:
                if compare_traverse(actual, expected_item):
                    return True
        return False
    else:
        return False


def compare_traverse(actual, expected):
    if type(actual) is dict and type(expected) is dict:
        for expected_key in expected.keys():
            key, command = get_key_command_pair(expected_key)
            if key not in actual:
                return False
            if not compare_by_command(actual[key], expected[expected_key], command):
                return False

        return True
    else:
        return actual == expected


def ask_and_compare_tests(bot_id, api_key, tests, endpoint_url, default_locale, show_progress=True):
    """
    todo: write tests format
    """
    results = []
    for test_number, test in enumerate(tests, 1):
        if 'request' not in test:
            raise InvalidArgumentError('request field is required')
        if 'expected' not in test:
            raise InvalidArgumentError('expected field is required')

        request = test['request']
        result = {}
        errors = []

        utterance = request.get('utterance')
        topic = request.get('topic')
        metadata = request.get('metadata')
        user_id = request.get('userId')
        locale = request.get('locale', default_locale)
        log_level = request.get('config', {}).get('logLevel')

        if utterance is None:
            errors.append('utterance is required.')

        if user_id is None:
            errors.append('userId is required.')

        if len(errors) > 0:
            if show_progress:
                click.secho(f'Error in test number {test_number}', fg='red', err=True)
                click.echo('-' * 16, err=True)
            result['errors'] = errors
            results.append(result)
            continue

        response_obj = platform.ask_bot(
            bot_id=bot_id,
            api_key=api_key,
            user_id=user_id,
            utterance=utterance,
            topic=topic,
            metadata=metadata,
            log_level=log_level,
            locale=locale,
            endpoint_url=endpoint_url
        )
        response = response_obj.get_response_body()
        result['utterance'] = utterance
        result['topic'] = response.get('topic')
        result['metadata'] = response.get('metadata')
        result['request_time'] = response_obj.get_request_time()
        result['response'] = response['response']

        expected = test['expected']
        result['expected'] = expected
        compare_result = {}
        for expected_key in expected:
            key, command = get_key_command_pair(expected_key)
            compare_result[key] = (
                key in result and
                compare_by_command(result[key], expected[expected_key], command))
        result['compare_result'] = compare_result
        results.append(result)

        if show_progress:
            click.secho(f'utterance: {utterance}', fg='bright_magenta', err=True)
            click.secho(f'response: {response["response"]}', fg='bright_magenta', err=True)
            for key, result in compare_result.items():
                click.echo(f'compare result({key}): {_result_as_text(result)}', err=True)
            click.echo('-' * 16, err=True)

    return results


def output_rows_to_csv(rows_with_header, output_stream, write_header):
    if len(rows_with_header) == 0:
        return

    fieldnames = list(rows_with_header[0].keys())
    writer = csv.DictWriter(output_stream, fieldnames=fieldnames)
    if write_header:
        writer.writeheader()
    writer.writerows(rows_with_header)


def _result_as_text(result):
    if type(result) is bool:
        return 'OK' if result else 'NG'
    else:
        return None


def output_result_as_csv(compare_results, output_stream, write_header):
    rows_with_header = []
    for result in compare_results:
        if 'errors' in result:
            continue
        row = {
            'timestamp': result['request_time'],
            'utterance': result['utterance'],
            'response text': result['response'],
            'expected response text': result['expected'].get('response'),
            'response text result': _result_as_text(result['compare_result'].get('response')),
            'topic': result['topic'],
            'expected topic': result['expected'].get('topic'),
            'topic result': _result_as_text(result['compare_result'].get('topic')),
            'metadata': result['metadata'],
            'expected metadata': result['expected'].get('metadata'),
            'metadata result': _result_as_text(result['compare_result'].get('metadata'))
        }
        rows_with_header.append(row)

    output_rows_to_csv(rows_with_header, output_stream, write_header)
