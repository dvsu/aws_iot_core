# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import json
import logging
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder


class AWSMQTT:

    def __init__(self, endpoint: str, port: int, client_id: str, certificate: str, private_key: str, root_ca: str, topic: str, logger=None):
        self.logger = None
        if logger:
            self.logger = logging.getLogger(logger)
        self.endpoint = endpoint
        self.client_id = client_id
        self.topic = topic
        self.root_ca = root_ca
        self.certificate = certificate
        self.private_key = private_key
        self.port = port

        self.event_loop_group = io.EventLoopGroup(1)
        self.host_resolver = io.DefaultHostResolver(self.event_loop_group)
        self.client_bootstrap = io.ClientBootstrap(
            self.event_loop_group, self.host_resolver)
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.endpoint,
            port=self.port,
            cert_filepath=self.certificate,
            pri_key_filepath=self.private_key,
            client_bootstrap=self.client_bootstrap,
            ca_filepath=self.root_ca,
            client_id=self.client_id,
            clean_session=False,
            keep_alive_secs=6)

        self.initializing_connection()

    def initializing_connection(self):
        self.logger.info(
            f"Connecting to endpoint {self.endpoint} with client ID '{self.client_id}'...")
        try:
            connect_future = self.mqtt_connection.connect()
            result = connect_future.result()
            self.logger.info("Connection successful!")

        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Failed to connect to endpoint {self.endpoint} with client ID '{self.client_id}'\n{type(e).__name__}: {e}")
            else:
                print(
                    f"Failed to connect to endpoint {self.endpoint} with client ID '{self.client_id}'\n{type(e).__name__}: {e}")

    def publish_message(self, message):
        try:
            self.mqtt_connection.publish(topic=self.topic, payload=json.dumps(
                message), qos=mqtt.QoS.AT_LEAST_ONCE)

        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Failed to publish message to topic '{self.topic}'\n{type(e).__name__}: {e}")
            else:
                print(
                    f"Failed to publish message to topic '{self.topic}'\n{type(e).__name__}: {e}")

    def end_connection(self):
        self.logger.info(f"Ending connection to endpoint {self.endpoint}...")

        try:
            disconnect_future = self.mqtt_connection.disconnect()
            disconnect_future.result()
            self.logger.info(
                f"Connection to endpoint '{self.endpoint}' has been disconnected")

        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Failed to disconnect from endpoint {self.endpoint}\n{type(e).__name__}: {e}")
            else:
                print(
                    f"Failed to disconnect from endpoint {self.endpoint}\n{type(e).__name__}: {e}")
