# import necessary libraries
from brainframe.api import BrainFrameAPI
from brainframe.api.bf_codecs import StreamConfiguration, ConnType

# initialize the API and connect to the server
api = BrainFrameAPI("http://localhost")

# check the existing streams and print them out
stream_configs = api.get_stream_configurations()
print("Existing streams: ", stream_configs)

# create a new new stream configuration codec
new_stream_config = StreamConfiguration(
    name="Test config",
    connection_type=ConnType.IP_CAMERA,
    connection_options={
        "url": "rtsp:xxxxx",
    },
    runtime_options={},
    premises_id=None,
)

# tell the server to connect to that stream configuration
new_stream_config = api.set_stream_configuration(new_stream_config)

# tell the server to start analyzing the stream you just set
api.start_analyzing(new_stream_config.id)
