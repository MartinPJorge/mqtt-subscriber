import pyshark
import sys
import json
import numpy as np
import os

# python3 correct_publishes.py X pcap-path solution-path 

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
            # print('A publish')
            # print(pkt[l]._all_fields)

            # Store the duplicate Message Idx
            if pkt[l]._all_fields['mqtt.topic'] in ['vitals/temp', 'vitals/TEMP']:
                # Get the PUBLISH payload as string
                # https://stackoverflow.com/a/66073701
                hex_string = str(pkt[l]._all_fields['mqtt.msg'])
                hex_split = hex_string.split(':')
                hex_as_chars = map(lambda hex: chr(int(hex, 16)), hex_split)
                human_readable = ''.join(hex_as_chars)

                # skip reported column header
                if 'TEMP (*C)' in human_readable:
                    continue

                if human_readable[0] == '{': # it is a JSON
                    temp_dict = json.loads(human_readable)
                    temp = temp_dict['TEMP'] if 'TEMP' in temp_dict.keys()\
                        else temp_dict['temp']
                else:
                    temp = float(human_readable)

                temps += [temp]

# In case no temperature report is found fill with negative
if len(temps) < 1:
    temps = [-200000]

print(int(max(temps) == respuestas['maxtemp']))


