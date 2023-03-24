from apps import app
from apps.engrafi import engrafi_client as ec
import os

if __name__ == '__main__':
    ENGRAFI_CLIENT = ec.EngrafiClient(os.path.join(os.getcwd(), 'apps', 'engrafi'))
    
    print('register broker')
    while(ENGRAFI_CLIENT.newDeviceRegister() == False):
        pass
    print('Done, start web services')
    
    app.run(debug=True, port=7343, host='0.0.0.0')