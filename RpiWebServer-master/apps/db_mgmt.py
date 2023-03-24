import time
import json
from threading import Thread
import requests
from flask import request 
import apps.config_util as cu

from apps import devices as dv
import sys


mydb=cu.createMysqlDbUsingConfigFile("db.conf")
mycursor = mydb.cursor()

def register_new_device(macaddr, name):
    mycursor.execute("SELECT sensors_id FROM master_sensors where sensors_code=%s", [macaddr])
    rows = mycursor.fetchall()
    if len(rows)==1:
        id=rows[0][0]
        return False
    else:
        cursor = mydb.cursor()
        sql = "INSERT INTO master_sensors(sensors_code,sensors_type,create_user_id,room,floor,building,create_date,update_date,status) VALUES (%s,1,0,%s,1,'A',now(),now(),'A')"
        cursor.execute(sql, [macaddr,name])
        mydb.commit()
        id=cursor.lastrowid
        cursor.close()        
        print("Got new sensor :",macaddr,id) 
        return True

def remove_device(macaddr, name):
    pass

#modify here : add new parameter for request (building and bed)
def remotedb_async_add(param):
    ## TEST ##
    # print('Sensor Code : {}\nName : {}\nMatch : {}'.format(sensor_code, name, master))
    info = None
    with open("apps/engrafi/engrafi_info.json", "r") as f:
        info = json.load(f)

    form_data = {
        "v":1,
        "token":info["accessToken"],
        "deviceCode":param["MAC"],
        "code":info["deviceCode"],
        "device_des":param["DEVICE_DES"],
        "bed":param["BED"],
        "building":param["BUILDING"]
    }

    print(form_data)
    status = 'uncommitted'
    try:
        # url = 'http://babyai.org:' + str(7343) +'/devsync' --- obsoleted
        url = info["serverUri"] + "device/register"
        r= requests.post(url, form_data)
        print(r)
        status = 'committed'
        #add fault check
    except requests.exceptions.RequestException as e:
        status = 'error'
        print('status error with reason {}'.format(e))
    finally:
        print('Status : {}'.format(status))
    

def db_asycn_service_attach(tsk_name, param):
    Thread(target=tsk_name, args=(param,)).start()
