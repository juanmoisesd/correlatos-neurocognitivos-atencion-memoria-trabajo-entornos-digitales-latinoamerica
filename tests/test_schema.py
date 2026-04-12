import json
import jsonschema
import pytest

def test_schema_validity():
    with open('schema.json', 'r') as f:
        schema = json.load(f)
    # Basic check that it's a valid JSON schema
    jsonschema.Draft7Validator.check_schema(schema)

def test_metadata_structure():
    with open('datapackage.json', 'r') as f:
        pkg = json.load(f)
    assert 'resources' in pkg
    assert pkg['name'] == 'correlatos-neurocognitivos-latam'
