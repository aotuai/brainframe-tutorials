# import necessary libraries
from brainframe.api import BrainFrameAPI
import itchat as wechat

# initialize the API and connect to the server
api = BrainFrameAPI("http://localhost")

# login to your WeChat account and send a message to the filehelper
wechat.auto_login()
wechat.send_msg(f"Notifications from BrainFrame have been enabled", toUserName="filehelper")

# get the one single zone status and print out
zone_status = api.get_latest_zone_statuses()
print("Zone Status: ", zone_status)

# get the zone status iterator
zone_status_iterator = api.get_zone_status_stream()

# iterate through the zone status packets
for zone_status_packet in zone_status_iterator:
    for stream_id, zone_statuses in zone_status_packet.items():
        for zone_name, zone_status in zone_statuses.items():
            for alert in zone_status.alerts:
                # check if the alert has ended
                if alert.end_time is not None:
                    total_time = alert.end_time - alert.start_time
                    # check if the alert lasts for more than 5 seconds
                    if total_time > 5:
                        wechat.send_msg(f"BrainFrame Alert: {alert.name} Duration {total_time}")

# logout your WeChat account
wechat.logout()
