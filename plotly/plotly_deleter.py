import plotly
import plotly.plotly as py

import json
import requests
from requests.auth import HTTPBasicAuth

username = 'enviro_scale' # Replace with YOUR USERNAME
api_key = 'xxjrfn3fqa' # Replace with YOUR API KEY

auth = HTTPBasicAuth(username, api_key)
headers = {'Plotly-Client-Platform': 'python'}

#plotly.tools.set_credentials_file(username=username, api_key=api_key)

fid = username+':15'
requests.post('https://api.plot.ly/v2/files/'+fid+'/trash', auth=auth, headers=headers)

fid = username+':13'
requests.post('https://api.plot.ly/v2/files/'+fid+'/trash', auth=auth, headers=headers)


fid = username+':19'
requests.post('https://api.plot.ly/v2/files/'+fid+'/trash', auth=auth, headers=headers)
