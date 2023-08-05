import pytest
import json
from cli.database import Database

@pytest.fixture
def database():
    database = Database(database_file_path='tests/fixtures/test_database.json')
    return database

@pytest.fixture
def spec_one_output_template():
    with open('tests/fixtures/spec_one_output_template.json') as json_file:
        specification = json.load(json_file)
    return specification

@pytest.fixture
def spec_one_output_database():
    with open('tests/fixtures/spec_one_output_database.json') as json_file:
        specification = json.load(json_file)
    return specification

def test_live_streams_table_exist(database):
    exist = database.live_streams_table_exist()
    assert exist in [False, True]

def test_insert_specification(database, spec_one_output_database):
    database.insert_specification(spec_one_output_database)
    assert 1==1

def test_insert_live_stream_mapping(database):
    document = {
        'live_stream_name': 'Baton-Test',
        'live_stream_id': 'mbwlljdc'
    }
    database.insert_live_stream_mapping(document)
    assert 1==1

def test_get_live_stream_id_from_name(database):
    id = database.get_live_stream_id_from_name('Baton-Test')
    assert id=='mbwlljdc'

def test_delete_specification(database, spec_one_output_database):
    id = spec_one_output_database['id']
    database.delete_specification(id)
    assert 1==1

def test_delete_live_stream_mapping(database, spec_one_output_database):
    id = spec_one_output_database['id']
    database.delete_live_stream_mapping(id)
    assert 1==1