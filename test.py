import configparser

config = configparser.ConfigParser()

config.read('config/data.ini')
for key in config['User']:
    print(config['User'][key])
