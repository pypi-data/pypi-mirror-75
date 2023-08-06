import requests
import functools
import json
import os
from jsondiff import diff
from boltons.iterutils import remap
from requests.exceptions import HTTPError, ConnectionError, Timeout
from wowpy.constants import logger
from wowpy.exceptions import DeleteRecordingException

# utils

def safe_run(func):
  @functools.wraps(func)
  def func_wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except Exception as excp:
      logger.error(excp)
      return 'not created'
  return func_wrapper

# core

def get_operation(data):
  operation = ''

  data_in_text = json.dumps(data)

  if 'insert' in data_in_text:
    operation = 'insert'
  elif 'delete' in data_in_text:
    operation = 'delete'
  else:
    operation = 'new'

  return operation

def validate_schema(schema, data):
  try:
    data = schema(data)
  except Exception as excp:
    logger.error(excp)
    return {'valid': False, 'data': None}
  return {'valid': True, 'data': data}

def make_query(endpoint, method, headers={}, data={}, auth=(), description='not description'):
  logger.info('Endpoint: {}, Method: {}, Data: {}, Description: {}'.format(endpoint, method, data, description))
  try:
    request_method = getattr(requests, method)
    response = request_method(endpoint, json=data, headers=headers, auth=auth)
    logger.debug('Response is: {}'.format(vars(response)))
    response.raise_for_status()
    logger.info('Endpoint {} succesfully reached'.format(endpoint))
  except HTTPError as err:
    logger.error(err.response.text)
    err_data = json.loads(err.response.text)
    message = err_data['meta']['message']
    status = err_data['meta']['status']
    if status == 410:
      raise DeleteRecordingException
    else:
      raise Exception(message)
  except ConnectionError as err:
    logger.error(err.response.text)
    raise Exception(str(err))
  except Timeout as err:
    logger.error(err.response.text)
    raise Exception(str(err))
  except Exception as err:
    logger.error(err)
    raise Exception(str(err))
  return response

# wowza core

def wowza_query(endpoint, method, data={}):
  wsc_access_key = os.environ.get('WSC_ACCESS_KEY')
  wsc_api_key = os.environ.get('WSC_API_KEY')
  headers = {
      'Content-Type': 'application/json',
      'cache-control': 'no-cache',
      'wsc-access-key': wsc_access_key,
      'wsc-api-key': wsc_api_key
  }
  response = make_query(endpoint=endpoint, method=method, headers=headers, data=data)

  if method == 'delete':
    response = response.text
  else:
    response = response.json()

  return response

# core utils compare

def compare_specs(spec_src, spec_dst):
    changes = diff(spec_src, spec_dst, marshal=True)
    changes = json.loads(json.dumps(changes)) # turn integer keys into string keys
    return changes

def clean_changes(changes):
    drop_empty = lambda path, key, value: bool(value)
    clean = remap(changes, visit=drop_empty)
    drop_delete_name = lambda path, key, value: not value == {'parameters': {'$delete': ['name']}}
    clean = remap(clean, visit=drop_delete_name)
    return clean