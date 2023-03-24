# Raspberry Pi ECM Web-server
Enable control tunnel for rpi information manipulation using simple HTTP webserver (Flask) via port 7343. All RPI are equipped with this script!

## GET

### ***/*** (for test) :
- Brief - Test if webserver is running

### ***/devlist*** : 
- Brief - get a list of network device and return in json form
	[JSON]
	{
    		<IP> : <mac address>
    }
- Parameter Type : None
- Data Key :  None

### ***/listnwkdev*** :
- Brief - get list of network devices using hostname as a key as following
    [JSON]
    {<hostname> :
		{
    		“MAC” : <mac address>
   		    “IP” : <IP address>
    	}	
    }
- Parameter Type : None
- Data Keys : None

## POST Method	
### ***/bbmap*** : 
- Brief - Modified current broker IP of BBs according to user specific parameter, NOTE - This function request to internal * /regdev * for multiple RPI in system purpose
- Parameter Type : JSON
- Data Key:  
    1. “MAC” : Blackbox's MAC address
	2. “NAME” : Blackbox's assigned name
    4. “IP” : Blackbox's IP Address
    5. “BROKERIP” : RPI's IP Address which Blackbox is currently connected to	
	6. "BUILDING" : 1st Alias name for blackbox location specify by user
	7. "BED" : 2nd Alias name for blackbox location specify by user
	8. "DEVICE_DES" : info specified by user for blackbox information

### ***/regdev*** : 
- Brief - Write mathinng information to RPI local table and invoke thread to sync information to remote table
- Parameter Type : JSON
- Data Key:  
    1. “MAC” : Blackbox's MAC address
	2. “NAME” : Blackbox's assigned name


## TO DO Lists
- [x] Create boot.sh and modified ***rc.local*** at ***/etc/**** 
- [x] Add Database Field (***building*** and ***bed***) to ***Devices***
- [x] API manipulate newly added field
- [x] Test 

## ISSUE
- rc.local doesn't seem to work, it must be bashed mannually