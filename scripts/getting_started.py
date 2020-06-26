# Import necessary libraries
from pathlib import Path
from brainframe.api import BrainFrameAPI, bf_codecs


# Initialize the API and connect to the server
api = BrainFrameAPI("http://localhost")

# Check the existing streams and print them out
stream_configs = api.get_stream_configurations()
print("Existing streams: ", stream_configs)

# Create a new ip camera stream configuration codec
new_ip_camera_stream_config = bf_codecs.StreamConfiguration(
    # The display name on the client side
    name="Ip Camera",
    connection_type=bf_codecs.ConnType.IP_CAMERA,
    # The url of the ip camera
    connection_options={
        "url": "your_ip_camera_url",
    },
    runtime_options={},
    premises_id=None,
)

# Create a local file stream configuration codec
new_web_camera_stream_config = bf_codecs.StreamConfiguration(
    # The display name on the client side
    name="Webcam",
    connection_type=bf_codecs.ConnType.WEBCAM,
    # The device id of the web camera
    connection_options={
        "device_id": 0,
    },
    runtime_options={},
    premises_id=None,
)

# Upload the local file to the database and create a storage id
storage_id = api.new_storage(
    data=Path("../videos/shopping_cashier_gone.mp4").read_bytes(),
    mime_type="application/octet-stream"
)
# Create a local file stream configuration codec
new_local_file_stream_config = bf_codecs.StreamConfiguration(
    # The display name on the client side
    name="Local File",
    connection_type=bf_codecs.ConnType.FILE,
    # The storage id of the file
    connection_options={
        "storage_id": storage_id,
    },
    runtime_options={},
    premises_id=None,
)

# Tell the server to connect to that stream configuration
new_local_file_stream_config = api.set_stream_configuration(
    new_local_file_stream_config)

# Tell the server to start analyzing the stream you just set
api.start_analyzing(new_local_file_stream_config.id)
