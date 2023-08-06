import pytest
import json
import requests
from unittest import skipIf
from mock import patch, Mock
from wowpy.resources import validate_resource, create_resource, update_resource
from wowpy.constants import SKIP_REAL

@pytest.fixture
def spec_one_output_template_full():
    with open('tests/fixtures/spec_one_output_template_full.json') as json_file:
        specification = json.load(json_file)
    return specification

@pytest.fixture
def spec_one_output_database():
    with open('tests/fixtures/spec_one_output_database.json') as json_file:
        specification = json.load(json_file)
    return specification

@pytest.fixture
def changes_spec_db_vs_spec_updated():
    with open('tests/fixtures/changes_spec_db_vs_spec_updated.json') as json_file:
        specification = json.load(json_file)
    return specification

def test_validate_resource(spec_one_output_template_full):
    valid = validate_resource(specification=spec_one_output_template_full)
    assert valid == True

@patch('wowpy.resources.Transcoder.associate_target_stream')
@patch('wowpy.resources.TargetStream.update_properties')
@patch('wowpy.resources.TargetStream.create_target')
@patch('wowpy.resources.Transcoder.create_transcoder_output') # returns an output id
@patch('wowpy.resources.Transcoder.update_transcoder')
@patch('wowpy.resources.Transcoder.get_transcoder_outputs')
@patch('wowpy.resources.LiveStream.create_live_stream')
def test_create_resource(mock_create_live,
                         mock_get_trans,
                         mock_update_trans, 
                         mock_create_output, 
                         mock_create_target, 
                         mock_update_target, 
                         mock_target_associate, 
                         spec_one_output_template_full):
    mock_create_live.return_value = {'id': 'abc123'}
    mock_get_trans.return_value = []
    mock_update_trans.return_value = None
    mock_create_output.return_value = 'abc123'
    mock_create_target.return_value = 'abc-123'
    mock_update_target.return_value = None
    mock_update_trans.return_value = None
    mock_target_associate.return_value = None
    specification = create_resource(specification=spec_one_output_template_full)
    assert type(specification) is dict

@patch('wowpy.resources.Transcoder.associate_target_stream')
@patch('wowpy.resources.TargetStream.update_properties')
@patch('wowpy.resources.TargetStream.create_target')
def test_update_resource(mock_create_target, 
                         mock_update_target, 
                         mock_target_associate,
                         spec_one_output_database,
                         changes_spec_db_vs_spec_updated):
    mock_create_target.return_value = 'abc-123'
    mock_update_target.return_value = None
    mock_target_associate.return_value = None
    updated_spec_with_ids = update_resource(spec_one_output_database, changes_spec_db_vs_spec_updated)
    assert type(updated_spec_with_ids) is dict

###

@skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
def test_real_create_resource(spec_one_output_template_full):
    specification = create_resource(specification=spec_one_output_template_full)
    assert type(specification) is dict