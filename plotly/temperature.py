import plotly
#plotly.__version__
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
# (*) Import module keep track and format current time
import datetime
import time

stream_id = {}
#stream_ids = ["2m6f6eq1bo", "qexgcccyuy", "kd4s18sz34", "kmunx5u0g8", "tjhuxxhfui", "vdec67rhyu"]
stream_obj = {}
trace = {}
s = {}

plotly.tools.set_credentials_file(username='enviro_scale', api_key='xxjrfn3fqa')
##use it to import credentials
stream_ids = tls.get_credentials_file()['stream_ids']
print stream_ids

def map_sensor_id_to_title(x):
    return {
        0 : "CH4 Concentration",
        1 : "LPG Concentration",
        2 : "CO2 Concentration",
        3 : "Dust Concentration",
        4 : "Temperature (degree C)",
        5 : "Humidity (%)",
    }.get(x, "none")    # "none" is default if x not found



# Get stream id from stream id list
i = 0
stream_id[i] = stream_ids[i]

# Make instance of stream id object
stream_obj[i] = go.Stream(
    token=stream_id[i],  # link stream id to 'token' key
    maxpoints=80      # keep a max of 80 pts on screen
)

# Initialize trace of streaming plot by embedding the unique stream_id
trace[i] = go.Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=stream_obj[i]         # (!) embed stream id, 1 per trace
)

data = go.Data([trace[i]])

# Add title to layout object
layout = go.Layout(title=map_sensor_id_to_title(i))

# Make a figure object
fig = go.Figure(data=data, layout=layout)

# Send fig to Plotly, initialize streaming plot, open new tab
py.iplot(fig, filename=map_sensor_id_to_title(i))

# We will provide the stream link object the same token that's associated with the trace we wish to stream to
s[i] = py.Stream(stream_id[i])

s[i].open()

def draw_to_plotly(jsonstr):
    """
    :param sensor_bundle:
    sensor_bundle[0] -> time
    sensor_bundle[1] -> ch4
    sensor_bundle[2] -> lpg
    sensor_bundle[3] -> co2
    sensor_bundle[4] -> dust
    sensor_bundle[5] -> temp
    sensor_bundle[6] -> humidity

    :return: Just draw to our plotly site
    """

    global s
    # We then open a connection

    #s[i].open()
    time.sleep(2)


    # Delay start of stream by 5 sec (time to switch tabs)


    # Current time on x-axis, random numbers on y-axis
    x = datetime.datetime.fromtimestamp(jsonstr["d"]["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
    #datetime.datetime.fromtimestamp(1466257792).strftime('%Y-%m-%d %H:%M:%S')


    y = jsonstr["d"]["value"]

    # Send data to your plot
    s[i].write(dict(x=x, y=y))

    #     Write numbers to stream to append current data on plot,
    #     write lists to overwrite existing data on plot

    #time.sleep(1)  # plot a point every second

    # Close the stream when done plotting
    #s[i].close()












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
    client.subscribe(get_topic_name("temperature"))

def on_message(client, userdata, msg):
    try:
        print ("From topic: " + msg.topic + " , received: ")
        global jsonstr
        jsonstr = json.loads(msg.payload)
        print jsonstr
        print jsonstr["d"]["value"]
        print jsonstr["d"]["timestamp"]
        draw_to_plotly(jsonstr)

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

