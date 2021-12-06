import time
import requests

url = 'http://192.168.1.153:30031/api/hvac/get_fanspeed'
x = requests.post(url)
print(x.text)

url = 'http://192.168.1.153:30031/api/hvac/set'
val = {'FanSpeed': 85}
x = requests.post(url, json=val)
print(x.text)

url = 'http://192.168.1.153:30031/api/hvac/get_fanspeed'
x = requests.post(url)
print(x.text)


