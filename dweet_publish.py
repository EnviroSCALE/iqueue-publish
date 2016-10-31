#for web-Dashboard
import requests
import datetime
urlDweetIO = "https://dweet.io/dweet/for/"
myThingName = "iotEnviroSCALE_BUET"

def get_time_str(a_time):
    return datetime.datetime.fromtimestamp(a_time).strftime('%H:%M:%S')


def dweetpublish(jsonstr, urlDweetIO="https://dweet.io/dweet/for/", myThingName="iotEnviroSCALE_BUET"):
    timestamp = get_time_str(jsonstr["d"]["timestamp"])
    lat = str(jsonstr["d"]["geotag"]["lat"])
    lon = str(jsonstr["d"]["geotag"]["lon"])
    value = (jsonstr["d"]["value"])
    mapper={"temperature": "Temparature", "methane": "CH4", "co2":"CO2", "humidity": "Humidity", "lpg": "LPG", "dust":"Dust"}
    eventname = mapper[jsonstr["d"]["event"]]
    # for web-Dashboard
    rqsString = urlDweetIO + myThingName + '?' + 'Time' + '= ' + timestamp + '& ' + eventname + '= ' + "{0:.2f}".format(
        value) + '& Lat' + '= ' + lat + '& Long' + '= ' + lon
    rqs = requests.get(rqsString)
    print(rqsString)



import traceback
import paho.mqtt.client as mqttClient
import json

HOST_IQUEUE = "iqueue.ics.uci.edu"
PIMAC = "74da382afd91"
jsonstr = None

def get_topic_name(event, device_id = "74da382afd91"):
    return "iot-1/d/" + device_id + "/evt/" + event + "/jsonplotly"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(get_topic_name("methane"))
    client.subscribe(get_topic_name("co2"))
    client.subscribe(get_topic_name("temperature"))
    client.subscribe(get_topic_name("humidity"))
    client.subscribe(get_topic_name("dust"))
    client.subscribe(get_topic_name("lpg"))

def on_message(client, userdata, msg):
    try:
        print ("From topic: " + msg.topic + " , received: ")
        global jsonstr
        jsonstr = json.loads(msg.payload)
        print jsonstr
        dweetpublish(jsonstr)

        #print jsonstr

    except:
        traceback.print_exc()
        print ("Error in message.")


#listen for receiving an encoded bundle
client = mqttClient.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST_IQUEUE, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

