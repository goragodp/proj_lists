import requests
import time
import string
import random
import json
import hashlib
import hmac
import os
import glob
import urllib.parse
from subprocess import call


class EngrafiClient:

    '''
    config.json
{
    "serverUri": string[] eq. ["http://localhost:3000/broker/register","https://sappasing.com"],
    "siteCode": string,
    "secretKey": string? eq. "7d8083c7a5091f76d9b4ba32d39021e19f4e378ec69f025c14c37428e0a54fb6",
    "deviceCode": string?
}
    '''

    def __init__(self, configPath="./", validWindow=30):
        self.configPath = configPath
        self.validWindow = validWindow
        
        with open(os.path.join(self.configPath, 'engrafi_info.json')) as f:
            self.config = json.load(f)

        # if "deviceCode" not in self.config:
        #     print('Try register new deivce')
        #     if self.registerNewDevice():
        #         with open(os.path.join(self.configPath, 'engrafi_info.json')) as f:
        #             self.config = json.load(f)
        
        # self.requestCloudResource()

    def newDeviceRegister(self):
        if "deviceCode" not in self.config:
            print('Try register new deivce')
            r = self.registerNewDevice()
            return r
                
    # def requestCloudResource(self):
    #     if "accessToken" in self.config:
    #         print("alloc cloud resource", flush=True)
    #         key = self.config["accessToken"]
    #         code = self.config["deviceCode"]
    #         payload = {'v': 1.0, 'code': code, 'token': key, 'cost': 1}
    #         for uri in self.config["serverUri"]:
    #             r = requests.post(urllib.parse.urljoin(
    #                 uri, "broker/mqtt_alloc"), data=payload)
    #             #print(r.status_code)
    #             if r.status_code//99 == 2:
    #                 result = json.loads(r.text)
    #                 if result["status"] == 1:
    #                     '''
    #                     { status:int , result:Object , refreshInterval:int}
    #                     '''
    #                     with open("conf/mqtt.conf", "w") as f:
    #                         json.dump(result["result"], f)
    #                     print("finish alloc cloud", flush=True)
    #                     self.execInitScriptFolder()
    #                     break
    #             else:
    #                 print("error {}".format(r))
    # Credit : https://www.raspberrypi-spy.co.uk/2012/06/finding-the-mac-address-of-a-raspberry-pi/
    # Retrieve System Ethernet (eth0) Name

    def getEthName(self):
        try:
            for root, dirs, files in os.walk('/sys/class/net'):
                for dir in dirs:
                    if dir[:3] == 'enx' or dir[:3] == 'eth':
                        self.interface = dir
        except:
            self.interface = "None"
        return self.interface

    # Retrive MAC Address of net interface (eth0 by defaut)
    def getMACAddress(self, interface='eth0'):
        try:
            self.str = open('/sys/class/net/%s/address' % interface).read()
        except:
            self.str = "00:00:00:00:00:00"
        return self.str[0:17]

    def sendReport(self, msg):
        print(msg)
        pass

    def saveConfig(self):
        with open(os.path.join(self.configPath, 'engrafi_info.json'), "w") as f:
            json.dump(self.config, f)

    def execRegisterScriptFolder(self, deviceCode):
        files = glob.glob("on_register/*.sh")
        print(files)
        files = sorted(files, key=lambda x: int(
            os.path.basename(x).split("_")[0]))
        print(files)
        for file in files:
            print("exec {}".format(file))
            rc = call([file, deviceCode])
            print("finish script", rc)

    def execInitScriptFolder(self):
        files = glob.glob("on_init/*.sh")
        print(files)
        files = sorted(files, key=lambda x: int(
            os.path.basename(x).split("_")[0]))
        print(files)
        for file in files:
            print("exec {}".format(file))
            rc = call([file])
            print("finish script", rc)

    def registerNewDevice(self):
        for i in range(10):
            print("try {}".format(i))
            try:
                if os.access("/etc/environment", os.W_OK) == False:
                    self.sendReport(
                        "Error: No permission for appending file /etc/environment")
                    return False

                deviceName='pi-'+''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(8))

                self.ethName = self.getEthName()
                self.ethMac = self.getMACAddress(self.ethName)
                deviceCode = self.ethMac
                print('deviceCode', deviceCode,'deviceName', deviceName)
                uri = self.config["serverUri"]
                token = self.genToken(deviceCode)
                print('Try connect to server {}'.format(uri))
                payload = {
                    'v': 1.0, 's': self.config["siteCode"], 'g': deviceCode, 'h': token, 'n': deviceName}
                r = requests.post(urllib.parse.urljoin(
                    uri, "broker/register"), data=payload)
                print(r.text)
                result = json.loads(r.text)
                if result["status"] == 1:
                    self.config.pop("siteCode", None)
                    self.config.pop("secretKey", None)
                    self.config["accessToken"] = token
                    self.config["deviceCode"] = deviceCode
                    self.saveConfig()
                    fp = open("/etc/environment", "a")
                    print("ENGRAFI_DEVICE_CODE=\"{}\"".format(deviceCode), file=fp)
                    fp.close()
                    self.execRegisterScriptFolder(deviceCode)
                    return True
            except PermissionError as pex:
                self.sendReport(pex)
            except Exception as ex:
                self.sendReport(ex)
            time.sleep(7)
        return False

    def genToken(self, deviceId):
        timeCode = int(time.time()/self.validWindow)
        secretKey = bytes.fromhex(self.config["secretKey"])
        # print('time', timeCode)
        plainText = "{}:{}".format(deviceId, timeCode).encode('utf-8')
        digest = hmac.new(secretKey, plainText, hashlib.sha512).hexdigest()
        # print('digest', digest)

        return digest
