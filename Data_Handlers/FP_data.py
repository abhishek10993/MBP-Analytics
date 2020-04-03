import random
import requests
import configparser
import pandas as pd

def getvalue():
    efficiency = random.choice([94, 98, 65, 78, 88, 41, 32, 54, 56, 81])
    temperature = random.choice([94, 98, 65, 78, 88, 41, 22, 54, 56, 81, 66, 54, 46, 34, 92])
    current = random.choice([94, 98, 65, 78, 88, 41, 22, 54, 56, 81, 66, 54, 46, 34, 92])
    status = random.choice(['1', '2', '3', '4', '5'])
    value = 'temperature:' + str(temperature) + ',' + 'current:' + str(current) + ',' + 'efficiency:' + str(
        efficiency) + ',' + 'status:' + status
    return value

def get_data(sensor_id):
    temp = ''
    config = configparser.RawConfigParser()
    config.read('resources/misc.properties')
    mbp_ip = config.get('MBP', 'mbp.ip')
    user = config.get('MBP', 'mbp.user')
    password = config.get('MBP', 'mbp.password')
    response = requests.get(
        'http://' + mbp_ip + '/MBP/api/sensors/' + sensor_id + '/valueLogs?size=5000&sort=time,desc',
        auth=(user, password))
    data = response.json()
    json = data['content']
    for x in json:
        data = x['value'].split(',')
        print(data)
        for value in data:
            header = value.split(':')[0]
            val = float(value.split(':')[1])
            if val > 90:
                label = header+'_veryhigh'
            elif val > 70:
                label = header+'_high'
            elif val > 50:
                label = header+'_med'
            elif val > 30:
                label = header+'_low'
            else:
                label = str(val)

            temp = temp + label + ' '
        temp = temp + '\n'

    print ('list found')
    filename = 'data.txt'
    f = open(filename, "w+")
    f.write(temp)
    f.close()
    return filename
