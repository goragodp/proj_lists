# Mediator program for bridging webapplication and Temi robot
> The program was develop as a mediator for low-code platform (LCP) web-application and Temi robot. Generally, the robot need to be program using android framework which is complicate and poses high learning curve. So, Blockly, a block programming style, is develop to generate a control logic of the robot. LCP translated blocks program into actual code and execute a logic flow program. This program will sent the logic flow to the robot using MQTT protocol.
- Framework : paho-mqtt
- language  : Python