import pyshark
import sys
import json
import numpy as np
import os

# python3 correct_alert.py X pcap-path solution-path 

X = int(sys.argv[1])
pcap_path = sys.argv[2]

# Open saved trace file 
cap = pyshark.FileCapture(pcap_path)

# Open solution file
solution_path = sys.argv[3]
with open(solution_path, 'r') as f:
    respuestas = json.load(f)



ok = 0
dups = []
temps = []
subs_req_qos = None
client_port = None
subs_port = None

topics = []
puback_topic = ''
alerts = 0
alert_qos = 0

for pkt in cap:
    time = pkt.frame_info._all_fields['frame.time_relative']
    # frame.time_relative

    if pkt.highest_layer != 'MQTT':
        continue

    # print(pkt['TCP']._all_fields)
    # print(len(pkt['TCP']._all_fields['tcp.payload'].split(':')))
    # print(pkt['TCP']._all_fields['tcp.pdu.size'])
    # print([k for k in pkt])

    # It may happen several MQTT headers are stacked inside one TCP payload
    for l,k in enumerate(pkt):
        if 'mqtt.msgtype' not in pkt[l]._all_fields:
            continue



        if pkt[l]._all_fields['mqtt.msgtype'] == '3': # PUBLISH
            alerts += int(pkt[l]._all_fields['mqtt.topic']=='vitals/alert')
            alert_qos = int(pkt[l]._all_fields['mqtt.qos'])


print(int(alerts==respuestas['numalerts']))
print(int(alert_qos==respuestas['qosalerts']))



