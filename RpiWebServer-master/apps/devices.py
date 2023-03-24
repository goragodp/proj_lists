'''
Author: Goragod
Email : g.pongth@gmail.com
Desc :  The script is for router-based mac-ip mapping
'''
import subprocess
import re
import json
import socket
import requests
import urllib
import time
from threading import Thread

# @Name: device_IPMAC_match
# @param : none
# @return : json
# @Brief : Find connected devices on network using 'nmap' command (sudo nmap <ip>/24 => scan subnet)
#          The function read a result and pack IP <key> and MAC <data> address of devices in following format
#             {
#                 <ip>:<mac>,
#                 <ip>:<mac>
#             }
#           if any device mac address is omited by nmap, null will be used as a data

def device_IPMAC_match():
    addr = get_nwk_ip()
    cmd = "sudo nmap -sP " + str(addr) + "/24"
    process = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            universal_newlines=True,
                            shell=True)

    opt = process.stdout.read()
    rgx = re.compile('[%s]' % ('()'))
    result = rgx.sub('', str(opt)).split('\n')

    d = get_self_info() #1st field is own ip and mac since nmap is not display mac of its own 
    for line in result:
        if line.find('Nmap scan') != -1: #Add ip as key
            key = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line).group()
            if key not in d.keys():
                d[key] = None
                continue
        elif(line.find('MAC Address') != -1) and key != None: # add mac as a field according to key
            mac = re.search(r'([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}', line)
            if mac:
                d[key] = mac.group()
                key = None
                continue
        else:
            continue

    return json.dumps(d)


def get_dev_list():
    addr = get_nwk_ip()
    cmd = "sudo nmap -sP " + str(addr) + "/24"
    process = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            universal_newlines=True,
                            shell=True)

    opt = process.stdout.read()
    rgx = re.compile('[%s]' % ('()'))
    result = rgx.sub('', str(opt)).split('\n')
    
    d = {}
    d[get_hostname()] = {"IP":get_ip(), "MAC": get_mac()}
    #create list of network devices with 2 cases
    # if Name is omitted, default name is UNKNOWx where x is number
    # if MAC is ommitted, "MAC" field is None
    unk_cnt  = 1 #counting device that omit its name -- for naming purpoose --
    key = None
    for line in result:
        if line.find('Nmap scan') != -1: #Add Name as key
            if(line.find('pi') != -1): #skip self (RPI)
                continue 
            t = line.split(' ')
            if(len(t) == 5): #only IP address is present!
                key = "UNKNOWN" + str(unk_cnt)
                d[key] = {"IP":t[4], "MAC":None}
            else: # Hostname and IP are present!
                key = t[4]
                d[key] = {"IP":t[5], "MAC":None}
            continue
        elif line.find('MAC') != -1: #MAc addr is present
            t = line.split(' ')
            d[key]["MAC"] = t[2]
            key = None
            continue

    return json.dumps(d)

# @Name: get_nwk_ip
# @param : none
# @return : ip address (string)
# @Brief : Find ip address and replace last field with 0 eg. 192.168.1.123 -> 192.168.1.0 for nmap command
def get_nwk_ip():
    opt = get_ip()
    opt = opt.split('.')
    opt[3] = "0" 
    return '.'.join(opt)


# @Name: get_self_info
# @param : none
# @return : dict of {<ip>:<mac>}
# @Brief : -
def get_self_info():
    ip = get_ip()
    mac = get_mac()
    return {ip:mac}

def get_ip():
    ip = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE, universal_newlines=True).stdout.read()
    return ip[:-2] 

def get_hostname():
    name = subprocess.Popen(['hostname'], stdout=subprocess.PIPE, universal_newlines=True).stdout.read()
    return name[:-1]

def get_mac(interface = 'eth0'):
    try:
        str = open('/sys/class/net/%s/address' % interface).read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]

if __name__ == "__main__":
    pass
