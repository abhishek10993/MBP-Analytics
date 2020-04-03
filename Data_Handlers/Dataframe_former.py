import requests
import configparser
import pandas as pd
import random
import time

def getvalue():
    efficiency = random.choice([94, 98, 65, 78, 88, 41, 22, 54, 56, 81])
    temperature = random.choice([5.0, 20.0, 18.5, 6.0, 8.0, 12.5, 17.5, 14.0, 10.1, 11.5, 12.9, 15.0])
    current = random.choice([0.0, 20.0, 18.5, 6.0, 8.0, 12.5, 17.5, 14.0, 10.1, 11.5, 12.9, 15.0])
    status = random.choice(['1', '2', '3', '4', '5'])
    value = 'temperature:' + str(temperature) + ',' + 'current:' + str(current) + ',' + 'efficiency:' + str(
        efficiency) + ',' + 'status:' + status
    return value

def download_data(sensor_id):
    config = configparser.RawConfigParser()
    config.read('resources/misc.properties')
    mbp_ip = config.get('MBP', 'mbp.ip')
    user = config.get('MBP', 'mbp.user')
    password = config.get('MBP', 'mbp.password')
    response = requests.get('http://'+ mbp_ip+ '/MBP/api/sensors/'+ sensor_id+'/valueLogs?size=5000&sort=time,desc',auth=(user, password))
    data = response.json()
    headers = []
    df_data = []
    json = data['content']
    for x in json:
        row = x['value'].split(',')
        temp = []
        for value in row:
            if len(headers) < len(row):
                headers.append(value.split(':')[0])
            temp.append(float(value.split(':')[1]))
        df_data.append(temp)

    df = pd.DataFrame(df_data, columns=headers)
    print(df)
    return df
