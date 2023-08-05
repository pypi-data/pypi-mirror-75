import json
import pytest
from cli.utils import compare_specs

@pytest.fixture
def spec_one_output_database():
    with open('tests/fixtures/spec_one_output_database.json') as json_file:
        specification = json.load(json_file)
    return specification

@pytest.fixture
def spec_one_output_template_updated():
    with open('tests/fixtures/spec_one_output_template_updated.json') as json_file:
        specification = json.load(json_file)
    return specification

def test_compare_specs(spec_one_output_database, spec_one_output_template_updated):
    response = compare_specs(
        spec_src=spec_one_output_database,
        spec_dst=spec_one_output_template_updated
    )
    assert type(response) is dict