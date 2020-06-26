# Import necessary libraries
import itchat as wechat
from pathlib import Path
from brainframe.api import BrainFrameAPI, bf_codecs

# Initialize the API and connect to the server
api = BrainFrameAPI("http://localhost")

# Login to your WeChat account and send a message to the filehelper
wechat.auto_login()
wechat.send_msg(f"Notifications from BrainFrame have been enabled",
                toUserName="filehelper")

# Upload the local file to the database and create a storage id
storage_id = api.new_storage(
    data=Path("../videos/shopping_cashier_gone.mp4").read_bytes(),
    mime_type="application/octet-stream"
)

# Create a Stream Configuration with the storage id
new_stream_config = bf_codecs.StreamConfiguration(
    # The display name on the client side
    name="Demo",
    # Type of the stream, for now we support ip cameras, web cams and video file
    connection_type=bf_codecs.ConnType.FILE,
    # The storage id of the file
    connection_options={
        "storage_id": storage_id,
    },
    runtime_options={},
    premises_id=None,
)

# Tell the server to connect to that stream configuration
new_stream_config = api.set_stream_configuration(new_stream_config)

# Tell the server to start analyzing the stream you just set
api.start_analyzing(new_stream_config.id)

# The trigger condition of the alarm
# The condition is less than 1 person in the zone.
no_cashier_alarm_condition = bf_codecs.ZoneAlarmCountCondition(
    test=bf_codecs.CountConditionTestType.LESS_THAN,
    check_value=1,
    with_class_name="person",
    with_attribute=None,
    window_duration=5.0,
    window_threshold=0.5,
    intersection_point=bf_codecs.IntersectionPointType.BOTTOM,
)

# Create a Zone Alarm
# This alarm is active from 00:00:00 to 12:00:00 everyday, and will be triggered
# if the detection results matches the above condition.
no_cashier_alarm = bf_codecs.ZoneAlarm(
    name="No Cashier Here!",
    count_conditions=[no_cashier_alarm_condition],
    rate_conditions=[],
    use_active_time=False,
    active_start_time="00:00:00",
    active_end_time="12:00:00"
)

# Create a Zone object with the above alarm
cashier_zone = bf_codecs.Zone(
    name="Cashier",
    stream_id=new_stream_config.id,
    alarms=[no_cashier_alarm],
    coords=[[513, 695], [223, 659], [265, 340], [513, 280], [578, 462]]
)

# Tell BrainFrame to create the Zone
api.set_zone(cashier_zone)

# Get the one single zone status and print out, mostly likely you will get
# nothing here because the stream just started, no results are coming out yet.
zone_status = api.get_latest_zone_statuses()
print("Zone Status: ", zone_status)

# Get the zone status iterator
zone_status_iterator = api.get_zone_status_stream()

keep_looping = True

# Iterate through the zone status packets
for zone_status_packet in zone_status_iterator:
    for stream_id, zone_statuses in zone_status_packet.items():
        for zone_name, zone_status in zone_statuses.items():
            for alert in zone_status.alerts:
                # Check if the alert has ended
                if alert.end_time is not None:
                    total_time = alert.end_time - alert.start_time
                    # Check if the alert lasts for more than 5 seconds
                    if total_time > 5:
                        alarm = api.get_zone_alarm(alert.alarm_id)
                        wechat.send_msg(
                            f"BrainFrame Alert: {alarm.name} "
                            f"Duration {total_time}", toUserName="filehelper")
                        keep_looping = False
    if not keep_looping:
        break

# Logout your WeChat account
wechat.logout()
