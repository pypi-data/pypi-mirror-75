from voluptuous import Schema, Required, All, Length, Range, Any, Optional

RESOURCE_SCHEMA = Schema({
    Required('version'): All(str, Length(min=0)),
    Required('name'): All(str, Length(min=0)),
    Required('id'): All(str, Length(min=0))
})

# TODO: Move all values to template, only left required ones

LIVE_STREAM_SCHEMA = Schema({
    Required('type'): 'live_stream',
    Required('id'): All(str, Length(min=0)),
    Required('parameters'): { # key is live_stream
        # Required
        Required('aspect_ratio_height'): All(int, Range(min=0)),
        Required('aspect_ratio_width'): All(int, Range(min=0)),
        Required('billing_mode'): All(str, Length(min=0)),
        Required('broadcast_location'): All(str, Length(min=0)),
        Required('encoder'): All(str, Length(min=0)),
        Required('name', default=''): All(str, Length(min=0)),
        Required('transcoder_type'): All(str, Length(min=0)),
        Required('delivery_method'): Any('pull','push'),
        # Non required
        'delivery_protocols': [All(str, Length(min=0)),All(str, Length(min=0))],
        'delivery_type': All(str, Length(min=0)),
        'disable_authentication': All(bool), # push
        'low_latency': All(bool),
        'recording': All(bool),
        'target_delivery_protocol': All(str, Length(min=0)),
        'use_stream_source': All(bool),
        'source_url': All(str, Length(min=0)),  # pull
    }
})

TRANSCODER_SCHEMA = Schema({
    Required('type'): 'transcoder', 
    Required('id'): All(str, Length(min=0)),
    Required('outputs'): All(
        [
            All(str, Length(min=0))
        ]
    ),
    Required('parameters'): { # key is empty
        Required('idle_timeout'): All(int, Range(min=0)),
        Required('buffer_size'): All(int, Range(min=0)),
        Required('low_latency'): All(bool)
    }
})

OUTPUT_SCHEMA = Schema({
    Required('type'): 'output',
    Required('id'): All(str, Length(min=0)),
    Required('targets'): All(
        [
            All(str, Length(min=0))
        ]
    ),
    Required('parameters'): {  # key is output
        # Required
        Required('stream_format'): All(str, Length(min=0)),
        Required('h264_profile'): All(str, Length(min=0)),
        Required('aspect_ratio_width'): All(int, Range(min=0)),
        Required('aspect_ratio_height'): All(int, Range(min=0)),
        Required('bitrate_video'): All(int, Range(min=0)),
        Required('bitrate_audio'): All(int, Range(min=0)),
        # Non required
        'framerate_reduction': All(str, Length(min=0)),
        'keyframes': All(str, Length(min=0)),
        'passthrough_audio': All(bool),
        'passthrough_video': All(bool)
    }
})

CUSTOM_TARGET_SCHEMA = Schema({
    Required('type'): 'custom_target',
    Required('id'): All(str, Length(min=0)),
    Required('parameters'): {  # key is stream_target_custom
        Required('provider'): Any('akamai_cupertino', 'rtmp', 'akamai_rtmp'),
        Required('primary_url'): All(str, Length(min=0)),
        Required('stream_name'): All(str, Length(min=0)),
        Required('use_https', default=True): All(bool)
    },
    'properties':
        All(
            [
                {
                    Required('property'): {
                        Required('key'): All(str, Length(min=0)),
                        Required('section'): All(str, Length(min=0)),
                        Required('value'): All(int, Range(min=0))
                    }
                }
            ]
        )
})
