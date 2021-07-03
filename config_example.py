####################### WiFi Configuration #####################
NETWORK_CONFIG = [
    {
        "ssid": "myssid1", 
        "pass": "strongpassword"
    },
    {
        "ssid": "mybackupssid", 
        "pass": "superstrongpassword"
    }
]

################### Basic Device Configuration #################

# Device name/ identifier
DEVICE_NAME = "thisdevicename"

# Sensor node update interval to cloud, measured in seconds
UPDATE_INTERVAL = 30


#################### AWS IoT MQTT Configuration #################

# AWS general configuration
AWS_HOST = 'xxxxxxxxx-xxx.iot.xxxxxxx.amazonaws.com'
AWS_ROOT_CA = 'cert/root-CA.crt'
AWS_CLIENT_CERT = 'cert/xxxxxxxxxx-certificate.pem.crt'
AWS_PRIVATE_KEY = 'cert/xxxxxxxxxx-private.pem.key'

# Subscribe / Publish Client
CLIENT_ID = 'arn:aws:iot:cxxxxxxxxxx:xxxxxxxxxxxx:thing/xxxxxxxxxx'
TOPIC = 'xxxxxxxxxxx'
PORT = 8883

####################### DynamoDB Config ########################

# Time to live of sensor data in DynamoDB
TTL = 900 # 15 minutes