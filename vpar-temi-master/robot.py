import json

class Robot:
    def __init__(self, interface, temi_serial):
        self.__TAG = "TEMI-ACTION STATUS [{}] : {}"
        self.interface = interface
        self.__id = temi_serial
        self.__robot_action = {
            'action':"",
            'state':""
        }
        
        self.interface.get_instance().subscribe("temi/{}/#".format(self.__id))
        #add listener for certain topic
        self.interface.get_instance().message_callback_add("temi/{}/goto-status".format(self.__id), self.onGotoStatusChangeListener)
        self.interface.get_instance().message_callback_add("temi/{}/call-status".format(self.__id), self.onTelepresenceEventChangeListener)
        self.interface.get_instance().message_callback_add("temi/{}/speak-status".format(self.__id), self.onTtsStatusChangeListener)
        
    # Class Utilities ###########################################################
    def __parser(self, obj):
            return json.dumps(obj)
    
    def command_send(self, package):
        self.__robot_action['action'] = package['action']
        self.__robot_action['state'] = 'sending command'
        self.interface.get_instance().publish('temi/{}/temi-cmd'.format(self.__id, package['action']), self.__parser(package))
        while(self.__robot_action['state'] is not 'done'):
            pass
    
    # Robot action methods #####################################################
    def speak(self, tts, lang_op):
        package = {'action':'speak',
                   'content':tts,
                   'language':lang_op}
        self.command_send(package)
        
    def goto(self, location):
        package = {'action':'goto',
                   'content':location}
        self.command_send(package)
    
    def call(self, id):
        package = {'action':'call',
                   'content':id}
        self.command_send(package)
    
    # Robot callback  #####################################################
    # Note that every callback has different COMPLETE state's name thus 
    # we use 'done' to indicate final state of action
    def onGotoStatusChangeListener(self, client, user_data, msg):
        state = msg.payload.decode('utf-8')
        if(state == 'START'):
            self.__robot_action['state'] = 'start'
        elif(state == 'CALCULATING'):
            self.__robot_action['state'] = 'calculating'
        elif(state == 'GOING'):
            self.__robot_action['state'] = 'going'
        elif(state == 'COMPLETE'):
            self.__robot_action['state'] = 'done'
        elif(state == 'ABORT'):
            self.__robot_action['state'] = 'abort'

        print(self.__TAG.format(self.__robot_action['action'], self.__robot_action['state']))
    
    def onTelepresenceEventChangeListener(self, client, user_data, msg):
        state = msg.payload.decode('utf-8')
        print(msg)
        if(state == 'TYPE_INCOMING'):
            self.__robot_action['state'] = 'incomming'
        elif(state == 'TYPE_OUTGOING'):
            self.__robot_action['state'] = 'outgoing'
        elif(state == 'STATE_STARTED'):
            self.__robot_action['state'] = 'started'
        elif(state == 'STATE_ENDED'):
            self.__robot_action['state'] = 'done'
            
        print(self.__TAG.format(self.__robot_action['action'], self.__robot_action['state']))
    
    def onTtsStatusChangeListener(self, client, user_data, msg):
        state = msg.payload.decode('utf-8')
        print(msg)
        if(state == 'COMPLETED'):
            self.__robot_action['state'] = 'done'
        elif(state == 'STARTED'):
            self.__robot_action['state'] = 'start'
        elif(state == 'ERROR'):
            self.__robot_action['state'] = 'error'
        elif(state == 'NOT_ALLOWED'):
            self.__robot_action['state'] = 'not_allow'
        
        print(self.__TAG.format(self.__robot_action['action'], self.__robot_action['state']))
        
if __name__ == "__main__":
    robot = Robot()
