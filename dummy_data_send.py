import traceback
import Queue
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as pub
from socket import *
from bitstruct import *
import json

HOST_ECLIPSE = "iqueue.ics.uci.edu"

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
            {"name": "temperature",
             "size": 8,
             "dtype": 's'
             },

            {"name": "humidity",
             "size": 8,
             "dtype": 'u'
             },

            {"name": "methane",
             "size": 10,
             "dtype": 'u'
             },

            {"name": "lpg",
             "size": 10,
             "dtype": 'u'
             },

            {"name": "co2",
             "size": 10,
             "dtype": 'u'
             },
            {"name": "lat",
             "size": 32,
             "dtype": 'f'
             },

            {"name": "lon",
             "size": 32,
             "dtype": 'f'
             },

            {"name": "dust",
             "size": 10,
             "dtype": 'u'
             }
        ]
}
sensor_conf = json.dumps(d)
c = json.loads(sensor_conf)


def queue_print(q):
    print "Printing start."
    queue_copy = []
    while True:
        try:
            elem = q.get(block=False)
        except:
            break
        else:
            queue_copy.append(elem)
    for elem in queue_copy:
        q.put(elem)
    for elem in queue_copy:
        print (elem)
    print "Printing end."


def extract_queue_and_encode(self):

    # Part 1: Extracting all elements from queue to "queue_copy"
    queue_copy = []
    i = 0
    while True:
        try:
            elem = self.get(block=False)
        except:
            break
        else:
            queue_copy.append(elem)
            print elem
        i = i + 1
        # to put a boundary on how many elements to pop
        # if i == 8:
        #    break

    # Part 2: Encoding elements in "queue_copy" and return a python "struct" object
    N = len(queue_copy)
    data = []

    fmt_string = "u8"   # number of readings bundled together is assumed to be in range 0-255, hence 8 bits
    data.append(N)

    fmt_string += "f32"  # initial timestamp
    data.append(queue_copy[0][2])

    # append the event ids
    for queue_elem in queue_copy:
        fmt_string += "u4"   # we have provision for maximum 16 sensors, hence 4 bits
        event_id = queue_elem[0]
        data.append(event_id)

    # append the sensor values
    for queue_elem in queue_copy:
        id = queue_elem[0]
        fmt_string += str(c["event"][id]["dtype"]) + str(c["event"][id]["size"])
        data.append(queue_elem[1])

    # append the timestamp offsets
    for queue_elem in queue_copy:
        id = queue_elem[0]
        time_actual = queue_elem[2]
        time_offset = int((time_actual - queue_copy[0][2])*10000)
        print (time_actual - queue_copy[0][2])
        print (time_offset)
        fmt_string += "u16"
        data.append(time_offset)
    packed = pack(fmt_string, *data)
    return packed


def publish_packet_raw(message):
    try:
        msgs = [{'topic': "paho2/test/iotBUET/bulk_raw/", 'payload': message},
                ("paho/test/multiple", "multiple 2", 0, False)]
        pub.multiple(msgs, hostname=HOST_ECLIPSE)
        return True

    except gaierror:
        print ('[MQTT] Publish ERROR.')
        return False


# simulating the queue used in EnviroSCALE pi by sending dummy data
newq = Queue.Queue()
newq.put((0, -32, time.time()))
time.sleep(1)
newq.put((0, 32, time.time()))
time.sleep(1)
newq.put((1, 32, time.time()))
time.sleep(1)
newq.put((2, 32, time.time()))
time.sleep(1)
newq.put((3, 32, time.time()))
time.sleep(1)
newq.put((4, 12, time.time()))
newq.put((5, 23.353, time.time()))

packed = extract_queue_and_encode(newq)
while 1:
    publish_packet_raw(bytearray(packed))



    print "Sent"
    time.sleep(3)