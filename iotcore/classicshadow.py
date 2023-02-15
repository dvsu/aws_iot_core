
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import json

# Shadow JSON schema:
#
# Name: Bot
# {
# "state": {
# "desired":{
# "property":<INT VALUE>
# }
# }
# }

# # Custom Shadow callback
# def customShadowCallback_Update(payload, responseStatus, token):
#     # payload is a JSON string ready to be parsed using json.loads(...)
#     # in both Py2.x and Py3.x
#     if responseStatus == "timeout":
#         print("Update request " + token + " time out!")
#     if responseStatus == "accepted":
#         payloadDict = json.loads(payload)
#         print("~~~~~~~~~~~~~~~~~~~~~~~")
#         print("Update request with token: " + token + " accepted!")
#         print("property: " + str(payloadDict["state"]["desired"]["property"]))
#         print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
#     if responseStatus == "rejected":
#         print("Update request " + token + " rejected!")

# def customShadowCallback_Delete(payload, responseStatus, token):
#     if responseStatus == "timeout":
#         print("Delete request " + token + " time out!")
#     if responseStatus == "accepted":
#         print("~~~~~~~~~~~~~~~~~~~~~~~")
#         print("Delete request with token: " + token + " accepted!")
#         print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
#     if responseStatus == "rejected":
#         print("Delete request " + token + " rejected!")


# # Delete shadow JSON doc
# deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)


class AWSIoTMQTTShadow:

    def __init__(self, endpoint: str, port: int, client_id: str, certificate: str, private_key: str, root_ca: str, thing_name: str, topic: str, logger=None):
        self.logger = None
        if logger:
            self.logger = logging.getLogger(logger)
        self.endpoint = endpoint
        self.client_id = client_id
        self.root_ca = root_ca
        self.certificate = certificate
        self.private_key = private_key
        self.port = port
        self.thing_name = thing_name

        self.mqtt_shadow_client = AWSIoTMQTTShadowClient(self.client_id)
        self.mqtt_shadow_client.configureEndpoint(self.endpoint, self.port)
        self.mqtt_shadow_client.configureCredentials(
            self.root_ca, self.private_key, self.certificate)

        # AWSIoTMQTTShadowClient configuration
        self.mqtt_shadow_client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.mqtt_shadow_client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.mqtt_shadow_client.configureMQTTOperationTimeout(5)  # 5 sec

        self.initializing_connection()

        # Create a deviceShadow with persistent subscription
        self.device_shadow_handler = self.mqtt_shadow_client.createShadowHandlerWithName(
            self.thing_name, True)

    def initializing_connection(self):
        self.logger.info(
            f"Connecting to endpoint {self.endpoint} with client ID '{self.client_id}'...")
        try:
            # Connect to AWS IoT
            self.mqtt_shadow_client.connect()

            self.logger.info("Connection successful!")

        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Failed to connect to endpoint {self.endpoint} with client ID '{self.client_id}'\n{type(e).__name__}: {e}")
            else:
                print(
                    f"Failed to connect to endpoint {self.endpoint} with client ID '{self.client_id}'\n{type(e).__name__}: {e}")

    def update_shadow(self, message):
        try:
            payload = {
                "state": {
                    "desired": message
                }
            }
            self.device_shadow_handler.shadowUpdate(
                json.dumps(payload), self.custom_shadow_callback_update, 5)

        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Failed to update desired shadow to thing '{self.thing_name}'\n{type(e).__name__}: {e}")
            else:
                print(
                    f"Failed to update desired shadow to thing '{self.thing_name}'\n{type(e).__name__}: {e}")

    def custom_shadow_callback_update(self, payload: str, response_status: str, token: str) -> None:
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x

        # Typical response_status
        #   "timeout"
        #   "accepted"
        #   "rejected"

        print(type(token))
        if response_status == "timeout":
            print("Update request " + token + " time out!")
        if response_status == "accepted":
            payloadDict = json.loads(payload)
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Update request with token: " + token + " accepted!")
            print("property: " +
                  str(payloadDict["state"]["desired"]))
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if response_status == "rejected":
            print("Update request " + token + " rejected!")

    # def end_connection(self):
    #     self.logger.info(f"Ending connection to endpoint {self.endpoint}...")

    #     try:
    #         disconnect_future = self.mqtt_connection.disconnect()
    #         disconnect_future.result()
    #         self.logger.info(
    #             f"Connection to endpoint '{self.endpoint}' has been disconnected")

    #     except Exception as e:
    #         if self.logger:
    #             self.logger.error(
    #                 f"Failed to disconnect from endpoint {self.endpoint}\n{type(e).__name__}: {e}")
    #         else:
    #             print(
    #                 f"Failed to disconnect from endpoint {self.endpoint}\n{type(e).__name__}: {e}")
