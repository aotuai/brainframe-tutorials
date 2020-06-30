# Import necessary libraries
from pathlib import Path
import cv2
from brainframe.api import BrainFrameAPI

# Initialize the API and connect to the server
api = BrainFrameAPI("http://localhost")

# Get the names of existing capsules
loaded_capsules = api.get_plugins()
loaded_capsules_names = [capsule.name for capsule in loaded_capsules]

# Print out the capsules names
print("Loaded Capsules: ", loaded_capsules)

IMAGE_ARCHIVE = Path("../images")

# Iterate through all image in the directory
for image_path in IMAGE_ARCHIVE.iterdir():
    # Get the image array
    image_array = cv2.read(str(image_path))
    # Do inference on the image and get the results
    detections = api.process_image(
        # Image array
        img_bgr=image_array,
        # The plugin names to enable while processing the image
        plugin_names=["detector_people_vehicles_fast"],
        # The plugin options you want to set. You can check the available plugin
        # options with the client. Or in the code above, print capsule metadata
        # instead of just the names.
        option_vals={
            "detector_people_vehicles_fast": {
                "filter_mode": "Only Animals",
            }
        }
    )

    print(f"Processed image {image_path.name} and got"
          f" {detections}")

    # Filter out the cat detection by the class name
    cat_detections = [detection for detection
                      in detections if detection.class_name == "cat"]

    if len(cat_detections) > 0:
        print(f"\n\nThis image contains {len(cat_detections)} cats\n\n")
