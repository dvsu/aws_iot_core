from pathlib import Path
from dotenv import dotenv_values
from pubsub import AWSIoTMQTTPubSub

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
