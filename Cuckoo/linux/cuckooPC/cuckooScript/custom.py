# Kunal Mukherjee
# cuckoo malware lab
# 9/11/2020


import logging
import os
import subprocess
import time

import json
import sys
import select


from lib.common.abstracts import Auxiliary
from lib.common.results import NetlogFile
from lib.core.config import Config

log = logging.getLogger(__name__)
_delay_time = 10

# put it in $CUCKCOO_HOME/analyzer/linux/modules/auxiliary

def int32(x):
  if type(x) == str:
    x = int(x, 16)

  if x>0xFFFFFFFF:
    raise OverflowError
  if x>0x7FFFFFFF:
    x=int(0x100000000-x)
    if x<2147483648:
      return -x
    else:
      return -2147483648
  return x

class SAGE(Auxiliary):
	"""NEC-Agent ID re-assignment """
	priority = -10 # same priority as stap 

	# copying from stap 
	def __init__(self):
		self.config = Config(cfg="analysis.conf")
		self.proc = None

	def start(self):

		# sync the time first
		process = subprocess.Popen(['sudo', 'systemctl', 'stop', 'ntp'],
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
		time.sleep(_delay_time)
		process = subprocess.Popen(['sudo', 'ntpd', '-gq'],
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
		time.sleep(_delay_time)
		process = subprocess.Popen(['sudo', 'systemctl', 'start', 'ntp'],
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
		log.info("Kunal: Time synced")
		time.sleep(_delay_time)

		# stop the NEC-agent
		process = subprocess.Popen(['sudo', 'systemctl', 'stop', 'NEC-Agent'],
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
		log.info("Kunal: NEC-Agent stopped")
		time.sleep(_delay_time)

		# remove the AgentID
		with open('/opt/NECLA/Agent/run/agent-rt.json', 'r+') as f:
			data = json.load(f)
			oldagentID = data['AgentID']
			data['AgentID'] = ""  # <--- add `id` value.
			f.seek(0)  # <--- should reset file position to the beginning.
			json.dump(data, f, indent=4)
			f.truncate()  # remove remaining part
			f.close()

		log.info("Kunal: Old NEC-Agent ID removed %s" % (oldagentID))
		log.info("Kunal: Old NEC-Agent ID %d" % (int32(str(oldagentID[-8:]))))
		time.sleep(_delay_time)

		# start the NEC-Agent
		process = subprocess.Popen(['sudo', 'systemctl', 'start', 'NEC-Agent'],
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
		# log.info("Kunal: NEC-Agent started")
		time.sleep(_delay_time)

		with open('/opt/NECLA/Agent/run/agent-rt.json', 'r+') as fo:
			data = json.load(fo)
			agentID = data['AgentID']
			while agentID == "":
				log.info("Kunal: NEC-Agent issue while starting")	
				time.sleep(_delay_time)

				# stop the NEC-agent
				process = subprocess.Popen(['sudo', 'systemctl', 'stop', 'NEC-Agent'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				log.info("Kunal: NEC-Agent stopped")			
				time.sleep(_delay_time)
			
				# start the NEC-Agent again
				process = subprocess.Popen(['sudo', 'systemctl', 'start', 'NEC-Agent'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				time.sleep(_delay_time)
				
				f = open('/opt/NECLA/Agent/run/agent-rt.json', 'r')
				data = json.load(f)
				agentID = data['AgentID']
				f.close()
		
		log.info("Kunal: NEC-Agent started")
		time.sleep(_delay_time)

		# print the AgentID
		with open('/opt/NECLA/Agent/run/agent-rt.json', 'r+') as fo:
			data = json.load(fo)
			agentID = data['AgentID']
		log.info("Kunal: New NEC-Agent ID %s" % (agentID))
		log.info("Kunal: New NEC-Agent ID %d" % (int32(str(agentID[-8:]))))
		time.sleep(_delay_time)

		# show the malware that is being run
		filename = [f for f in os.listdir('/tmp/') if ".bin" in f][0]
		log.info("Kunal: malware name %s" % (filename))

		# make the malware executable
		os.system('sudo chmod +x /tmp/'+filename)

		# run the malware and reroute the output to mango.stderr
		os.chdir("/tmp/")
		os.system("script -c './"+ filename +"' >> /home/rider/magic/mango.stderr")
	

	def stop(self):
		with open('/opt/NECLA/Agent/run/agent-rt.json', 'r+') as fo:
			data = json.load(fo)
			agentID = data['AgentID']
		log.info("Kunal: New NEC-Agent ID %s" % (agentID))

		# stop the NEC-agent
		process = subprocess.Popen(['sudo', 'systemctl', 'stop', 'NEC-Agent'],
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)
		log.info("Kunal: NEC-Agent stopped")
		time.sleep(_delay_time)