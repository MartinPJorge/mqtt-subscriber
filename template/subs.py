#https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# python 3.11

import random

from paho.mqtt import client as mqtt_client


broker = '' # TODO
port = 0 # TODO
topic = '' # TODO
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(self, client, userdata, flags, rc):
        print('flags', flags)
        ## print('client', client)
        ## print('rc', rc)
        ## if rc == 0:
        ##     print("Connected to MQTT Broker!")
        ## else:
        ##     print(f"Failed to connect, return code {rc}\n")

    #client = mqtt_client.Client(client_id)
    client = mqtt_client.Client(client_id=client_id,
     callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        # TODO


    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

