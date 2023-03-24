
#RUN ONLY ONCE TO GENERATE LOG TEMPALTE FOR EACH DATASET

from csv import writer



def template_generator(log_fname, headers):
    log_fname = log_fname
    with open(log_fname, 'w+', newline='', encoding='utf8') as f:
        wrt = writer(f)
        wrt.writerow(headers)

headers = ['TS', 'ID', 'ZONE TEMPERATURE TEMP', 'ZONE TEMPERATURE_SETPOINT', 'AIR FLOW ACTUAL(cfm)', 'AIR FLOW ACTUAL(cfm)']
log_fname = 'vav_log.csv'
template_generator(log_fname, headers)

header = ['TS', 'ID', 'SUPPLY_TEMPERATURE_TEMP', 'SUPPLY TEMPERATURE SETPOINT', 'SUPPLY TEMPERATURE SETPOINT', 'SUPPLY TEMPERATURE SETPOINT','VSD POWER(kW)', 'VSD SPEED(rpm)']
log_fname = 'ahu_log.csv'
template_generator(log_fname, headers)

headers = ["Control","Avg Current % RLA","Current L1","Current L2",
"Current L3","Voltage AB","Voltage BC","Voltage CA","Motor Winding Temp #1",
"Motor Winding Temp #2","Motor Winding Temp #3"]
log_fname = 'chiller_log.csv'
template_generator(log_fname, headers)

headers = ["OUTDOOR TEMP","OUTDOOR HUMID","CH 01 Compressorcurrentdraw","CH 01 Chillwater temp leaving",
          "CH 02 Compressorcurrentdraw","CH 02 Chillwater temp leaving","CH 03 Compressorcurrentdraw",
          "CH 03 Chillwater temp leaving","CH 04 Compressorcurrentdraw","CH 04 Chillwater temp leaving"]
log_fname = 'plant_log.csv'
template_generator(log_fname, headers)

headers = ["VSD-kW","CHILLER Power(kW)","CHILLER kW/ton","CPMS Power(kW)","CPMS kW/ton","CPMS+VSD kW","CPMS+VSD kW/ton"]
log_fname = 'report_log.csv'
template_generator(log_fname, headers)
