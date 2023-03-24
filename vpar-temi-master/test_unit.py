import paho.mqtt.client as mqtt

test_serial = '01234'

def on_connect(client, user_data, flag, rc):
    print("Client connected")
    client.subscribe('temi/{}'.format(test_serial))
    client.message_callback_add('test/', test)

def on_message(client, user_data, msg):
    print("MQTT Topic [{}] : {}".format(msg.topic, msg.payload))
    client.publish("temi/{}/{}".format(test_serial, msg.topic), 'COMPLETED')
    client.publish("temi/{}/{}".format(test_serial, msg.topic), 'STATE_END')
    client.publish("temi/{}/{}".format(test_serial, msg.topic), 'COMPLETE')

def test(client, user_data, msg):
    print(msg)
    
host = 'babyai.org'
usr = 'wifimod'
psw = 'PeEFc9Ag'

client = mqtt.Client("")

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(usr, psw)
client.connect(host, 1883, 60)

client.loop_forever()