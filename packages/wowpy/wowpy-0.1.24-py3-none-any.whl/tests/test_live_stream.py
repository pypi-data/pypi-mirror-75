import pytest
import json
import requests
from mock import patch, Mock
from wowpy.livestreams import LiveStream

@pytest.fixture
def live_stream_data():
    with open('tests/fixtures/spec_one_output_template_full.json') as json_file:
        specification = json.load(json_file)
    live_stream_data = {'live_stream': specification['live_stream']['parameters']}
    live_stream_data['live_stream']['name'] = specification['name']
    return live_stream_data

@patch('wowpy.livestreams.wowza_query')
def test_create_live_stream(mock_wowza_query, live_stream_data):
    mock_wowza_query.return_value = {'live_stream': {'id': 'abc123'}}
    live_stream_info = LiveStream.create_live_stream(data=live_stream_data)
    assert type(live_stream_info) is dict