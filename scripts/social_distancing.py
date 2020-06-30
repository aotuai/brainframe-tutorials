# Import the dependencies
import math
from argparse import ArgumentParser
from brainframe.api import BrainFrameAPI, bf_codecs


# Help function to check if two detection is overlapped
def check_overlap(det1: bf_codecs.Detection,
                  det2: bf_codecs.Detection) -> bool:
    """
    :param det1: First bbox detection
    :param det2: Second bbox detection
    :return: If the two detections' bbox is overlapped
    """

    # Sort the x, y in ascending order
    coords1_sorted_x = sorted([c[0] for c in det1.coords])
    coords2_sorted_x = sorted([c[0] for c in det2.coords])
    coords1_sorted_y = sorted([c[1] for c in det1.coords])
    coords2_sorted_y = sorted([c[1] for c in det2.coords])

    # Return false if one rect is on the left side of the other
    if coords1_sorted_x[0] > coords2_sorted_x[-1] or \
            coords2_sorted_x[0] > coords1_sorted_x[-1]:
        return False

    # Return false if one rect is on the top side of the other
    if coords1_sorted_y[0] > coords2_sorted_y[-1] or \
            coords2_sorted_y[0] > coords1_sorted_y[-1]:
        return False

    # Other wise return True
    return True


# Help function to calculate the distance between the center point of two
# detections
def get_distance(det1: bf_codecs.Detection,
                 det2: bf_codecs.Detection) -> float:
    """
    :param det1: First bbox detection
    :param det2: First bbox detection
    :return: Distance between the center of these two detections
    """
    return math.sqrt((det1.center[0] - det2.center[0]) ** 2 +
                     (det1.center[1] - det2.center[1]) ** 2)


def social_distancing(min_distance: int):
    """
    :param min_distance: The minimum distance between two people
    :return:
    """
    # Initialize the API
    api = BrainFrameAPI("http://localhost")
    assert len(api.get_stream_configurations()), \
        "There should be at least one stream already configured!"
    # Get the inference stream.
    for zone_status_packet in api.get_zone_status_stream():
        # Organize detections results as a dictionary of
        # {stream_id: [Detections]}.
        detections_per_stream = {
            stream_id: zone_status.within
            for stream_id, zone_statuses in zone_status_packet.items()
            for zone_name, zone_status in zone_statuses.items()
            if zone_name == "Screen"
        }

        # Iterate over each stream_id, detections combination
        for stream_id, detections in detections_per_stream.items():
            # If there are less than one person in the stream, you are safe.
            if len(detections) <= 0:
                pass
            # Compare the distance between each detections.
            for i in range(0, len(detections)):
                current_detection = detections[i]
                violating = False
                for j in range(i + 1, len(detections)):
                    target_detection = detections[j]
                    # If the bbox representing two people are overlapped, the
                    # distance is 0, otherwise it's the distance between the
                    # center of these two bbox.
                    distance = 0 if check_overlap(current_detection,
                                                  target_detection) \
                        else get_distance(current_detection, target_detection)
                    if distance < min_distance:
                        print(f"Some people violating social distancing rule, "
                              f"current distance: {distance}")
                        violating = True
                        break
                if violating:
                    break


def main():
    parser = ArgumentParser()
    parser.add_argument("--min-distance", type=int, default=100,
                        help="The min distance allowed between two people")
    args = parser.parse_args()
    social_distancing(args.min_distance)


if __name__ == "main":
    main()
