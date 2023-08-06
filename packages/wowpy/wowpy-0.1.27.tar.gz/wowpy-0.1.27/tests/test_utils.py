import json
import pytest
from wowpy.utils import compare_specs, clean_changes

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

@pytest.fixture
def changes_spec_db_vs_spec_updated_unclean():
    with open('tests/fixtures/changes_spec_db_vs_spec_updated_unclean.json') as json_file:
        specification = json.load(json_file)
    return specification

def test_clean_changes(changes_spec_db_vs_spec_updated_unclean):
    response = clean_changes(changes_spec_db_vs_spec_updated_unclean)
    assert type(response) is dict

def test_compare_specs(spec_one_output_database, spec_one_output_template_updated):
    response = compare_specs(
        spec_src=spec_one_output_database,
        spec_dst=spec_one_output_template_updated
    )
    assert type(response) is dict