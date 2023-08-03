from enum import Enum
from aixplain.client import AixplainClient

LANGUAGES_PATH = 'sdk/languages'
FUNCTIONS_PATH = 'sdk/languages'
LICENSES_PATH = 'sdk/licenses'


def populate_language_enum(client: AixplainClient) -> Enum:
    """Generate an Enum representing available languages and dialects."""
    payload = client.get(LANGUAGES_PATH)
    languages = {}
    for entry in payload:
        language = entry['value']
        language_label = '_'.join(entry['label'].split())
        languages[language_label] = {'language': language, 'dialect': None}
        for dialect in entry['dialects']:
            dialect_label = '_'.join(dialect['label'].split()).upper()
            dialect_value = dialect['value']
            dialect_key = f'{language_label} {dialect_label}'
            languages[dialect_key] = {
                'language': language,
                'dialect': dialect_value
            }
    return Enum('Language', languages, type=dict)


def populate_license_enum(client) -> Enum:
    """Generate an Enum representing available licenses."""
    payload = client.get(LICENSES_PATH)
    licences = {}
    for entry in payload:
        license_key = '_'.join(entry['name'].split())
        license_value = entry['id']
        licences[license_key] = license_value
    return Enum('License', licences, type=str)


def populate_function_enum(client) -> Enum:
    """Generate an Enum representing available functions."""
    payload = client.get(FUNCTIONS_PATH)
    licences = {}
    for entry in payload['items']:
        function_key = entry['id'].upper().replace('-', '_')
        function_value = entry['id']
        licences[function_key] = function_value
    return Enum('Function', licences, type=str)
