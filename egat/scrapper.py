from concurrent.futures import ThreadPoolExecutor, wait
import datetime
import json
from csv import writer
import requests

plant_url = ['https://enzy-chiller.egat.co.th/api/get-plant']
report_url = ['https://enzy-chiller.egat.co.th/api/get-report']#report

chiller_url = [f'https://enzy-chiller.egat.co.th/api/get-chiller?id=CH_{str(i).zfill(2)}' 
                for i in range(1, 4 + 1)]
ahu_url = [f'https://enzy-chiller.egat.co.th/api/get-ahu-fl4?id=AHU_4_{i}' 
             for i in range(1,2 + 1)] #AHU of 4 floor
vav_url = [f'https://enzy-chiller.egat.co.th/api/get-vav-fl4?id=VB_4_{str(i).zfill(2)}'
            for i in range(1, 18 + 1)] #VAV of 4 floor

class base:
    def __init__(self,log_fname, headers):
        self.log_fname = log_fname
        self.headers = headers
    
    def get(self):
        pass

    def req(self):
        pass

    def write(self):
        pass

class scrapper(base):
    def __init__(self, urls, log_fname, headers):
        super().__init__(log_fname, headers)
        self.urls = urls
    
    def get(self, url):
        r = requests.get(url)
        ts = datetime.datetime.now().strftime(("%m/%d/%Y-%H:%M:%S"))
        loc = url.find('?')
        _, data = url[loc + 1:].split('=')
        result = {}
        result['TS'] = ts
        result['ID'] = data 
        
        res_json = json.loads(r.text)
        result = dict(result, **res_json)

        return result

    def req(self):
        with ThreadPoolExecutor() as executor:
            self.res = [executor.submit(self.get, url) for url in self.urls]
            wait(self.res)
        self.write(self.res)
    
    def write(self, res):
        with open(self.log_fname, 'a+', newline='', encoding='utf8') as f:
            wrt = writer(f)
            for r in res:
                data = r.result()
                log_data = [data[key] for key in data]
                wrt.writerow(log_data)


class scrapper_single_point(base):
    
    def __init__(self, url, log_fname, headers):
        super().__init__(log_fname, headers)
        self.url = url

    def  get(self, url):
        r = requests.get(url)
        ts = datetime.datetime.now().strftime(("%m/%d/%Y-%H:%M:%S"))
        result = {}
        result['TS'] = ts
        res_json = json.loads(r.text)
        result = dict(result, **res_json)

        return result

    def req(self):
        with ThreadPoolExecutor() as executor:
            self.res = executor.submit(self.get, self.url)
        self.write(self.res)
    
    def write(self, res):
        with open(self.log_fname, 'a+', newline='', encoding='utf8') as f:
            wrt = writer(f)
            data = res.result()
            log_data = [data[key] for key in data]
            wrt.writerow(log_data)



header = ['TS', 'ID', 'ZONE TEMPERATURE TEMP', 'ZONE TEMPERATURE_SETPOINT', 'AIR FLOW ACTUAL(cfm)', 'AIR FLOW ACTUAL(cfm)']
log_fname = '/home/mmm/egat/vav_log.csv'
vav_logger = scrapper(vav_url, log_fname, header)

header = ['TS', 'ID', 'SUPPLY_TEMPERATURE_TEMP', 'SUPPLY TEMPERATURE SETPOINT', 'SUPPLY TEMPERATURE SETPOINT', 'SUPPLY TEMPERATURE SETPOINT','VSD POWER(kW)', 'VSD SPEED(rpm)']
log_fname = '/home/mmm/egat/ahu_log.csv'
ahu_logger  = scrapper(ahu_url, log_fname, header)

header = ["Control","Avg Current % RLA","Current L1","Current L2",
"Current L3","Voltage AB","Voltage BC","Voltage CA","Motor Winding Temp #1",
"Motor Winding Temp #2","Motor Winding Temp #3"]
log_fname = '/home/mmm/egat/chiller_log.csv'
chiller_logger  = scrapper(chiller_url, log_fname, header)

header = ["OUTDOOR TEMP","OUTDOOR HUMID","CH 01 Compressorcurrentdraw","CH 01 Chillwater temp leaving",
          "CH 02 Compressorcurrentdraw","CH 02 Chillwater temp leaving","CH 03 Compressorcurrentdraw",
          "CH 03 Chillwater temp leaving","CH 04 Compressorcurrentdraw","CH 04 Chillwater temp leaving"]
log_fname = '/home/mmm/egat/plant_log.csv'
plant_logger  = scrapper_single_point(plant_url[-1], log_fname, header)

header = ["VSD-kW","CHILLER Power(kW)","CHILLER kW/ton","CPMS Power(kW)","CPMS kW/ton","CPMS+VSD kW","CPMS+VSD kW/ton"]
log_fname = '/home/mmm/egat/report_log.csv'
report_logger  = scrapper_single_point(report_url[-1], log_fname, header)

try:
    vav_logger.req()
    ahu_logger.req()
    chiller_logger.req()
    plant_logger.req()
    report_logger.req()
except Exception as e:
    print(e)
