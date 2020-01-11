import requests
import configparser

def download_data(sensor_id):
    config = configparser.RawConfigParser()
    config.read('../resources/misc.properties')
    mbp_ip = config.get('MBP', 'mbp.ip')
    user = config.get('MBP', 'mbp.user')
    password = config.get('MBP', 'mbp.password')
    response = requests.get('http://'+ mbp_ip+ '/MBP/api/sensors/'+ sensor_id+'/valueLogs?size=20&sort=time,desc',auth=(user, password))
    data = response.json()
    json = data['content']
    for x in json:
        print(x['value'])
        print('\n\n')


download_data('5de657692ee0a13064c8a56b')