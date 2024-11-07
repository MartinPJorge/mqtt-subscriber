import pyshark
import sys
import json
import numpy as np
import os

# python3 correct_temp_subs.py X pcap-path solution-path 

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

        if pkt[l]._all_fields['mqtt.msgtype'] == '3': # SUBSCRIBE REQUEST
            subs_req_qos = int(pkt[l]._all_fields['mqtt.qos'])


        #print(pkt['TCP']._all_fields['tcp.dstport'], pkt['TCP']._all_fields['tcp.srcport'])
        if pkt[l]._all_fields['mqtt.msgtype'] == '3' and pkt['TCP']._all_fields['tcp.dstport']=="1883": # PUBLISH->broker
            client_port = int(pkt['TCP']._all_fields['tcp.srcport'])
        elif pkt[l]._all_fields['mqtt.msgtype'] == '3' and pkt['TCP']._all_fields['tcp.srcport']=="1883": # PUBLISH->subscriber
            subs_port = int(pkt['TCP']._all_fields['tcp.dstport'])


print(int( int(respuestas['reqtype'])==8) )
print(int( int(respuestas['subsqos'])==subs_req_qos) )
print(int( int(respuestas['pubport'])==client_port) )
print(int( int(respuestas['subport'])==subs_port) )



