# Import dependencies
from vcap import BaseCapsule, NodeDescription, BaseBackend, DetectionNode


# Define the Backend Class
class Backend(BaseBackend):
    # Since this is a fake Backend, we are not going to do any fancy stuff in
    # the constructor.
    def __init__(self, capsule_files, device):
        print("Loading onto device:", device)
        super().__init__()

    # In a real capsule, this function will be performing inference or running
    # algorithms. For this tutorial, we are just going to return a single, fake
    # bounding box.
    def process_frame(self, frame, detection_node: None, options, state):
        return [
            DetectionNode(
                name="fake_box",
                coords=[[10, 10], [100, 10], [100, 100], [10, 100]]
            )
        ]

    # Batch process can be used to improve the performance, we will skip it in
    # this example.
    def batch_predict(self, input_data_list):
        pass

    # This function can be implemented to perform clean-up. We can't skip it
    # for this tutorial
    def close(self) -> None:
        pass


# Define the Capsule class
class Capsule(BaseCapsule):
    # Metadata of this capsule
    name = "detector_bounding_box_fake"
    description = "A fake detector that outputs a single bounding box"
    version = 1
    # Define the input type. As this is an object detector, and does not require
    # any input from other capsules, the input type will be a NodeDescription
    # with size=NONE
    input_type = NodeDescription(size=NodeDescription.Size.NONE)
    # Define the output type. In this case we are going to return a list of
    # bounding boxes, so the output type will be size=ALL
    output_type = NodeDescription(
        size=NodeDescription.Size.ALL,
        detections=["fake_box"],
    )
    # Define the backend. In this example, we are going to use a fake Backend,
    # defined below
    backend_loader = lambda capsule_files, device: Backend(
        capsule_files=capsule_files, device=device)
    options = {}
