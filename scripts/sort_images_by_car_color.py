# Import necessary libraries
from pathlib import Path
import shutil

import cv2

from brainframe.api import BrainFrameAPI

# Initialize the API and connect to the server
api = BrainFrameAPI("http://localhost")

# Get the names of existing capsules
loaded_capsules = api.get_capsules()
loaded_capsules_names = [capsule.name for capsule in loaded_capsules]

# Print out the capsules names
print(f"Loaded Capsules: {loaded_capsules_names}")

# Root directory containing the images.
IMAGE_ARCHIVE = Path("../images/cars")

# Iterate through all images in the directory
for image_path in IMAGE_ARCHIVE.iterdir():
    # Use only PNGs and JPGs
    if image_path.suffix not in [".png", ".jpg"]:
        continue

    # Get the image array
    image_array = cv2.imread(str(image_path))

    # Perform inference on the image and get the results
    detections = api.process_image(
        # Image array
        img_bgr=image_array,
        # The names of capsules to enable while processing the image
        capsule_names=["classifier_vehicle_color_openvino",
                       "detector_person_vehicle_bike_openvino"],
        # The capsule options you want to set. You can check the available
        # capsule options with the client. Or in the code snippet above that
        # printed capsule names, also print the capsule metadata.
        option_vals={}
    )

    print()
    print(f"Processed image {image_path.name} and got {detections}")

    car_detections = [detection for detection in detections if
                      detection.class_name == "vehicle"]

    if len(car_detections) != 1:
        print("No car or more and one car detected in this image, skip.")
        continue

    color = car_detections[0].attributes["color"]
    color_folder = IMAGE_ARCHIVE / color

    if not color_folder.exists():
        color_folder.mkdir()

    shutil.copy(str(image_path), str(color_folder))





