import json


def read_report(file_path, last_line, num_lines):
    """
    read the next num_lines from a file.

lines <class 'str'> 0,0,94,21,97,36.2,normal
    :param file_path: path to the file
    :param last_line: last line read
    :param num_lines: number of lines to read

    :returns: a list of read lines
    """

    with open(file_path) as myfile: # sol
        lines = myfile.readlines()[last_line:last_line+num_lines] # sol

    return lines # sol



def line_to_json(line):
    """
    transforms a line with vital signs into a json.

    :param line: comma separated string with a row of vital signs dataset

    :returns: a json formatted string
    """

    # nota: recuerde que las columnas son
    # idx ,time (s), hr (bpm), resp (bpm), spo2 (%),temp (*c),output

    keys = ['idx', 'time', 'hr', 'resp', 'spo2', 'temp', 'output']

    return json.dumps({
        k: v
        for k,v in zip(keys,line.split(','))
    })


    

