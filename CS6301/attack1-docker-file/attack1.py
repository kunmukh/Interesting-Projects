import time
import requests
import os


ip =os.environ.get('IP')

url = f'http://{ip}:30030/api/audiomixer/volume'
val = {'control': 'Master'}
x = requests.post(url, json=val)
print(x.text)


t = 0
while (True):
	for t in range(0, 100, 5):
		val1 = {'control':'Master', 'value':f'{t/100}'}
		x1 = requests.post(url, json=val1)
		print(x1.text)
		time.sleep(0.5)

