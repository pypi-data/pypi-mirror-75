from wowpy.constants import WSC_API_ENDPOINT, logger
from wowpy.utils import wowza_query
from wowpy.constants import logger
from wowpy.exceptions import DeleteRecordingException

class Recording:
  recording_base = WSC_API_ENDPOINT + 'recordings'
  recording_pagination = recording_base + '/?page={page_number}&per_page=1000'
  recording_single = recording_base + '/{recording_id}'                         # recording delete, get

  @classmethod
  def get_recording(cls, recording_id):
    # Get recording info
    endpoint = cls.recording_single.format(
      recording_id=recording_id
    )
    response = wowza_query(endpoint=endpoint, method='get')
    recording = response['recording']
    logger.debug('Recording info is {}'.format(recording))
    return recording

  @classmethod
  def get_recordings(cls):
    # Get the list of livestream
    response = wowza_query(endpoint=cls.recording_base, method='get')
    recordings = response['recordings']

    total_pages = response['pagination']['total_pages']
    for i in range(2, total_pages + 1):
      try:
        endpoint = cls.recording_pagination.format(page_number=i)
        response = wowza_query(endpoint=endpoint, method='get')
        recordings.extend(response['recordings'])
      except DeleteRecordingException as err:
        logger.warning(err)
    return recordings