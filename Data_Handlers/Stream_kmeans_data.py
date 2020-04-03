import pandas as pd
import random
import numpy as np
import requests
import configparser

def get_data(sensor_id,size):

    config = configparser.RawConfigParser()
    config.read('resources/misc.properties')
    mbp_ip = config.get('MBP', 'mbp.ip')
    user = config.get('MBP', 'mbp.user')
    password = config.get('MBP', 'mbp.password')
    response = requests.get(
        'http://' + mbp_ip + '/MBP/api/sensors/' + sensor_id + '/valueLogs?size=' + str(size) + '&sort=time,desc',
        auth=(user, password))
    sensor_data = response.json()
    data = []
    json = sensor_data['content']
    for x in json:
        # print(x['value'])
        row = x['value'].split(',')
        temp = []
        for value in row:
            temp.append(float(value.split(':')[1]))
        data.append(temp)
    return np.array(data)

