# Import necessary libraries
from brainframe.api import BrainFrameAPI
from brainframe.api.bf_codecs import StreamConfiguration, ConnType

# Initialize the API and connect to the server
api = BrainFrameAPI("http://localhost")

# Check the existing streams and print them out
stream_configs = api.get_stream_configurations()
print("Existing streams: ", stream_configs)

# Create a new new stream configuration codec
new_stream_config = StreamConfiguration(
    # The display name on the client side
    name="Test config",
    # Type of the stream, for now we support ip cameras, web cams and video file
    connection_type=ConnType.IP_CAMERA,
    # The url of the ip camera
    connection_options={
        "url": "rtsp:xxxxx",
    },
    runtime_options={},
    premises_id=None,
)

# Tell the server to connect to that stream configuration
new_stream_config = api.set_stream_configuration(new_stream_config)

# Tell the server to start analyzing the stream you just set
api.start_analyzing(new_stream_config.id)
