# AWS IoT Core

Wrapper module for `awsiotsdk`

## Setup

1. Create `.env` file and store AWS IoT Core connection config

    ```none
    # Sensor node update interval to cloud, measured in seconds
    UPDATE_INTERVAL=30
    ENDPOINT="some_id.iot.aws_region.amazonaws.com"
    ROOT_CA="AmazonRootCA1.pem"
    CLIENT_CERT="12345abcde-certificate.pem.crt"
    PRIVATE_KEY="12345abcde-private.pem.key"
    CLIENT_ID="arn:aws:iot:aws_region:accound_id:thing/thing_name"
    TOPIC="my/topic"
    PORT=8883
    ```

2. Create `certs` folder at project root and store RootCA, client certificate, and private key


## Usage

```python
from pathlib import Path
from dotenv import dotenv_values
from iotcore import AWSIoTMQTTPubSub

config = dotenv_values(".env")

if __name__ == "__main__":
    cert_path = Path.joinpath(Path.cwd(), "certs")

    aws_mqtt = AWSIoTMQTTPubSub(
        endpoint=config["ENDPOINT"],
        port=config["PORT"],
        client_id=config["CLIENT_ID"],
        certificate=str(Path.joinpath(cert_path, config["CLIENT_CERT"])),
        private_key=str(Path.joinpath(cert_path, config["PRIVATE_KEY"])),
        root_ca=str(Path.joinpath(cert_path, config["ROOT_CA"])),
        topic=config["TOPIC"],
        debug=True)

    data = {
        "param1": 12,
        "param2": 23,
        "param3": 34
    }

    aws_mqtt.publish_message(data)
    aws_mqtt.end_connection()
```