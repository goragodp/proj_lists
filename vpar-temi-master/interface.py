import paho.mqtt.client as mqtt
import socket
import time
from datetime import datetime

class CommandInterface:
    def __init__(self):
        self.__conn_state = False
        self.__TAG = "MQTT-SERVICE STATUS [{}] : {}"
        self.__timeout = 120
        self.__broker_url = "babyai.org"
        self.__usr = "wifimod"
        self.__psw = "PeEFc9Aq"
        self.__port = 1883
        self.__client_id = socket.gethostname() + ":" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        self.cmd_client = mqtt.Client(self.__client_id)
        self.cmd_client.username_pw_set(username=self.__usr, password=self.__psw)
        self.cmd_client.on_connect = self._on_connect
        self.cmd_client.on_disconnect = self._on_disconnect
        self.cmd_client.on_message = self._on_message
        
    def _on_connect(self, client, user_data, flag, rc):
        self.__conn_state = True
        print(self.__TAG.format('CONNECTED', flag))
    
    def _on_disconnect(self, client, user_data, rc):
        self.__conn_state = False
        print(self.__TAG.format('DISCONNECT', rc))
        self.cmd_client.loop_stop()

    def _on_message(self, client, user_data, msg):
        print(self.__TAG.format('MESSAGE_RECEIVED FROM {}'.format(msg.topic), msg.payload))
            
    def connect(self):
        try:
            self.cmd_client.connect(self.__broker_url, self.__port, self.__timeout)
            self.cmd_client.loop_start()
            while(not self.is_connected()):
                pass
        except:
            print(self.__TAG.format("ERROR", "problem on connect method"))
            
    def get_instance(self):
        return self.cmd_client
    
    def is_connected(self):
        return self.__conn_state
    
if __name__ == "__main__":
    conn_obj = interface_command()
    while True: 
        pass