# Import dependencies
from typing import Dict
import numpy as np
from vcap import (
    BaseCapsule,
    NodeDescription,
    DetectionNode,
    FloatOption,
    DETECTION_NODE_TYPE,
    OPTION_TYPE,
    BaseStreamState,
    rect_to_coords,
)
from vcap_utils import TFObjectDetector


# Define the Backend Class
class Backend(TFObjectDetector):
    def process_frame(self, frame: np.ndarray,
                      detection_node: None,
                      options: Dict[str, OPTION_TYPE],
                      state: BaseStreamState) -> DETECTION_NODE_TYPE:
        """
        :param frame: A numpy array of shape (height, width, 3)
        :param detection_node: None
        :param options: Something like {"threshold": 0.5}, it's defined in capsule.
        :param state: Ingnore this
        :return:
        """
        # We have already implemented the batch inference function for a TensorFlow
        # object detector using TensorFlow's API. So here we will just send the frame
        # to BrainFrame through send_to_batch() function. This function will return a
        # queue. Once BrainFrame got the frames, it will process the use the batch_process
        # function and write the results to the queue.
        prediction_output_queue = self.send_to_batch(frame)
        # Get the predictions when they are ready.
        predictions = prediction_output_queue.get()
        detection_node = []
        # Iterate through all the predictions we got in this frame.
        for prediction in predictions:
            # Filter out detections that is not a face.
            if prediction.name != "face":
                continue
            # Filter out detection with low confidence.
            if prediction.confidence < options["threshold"]:
                continue
            # Create a DetectionNode with the prediction, it will be reused by other capsules
            # if those capsules require a face DetectionNode as input type. For example, an age
            # classifier.
            new_detection = DetectionNode(
                name=prediction.name,
                # convert [x1, y1, x2, y2] to [[x1,y1], [x1, y2]...]
                coords=rect_to_coords(prediction.rect),
                extra_data={"detection_confidence": prediction.confidence}
            )
            detection_node.append(new_detection)
        return detection_node


# Define the Capsule class
class Capsule(BaseCapsule):
    # Metadata of this capsule
    name = "face_detector"
    description = "This is an example of how to wrap a TensorFlow Object Detection API Model"
    version = 1
    # Define the input type, since this is an object detector, and doesn't
    # require any input from other capsules, the input type is a NodeDescription
    # with size None.
    input_type = NodeDescription(size=NodeDescription.Size.NONE)
    # Define the output time, in this case, we are going to return a list of
    # bounding boxes so the output type would be size ALL.
    # The type of detection will be face, and we will have the confidence in
    # extra data.
    output_type = NodeDescription(
        size=NodeDescription.Size.ALL,
        detections=["face"],
        extra_data=["detection_confidence"]
    )
    # Define the backend_loader
    backend_loader = lambda capsule_files, device: Backend(
        device=device,
        model_bytes=capsule_files["detector.pb"],
        metadata_bytes=capsule_files["dataset_metadata.json"])
    # The options of this capsule, in the example, we allow the user to set the threshold
    # of the min detection confidence in BrainFrame client or from REST API.
    options = {
        "threshold": FloatOption(
            description="Filter out bad detections",
            default=0.5,
            min_val=0.0,
            max_val=1.0,
        )
    }
