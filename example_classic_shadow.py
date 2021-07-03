import sys
import json
import config
import logging
import threading
from time import sleep
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from aws.iotcore.classicshadowupdater import AWSIoTMQTTShadow


class Tasks:

    def __init__(self, log_path: str, log_enabled: bool = False):

        # Set up logger
        self.log_enabled = log_enabled
        self.log_format = '%(asctime)s %(levelname)s [MODULE] %(module)s [FUNCTION] %(funcName)s - %(message)s'
        self.date_format = '%Y-%m-%d %H:%M:%S'
        # Backup for 2 months
        self.log_handler = TimedRotatingFileHandler(
            log_path, when="H", interval=2, backupCount=720)
        self.log_handler.setFormatter(logging.Formatter(
            self.log_format, datefmt=self.date_format))
        self.logger_name = "main_logger" if self.log_enabled else ""
        self.logger = logging.getLogger(self.logger_name)
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.INFO)
        self.logger.info(f'{"-"*200}')

        # set up AWS MQTT communication
        self.aws_iot_shadow = AWSIoTMQTTShadow(
            endpoint=config.AWS_HOST,
            port=config.PORT,
            client_id=config.CLIENT_ID,
            certificate=config.AWS_CLIENT_CERT,
            private_key=config.AWS_PRIVATE_KEY,
            root_ca=config.AWS_ROOT_CA,
            thing_name=config.THING_NAME,
            topic=config.TOPIC,
            logger=self.logger_name)

        self.run()

    def update_shadow_data(self) -> None:
        while True:
            try:
                data = {}

                with open('dummy_data.json', 'r') as file:
                    data = json.load(file)

                data["logtime"] = int(datetime.now().timestamp())
                data["ttl"] = int(data["logtime"] + config.TTL)
                self.aws_iot_shadow.update_shadow(data)

            except Exception as e:
                self.logger.warning(f"{type(e).__name__}: {e}")

            finally:
                sleep(config.UPDATE_INTERVAL)

    def run(self) -> None:
        threading.Thread(target=self.update_shadow_data, daemon=True).start()

        while True:
            try:
                sleep(config.UPDATE_INTERVAL)

            except KeyboardInterrupt:
                self.logger.info(
                    "Process interrupted by KeyboardInterrupt. Exiting...")
                # self.aws_mqtt.end_connection()
                sys.exit(1)

            except Exception as e:
                self.logger.warning(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    # period of API call interval in seconds
    tasks = Tasks(log_path="logs/log", log_enabled=True)
