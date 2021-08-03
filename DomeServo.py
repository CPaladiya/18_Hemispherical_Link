from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep

#a class that will have function to handle all the movements related to servo
class DomeServo:
    
    def __init__(self):
        #before running the program do 'sudo pigpiod' in terminal
        factory = PiGPIOFactory() #since the pulses are software generated we want to mimic hardware generated to remove jitter from servo
        #top camera servo configuration, here we have set pulse width to reach full capabilities of servo
        self.ST = Servo(17, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory = factory)
        self.ST.value = -1
        #bottom camera servo configuration
        self.SB = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory = factory)
        self.SB.value = 0
        
    #we set value within limit otherwise we print overlimit in terminal
    #range allowed -0.6 to 0.6. limited to save hardware and wires
    def AddSBValue(self,AddValue):
        temp = self.SB.value
        temp -= AddValue
        if(temp >= -0.6 and temp <= 0.6):
            self.SB.value -= AddValue
            print("New Bottom servo value {}".format(self.SB.value))
        else:
            print("Bottom Servo Value out of limit! {}".format(temp))
            if(temp >=0):
                self.SB.value = 0.6
            else:
                self.SB.value = -0.6
    
    #we set value within limit otherwise we print overlimit in terminal
    #range allowed -1.0 to -0.4. limited to save hardware and wires
    def AddSTValue(self,AddValue):
        temp = self.ST.value
        temp -= AddValue
        if(temp >= -1.0 and temp <= -0.25):
            self.ST.value -= AddValue
            print("New Top servo value {}".format(self.ST.value))
        else:
            print("Top Servo Value out of limit! {}".format(temp))
            if(temp >-0.25):
                self.ST.value = -0.25
            else:
                self.ST.value = -1.0
