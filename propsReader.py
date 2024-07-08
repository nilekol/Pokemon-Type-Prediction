import configparser

config = configparser.ConfigParser()

config.read('db.ini')

user = config['main']['username']
passwd = config['main']['password']

print("hello")


