import robot as temi
from interface import CommandInterface

temi_serial = '01234'

print('test')
mqtt = CommandInterface()
mqtt.connect()

robot = temi.Robot(mqtt, temi_serial)

robot.speak("Hello", "en")
robot.speak("How are you", "en")
robot.goto("whiteboard")
robot.speak("Arrrived", "en")
robot.speak("I will leave now", "en")
robot.goto("home base")
# robot.call("man")

