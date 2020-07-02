# Import necessary libraries
from pathlib import Path
import itchat as wechat
from brainframe.api import BrainFrameAPI, bf_codecs

# Initialize the API and connect to the server
api = BrainFrameAPI("http://localhost")

# Login to your WeChat account and send a message to the filehelper
wechat.auto_login()
wechat.send_msg(f"Notifications from BrainFrame have been enabled",
                toUserName="filehelper")

# Upload the local file to the BrainFrame server's database and get its storage
# ID
storage_id = api.new_storage(
    data=Path("../videos/shopping_cashier_gone.mp4").read_bytes(),
    mime_type="application/octet-stream"
)

# Create a StreamConfiguration with the storage ID
new_stream_config = bf_codecs.StreamConfiguration(
    # The display name on the client side
    name="Demo",
    # Specify that we're using a file
    connection_type=bf_codecs.ConnType.FILE,
    connection_options={
        # The storage id of the file
        "storage_id": storage_id,
    },
    runtime_options={},
    premises_id=None,
)

# Send the StreamConfiguration to the server to have it connect
new_stream_config = api.set_stream_configuration(new_stream_config)

# Tell the server to start analysis on the new stream
api.start_analyzing(new_stream_config.id)

# Condition for the Alarm that will trigger when there is <1 person in the zone
# that it is assigned to
no_cashier_alarm_condition = bf_codecs.ZoneAlarmCountCondition(
    test=bf_codecs.CountConditionTestType.LESS_THAN,
    check_value=1,
    with_class_name="person",
    with_attribute=None,
    window_duration=5.0,
    window_threshold=0.5,
    intersection_point=bf_codecs.IntersectionPointType.BOTTOM,
)

# Create the ZoneAlarm. It will be active all day, everyday and will be
# triggered if the detection results satisfy the condition we created. Because
# use_active_time==False, the active end/start times will be ignored.
no_cashier_alarm = bf_codecs.ZoneAlarm(
    name="Missing Cashier!",
    count_conditions=[no_cashier_alarm_condition],
    rate_conditions=[],
    use_active_time=False,
    active_start_time="00:00:00",
    active_end_time="23:59:59",
)

# Create a Zone object with the above alarm
cashier_zone = bf_codecs.Zone(
    name="Cashier",
    stream_id=new_stream_config.id,
    alarms=[no_cashier_alarm],
    coords=[[513, 695], [223, 659], [265, 340], [513, 280], [578, 462]]
)

# Send the Zone to BrainFrame
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
                if alert.end_time is None:
                    continue

                total_time = alert.end_time - alert.start_time
                # Check if the alert lasted for more than 5 seconds
                if total_time > 5:
                    alarm = api.get_zone_alarm(alert.alarm_id)
                    wechat.send_msg(
                        f"BrainFrame Alert: {alarm.name} \n"
                        f"Duration {total_time}", toUserName="filehelper")

                    # Log out your WeChat account
                    wechat.logout()

                    # Stop here, for demo purposes
                    exit()
