import configparser
config = configparser.RawConfigParser()
config.read('../resources/misc.properties')

print (config.get('MBP', 'database.dbname'))
