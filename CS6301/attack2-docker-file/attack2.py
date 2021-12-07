import time
import requests
import os


ip =os.environ.get('IP')


url = f'http://{ip}:30031/api/hvac/get_fanspeed'
x = requests.post(url)
print(x.text)

url = f'http://{ip}:30031/api/hvac/set'
val = {'FanSpeed': 85}
x = requests.post(url, json=val)
print(x.text)

url = f'http://{ip}:30031/api/hvac/get_fanspeed'
x = requests.post(url)
print(x.text)


