# Before Starting
Python version 2.7.3
## Dependencies
* bitstruct  
* json  
* paho-mqtt  
To install a python package via pip:  

> > > > > > > pip install paho-mqtt

## Description

publish_script.py is the main script to decode the data sent from raspberry Pi to the intermediate server and send it to iqueue. To test that it works without running the setup, the script "dummy_data_send.py" is written to send dummy data every 3 seconds to topic "paho/test/iotBUET/bulk_raw/" (host: "iot.eclipse.org"). Running the script "final_subscriber.py" shows all the iqueue publishers' data.

