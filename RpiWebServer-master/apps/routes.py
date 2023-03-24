from flask import Flask, request, jsonify, json
import requests

from apps import devices as dv
from apps import db_mgmt as dbm
from apps import app

@app.route('/')
def index():
    return ('Obiwan : Hello there!')

@app.route('/listnwkdev')
def discovery_device():
    resp = dv.get_dev_list()
    return resp

@app.route('/devlist')
def get_device_ip_mac():
    resp = dv.device_IPMAC_match()
    return resp


'''
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"MAC":"C4:4F:33:0C:AE:19","IP":"192.168.43.72", "NAME":"R0304 - EMERG", "BROKERIP":"192.168.43.200"}' \
  http://192.168.43.200:7343/bbmap
'''
@app.route('/bbmap', methods=['POST'])
def device_register():
    content = request.get_json(silent=True)
    if content != None:
        mac = content["MAC"]
        name = content["NAME"]
        ip = content["IP"]
        brokerip = content["BROKERIP"] #rpi ip
        building = content["BUILDING"]
        bed = content["BED"]
        dev_des = content["DEVICE_DES"]

        #modify data master sensor database on rpi by inserting blackbox mac
        url = "http://" + brokerip + ":7343/regdev"
        obj = {"MAC":mac, "NAME":name}
        print("Sendin to {}".format(url))
        try:
            requests.post(url, json=content)
        except requests.exceptions.RequestException as e:
            print(e)
            return json.dumps({'status':'ERROR'})

        #Black box Broker IP modify via http
        url = "http://" + ip + "/api/v1/system/config"
        obj = {"mqtt_uri":"mqtt://" + brokerip}
        print("Connect to bb")
        try:
            requests.post(url, json=obj, timeout = 1) #black box do not return timeout
        except requests.exceptions.RequestException as e:
            pass
        
        return json.dumps({'status':'OK'})
    else:
        return json.dumps({'status':'ERROR, EMPTY CONTENT'})

@app.route('/regdev', methods=['POST'])
def wifi_module_register():
    content = request.get_json(silent=True)
    mac = content["MAC"]
    name = content["NAME"]
    building = content["BUILDING"]
    bed = content["BED"]
    dev_des = content["DEVICE_DES"]

    
    result = dbm.register_new_device(mac, name)
    
    # attach new async task for db sync
    dbm.db_asycn_service_attach(dbm.remotedb_async_add, content)
    
    if result == True:
        return json.dumps({'status':'OK'})
    else:
        return json.dumps({'status':'ERROR'})


