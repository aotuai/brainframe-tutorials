# Import dependencies
from vcap import BaseCapsule, NodeDescription, BaseBackend, DetectionNode


# Define the Backend Class
class Backend(BaseBackend):
    # Since this is a fake Backend, we are not going to do any fancy stuff in
    # the constructor.
    def __init__(self, capsule_files, device):
        print("Loading onto device: ", device)
        super().__init__()

    # This is the function that doing the inference, we are just going to return
    # a fake bounding box here.
    def process_frame(self, frame, detection_node: None, options, state):
        return [
            DetectionNode(
                name="fake_box",
                coords=[[10, 10], [100, 10], [100, 100], [10, 100]]
            )
        ]

    # Batch process will help to improve the performance, we will skip it in
    # this example.
    def batch_predict(self, input_data_list):
        pass

    # Do some clean up work here
    def close(self) -> None:
        pass


# Define the Capsule class
class Capsule(BaseCapsule):
    # Metadata of this capsule
    name = "detector_bounding_box_fake"
    description = "A fake detector that outputs a single bounding box"
    version = 1
    # Define the input type, since this is an object detector, and doesn't
    # require any input from other capsules, the input type is a NodeDescription
    # with size None
    input_type = NodeDescription(size=NodeDescription.Size.NONE)
    # Define the output time, in this case, we are going to return a list of
    # bounding boxes so the output type would be size ALL
    output_type = NodeDescription(
        size=NodeDescription.Size.ALL,
        detections=["fake_box"],
    )
    # Define the backend, in this example, we are going to use the fake Backend
    backend_loader = lambda capsule_files, device: Backend(
        capsule_files=capsule_files, device=device)
    options = {}
