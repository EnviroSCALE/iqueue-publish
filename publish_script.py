import paho.mqtt.client as mqttClient
import paho.mqtt.publish as pub
from bitstruct import *
import time
import datetime
import traceback
import json


HOST_ECLIPSE = "iot.eclipse.org"
HOST_IQUEUE = "iqueue.ics.uci.edu"


'''
# size : how many bits
# id : index of event in json
# s : signed int
# u : unsigned int
# f : float
'''
d = {
  "event":
  [
    { "name": "temperature",
      "size": 8,
      "dtype": 's'
    },

    { "name": "humidity",
      "size": 8,
      "dtype": 'u'
    },

    { "name" : "methane",
      "size": 10,
      "dtype": 'u'
    },

    { "name" : "lpg",
      "size": 10,
      "dtype": 'u'
    },

    { "name" : "co2",
      "size": 10,
      "dtype": 'u'
    },
    { "name" : "lat",
      "size": 32,
      "dtype": 'f'
    },

    { "name" : "lon",
      "size": 32,
      "dtype": 'f'
    },

    { "name" : "dust",
      "size": 10,
      "dtype": 'u'
    }
  ]
}

sensor_conf = json.dumps(d)
c = json.loads(sensor_conf)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("paho/test/iotBUET/bulk_raw/")


# The callback for when a PUBLISH message is received from the server.
# Sent directly from raspberry pi to iot.eclipse.org
def on_message(client, userdata, msg):
    try:
        #print ("From topic: " + msg.topic + " , received: " + str(msg.payload))
        print ("From topic: " + msg.topic + " , received: ")
        # print (msg.payload)
        unpacked = decode_bitstruct(msg.payload, c)
        print unpacked
        N = unpacked[0]
        initial_time = unpacked[1]

        for i in range(N):
            id = unpacked[i+2]
            value = unpacked[i + N + 2]
            time_offset = unpacked[i + N*2 + 2]
            print ("Publishing now: ", id, value, time_offset)
            time = initial_time + (time_offset/10000.0)
            timestring =  datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S.%f')
            #timestring = time.time()
            publish(HOST_IQUEUE, c["event"][i]["name"], value, timestring)
    except:
        traceback.print_exc()
        print ("Error")



def publish(hostname, event, value,  timestamp, device_id="74da382afd91", prio_class="low", prio_value=10):
    d = {"d:":
            {
                "timestamp": timestamp,
                "event": event,
                "value": value,
                "prio_class": prio_class,
                "prio_value": prio_value,
            }
        }
    jsonstr = json.dumps(d)
    msg = jsonstr

    try:
        # "iot-1/d/801f02da69bc/evt/light/json"
        topic = "iot-1/d/" + device_id + "/evt/" + event + "/json"
        #topic = "paho/test/iotBUET/bulk/"
        msgs = [{'topic': topic, 'payload': msg},
                ("paho/test/multiple", "multiple 2", 0, False)]
        pub.multiple(msgs, hostname=hostname, port=1883)
        return True
    except:
        print ("error")
        traceback.print_exc()
        return False



def decode_bitstruct(packed_bytes, c):

    fmt_decode = "u8f32"    # how many readings ahead 8 bits unsigned, initial timestamp 32 bits float
    N = unpack(fmt_decode, packed_bytes)[0]
    # initial_time = unpack(fmt_decode, packed_bytes)[1]

    # each id is 4 bits
    for i in range(N):
        fmt_decode += "u4"

    unpacked2 = unpack(fmt_decode, packed_bytes)

    list_of_sensor_ids = unpacked2[2:(2+N+1)]
    #list_of_offsets = unpacked2[(2+N):]

    for i in list_of_sensor_ids:
        fmt_decode += str(c["event"][i]["dtype"]) + str(c["event"][i]["size"])
    for i in range(N):
        fmt_decode += "u16"

    unpacked3 = unpack(fmt_decode, packed_bytes)
    return unpacked3


# listen for receiving an encoded bundle
client = mqttClient.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST_ECLIPSE, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()