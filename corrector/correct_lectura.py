import json
import utils_sol as u
import sys

# usage correct_lectura.py X respuestasJSON
X = int(sys.argv[1])

respuestas = None
with open(sys.argv[2], 'r') as f:
    respuestas = json.load(f)


read_dict = json.loads(u.line_to_json(u.read_report('Human_vital_signs_R.csv', X+2,1)[0]))
# reads: {'idx': '0', 'time': '0', 'hr': '94', 'resp': '21', 'spo2': '97', 'temp': '36.2', 'output': 'Normal\n'}
#print(read_dict)

num_cols_ok = len(respuestas['lectura'].keys()) / len(read_dict.keys())
#print(num_cols_ok)

#print(respuestas['lectura'])

num_vals_ok = 0
lectura_lower_case_keys = [k.lower() for k in respuestas['lectura']]
#print(lectura_lower_case_keys)
for k,v in read_dict.items():
    num_vals_ok += 1 if k in lectura_lower_case_keys else 0
num_vals_ok /= len(read_dict.keys())
#print(num_vals_ok)


print((num_cols_ok+num_vals_ok)/2)





