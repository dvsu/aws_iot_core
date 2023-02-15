import json
import logging
from typing import Any
from dataclasses import asdict
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder


class AWSIoTMQTTPubSub:

    def __init__(self, endpoint: str, port: int,
                 client_id: str, certificate: str,
                 private_key: str, root_ca: str,
                 topic: str, debug=False):
        self.endpoint = endpoint
        self.client_id = client_id
        self.topic = topic
        self.root_ca = root_ca
        self.certificate = certificate
        self.private_key = private_key
        self.port = port
        self.debug = debug

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
        self.self_subscription()

    def initializing_connection(self):
        self.logger.info(
            f"Connecting to endpoint {self.endpoint} with client ID '{self.client_id}'...")
        try:
            connect_future = self.mqtt_connection.connect()
            result = connect_future.result()
            self.logger.info("Connection successful!")

        except Exception as e:
            print(
                f"Failed to connect to endpoint {self.endpoint} with client ID '{self.client_id}'\n{type(e).__name__}: {e}")

    def self_subscription(self):

        print("Subscribing to topic '{}'...".format(self.topic))

        try:
            # mqtt_connection.subscribe() will return 2 variables, "subscribe_future" and "packet_id".
            # The latter is not used, then can be replaced with _
            subscribe_future, _ = self.mqtt_connection.subscribe(
                topic=self.topic,
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_message_received)

            subscribe_result = subscribe_future.result()

            if self.logger:
                self.logger.info("Subscribed with {}".format(
                    str(subscribe_result['qos'])))
            else:
                print("Subscribed with {}".format(
                    str(subscribe_result['qos'])))

        except Exception as e:
            print(f"Failed to subscribe to topic {self.topic}\n{type(e).__name__}: {e}")

    def on_message_received(self, topic, payload, dup, qos, retain, **kwargs):
        if self.debug:
            print(f"Received message from topic '{topic}': {payload}")

    def publish_message(self, message: dict[str, Any]):
        try:
            self.mqtt_connection.publish(topic=self.topic, payload=json.dumps(
                message), qos=mqtt.QoS.AT_LEAST_ONCE)

        except Exception as e:
            print(f"Failed to publish message to topic '{self.topic}'\n{type(e).__name__}: {e}")

    def end_connection(self):
        print(f"Ending connection to endpoint {self.endpoint}...")

        try:
            disconnect_future = self.mqtt_connection.disconnect()
            disconnect_future.result()
            print(
                f"Connection to endpoint '{self.endpoint}' has been disconnected")

        except Exception as e:
            print(f"Failed to disconnect from endpoint {self.endpoint}\n{type(e).__name__}: {e}")
