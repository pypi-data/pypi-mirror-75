from wowpy.livestreams import LiveStream
from wowpy.recordings import Recording
from wowpy.transcoders import Transcoder
from wowpy.constants import logger
from wowpy.exceptions import DeleteRecordingException

class Mapper:

  @classmethod
  def map_live_streams(cls):
    document_batch = []
    live_streams = LiveStream.get_live_streams()
    for live_stream in live_streams:
      live_stream_id = live_stream['id']
      live_stream_name = live_stream['name']
      document = {
        'live_stream_name': live_stream_name,
        'live_stream_id': live_stream_id
      }
      document_batch.append(document)
    return document_batch
    
  @classmethod
  def map_recordings(cls):
    """
    Live stream id has the same value that transcoder id
    """
    document_batch = []
    live_streams = LiveStream.get_live_streams()

    ### TODO: Find a better way
    live_stream_dict = {}
    for live_stream in live_streams:
      live_stream_dict[live_stream['id']] = live_stream['name']
    ###

    recordings = Recording.get_recordings()
    for recording in recordings:
      try:
        recording_id = recording['id']
        transcoder_id = recording['transcoder_id']
        live_stream_name = live_stream_dict[transcoder_id]
        document = {
          'transcoder_id': transcoder_id,
          'live_stream_name': live_stream_name,
          'recording_id': recording_id
        }
        document_batch.append(document)
      except KeyError as err:
        logger.warning('Not found %s', err)
    return document_batch
