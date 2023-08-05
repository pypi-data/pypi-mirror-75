from wowpy.livestreams import LiveStream
from wowpy.transcoders import Transcoder
from wowpy.targets import TargetStream
from wowpy.utils import validate_schema, get_operation
from wowpy.constants import logger
from wowpy import schemas

def create_resource(specification):

  # Get data from specification
  version = specification['version']
  resource_name = specification['name']
  resource_keys = list(specification.keys())

  for resource_key in resource_keys:

    item = specification[resource_key]

    if type(item) is not dict:
      continue

    resource_type = item.get('type', None)
    if resource_type in [None, 'custom_target', 'output']:
      continue

    if resource_type == 'live_stream':
      live_stream_data = {'live_stream': specification[resource_key]['parameters']}
      live_stream_data['live_stream']['name'] = resource_name
      live_stream = LiveStream.create_live_stream(data=live_stream_data)
      live_stream_id = live_stream['id']
      outputs = Transcoder.get_transcoder_outputs(transcoder_id=live_stream_id)
      specification[resource_key]['id'] = live_stream_id
      specification['id'] = live_stream_id # set global id

      # Delete default output
      for output in outputs:
        output_id = output['id']
        Transcoder.delete_transcoder_output(transcoder_id=live_stream_id, output_id=output_id)
        target_id = output['output_stream_targets'][0]['stream_target']['id']
        TargetStream.delete_target(stream_type='fastly', stream_target_id=target_id)

    if resource_type == 'transcoder':
      transcoder_data = {'transcoder': specification[resource_key]['parameters']} 
      Transcoder.update_transcoder(transcoder_id=live_stream_id, data=transcoder_data)
      specification[resource_key]['id'] = live_stream_id

      output_keys = specification[resource_key]['outputs']
      for output_key in output_keys:
        output_data = {'output': specification[output_key]['parameters']}
        output_id = Transcoder.create_transcoder_output(transcoder_id=live_stream_id, data=output_data)
        specification[output_key]['id'] = output_id

        target_keys = specification[output_key]['targets']
        for target_key in target_keys:
          target_data = {'stream_target_custom': specification[target_key]['parameters']}
          target_provider = specification[target_key]['parameters']['provider'].split('_')
          target_provider_upper = target_provider[0].upper()
          target_name = '-'.join([resource_name, target_provider_upper])
          target_data['stream_target_custom']['name'] = target_name
          target_id = TargetStream.create_target(data=target_data)
          target_properties = specification[target_key]['properties']

          TargetStream.update_properties(stream_target_id=target_id, properties_data=target_properties)
          Transcoder.associate_target_stream(transcoder_id=live_stream_id, output_id=output_id, stream_target_id=target_id)
          specification[target_key]['id'] = target_id

  return specification
    
def update_resource(stored_spec, changes):
  resource_name = stored_spec['name']
  live_stream_id = stored_spec['id']
  changed_keys = list(changes.keys())

  targets = []
  outputs = []

  for changed_key in changed_keys:
    stored_data = stored_spec.get(changed_key, None) 
    if stored_data:
      resource_type = stored_data['type']
      resource_id = stored_data['id']
      resource_key = changed_key
    else:
      resource_type = changes[changed_key]['type']
      resource_id = ''
      resource_key = changed_key

    if resource_type == 'custom_target':
      resource_data = changes[changed_key]
      parameters = resource_data.get('parameters', None)
      properties = resource_data.get('properties', [])
      targets.append(
        {
          'id': resource_id,
          'type': resource_type,
          'key': resource_key,
          'parameters': parameters,
          'properties': properties
        }
      )

    if resource_type == 'output':
      resource_data = changes[changed_key]
      parameters = resource_data.get('parameters', None)
      output_targets = resource_data.get('targets', [])
      outputs.append(
        {
          'id': resource_id,
          'type': resource_type,
          'key': resource_key,
          'parameters': parameters,
          'targets': output_targets
        }
      )

  for target in targets:
    operation = get_operation(data=target)

    if operation == 'new':
      target_key = target['key']
      target_data = {'stream_target_custom': target['parameters']} 
      target_provider = target['parameters']['provider'].split('_')
      target_provider_upper = target_provider[0].upper()
      target_name = '-'.join([resource_name, target_provider_upper])
      # With the following line the 'name' key is added to target['parameters'] 
      target_data['stream_target_custom']['name'] = target_name
      target_id = TargetStream.create_target(data=target_data)
      target_properties = target['properties']
      TargetStream.update_properties(stream_target_id=target_id, properties_data=target_properties)
      stored_spec[target_key] = {
        'id': target_id,
        'type': target['type'],
        'parameters': target['parameters'],
        'properties': target['properties']
      }

  for output in outputs:
    operation = get_operation(data=output)
    output_key = output['key']
    if operation == 'insert':
      new_targets = output['targets']['$insert']
      for new_target in new_targets:
        target_key = new_target[1]
        output_id = output['id']
        target_id = stored_spec[target_key]['id']
        Transcoder.associate_target_stream(transcoder_id=live_stream_id, output_id=output_id, stream_target_id=target_id)
        stored_spec[output_key]['targets'].append(target_key)

  return stored_spec

def delete_resource(live_stream_id):
  try: 
    live_stream_info = LiveStream.get_live_stream(live_stream_id=live_stream_id)
    LiveStream.delete_live_stream(live_stream_id=live_stream_id)
    stream_targets = live_stream_info['stream_targets']
    for stream_target in stream_targets:
      stream_target_id = stream_target['id']
      TargetStream.delete_target('custom', stream_target_id)
  except Exception as excp:
    logger.info('Resource {live_stream_id} not propertly deleted'.format(live_stream_id=live_stream_id))
    raise Exception(str(excp))

# TODO: Validate lists in resource blocks

def validate_resource(specification):
  block_keys = specification.keys()
  for block_key in block_keys:
    if block_key in ['version', 'name', 'id']:
      continue
    data_block = specification[block_key]
    schema_name = data_block['type']+'_'+'schema'
    schema_uppercase = schema_name.upper().replace(' ','_') # upper replaces underscore with space
    schema_model = getattr(schemas, schema_uppercase)
    response = validate_schema(schema=schema_model, data=data_block)
    if not response['valid']:
      return False
  return True

def get_resource_info(id):
  resource_info = {
    'livestream': {},
    'transcoder': {},
    'targets': [],
    'schedule': {}
  }

  live_stream_info = LiveStream.get_live_stream(id)
  resource_info['livestream'] = live_stream_info
  transcoder_info = Transcoder.get_transcoder(id)
  resource_info['transcoder'] = transcoder_info
  transcoder_outputs = transcoder_info['outputs']
  for output_item in transcoder_outputs:
    stream_targets = output_item['output_stream_targets']
    for target_item in stream_targets:
      stream_target_id = target_item['stream_target']['id']
      stream_target_type = target_item['stream_target']['type']
      stream_target_info = TargetStream.get_target(stream_type=stream_target_type, stream_target_id=stream_target_id)
      stream_target_properties = TargetStream.get_target_properties(stream_type=stream_target_type, stream_target_id=stream_target_id)
      resource_info['targets'].append({'config': stream_target_info, 'properties': stream_target_properties})

#   schedule_info = Schedule.get_schedule(scheduler_id=scheduler_id)
#   resource_info['schedule'] = schedule_info

  return resource_info