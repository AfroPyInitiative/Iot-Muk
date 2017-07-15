import RPi.GPIO as GPIO
from time

RelayPin = 23                                                            #gpio pin for relay
ButtonPin = 11                                                           #gpio pin for button
percolator = 13                                                          #gpio pin for percolator

def setup():
	GPIO.setmode(GPIO.BCM)                                           #set gpio mode to bread board mode
	GPIO.setup(RelayPin, GPIO.OUT)                                  #setup relay gpio as an output
	GPIO.setup(ButtonPin, GPIO.IN)                                    #setup relay gpio as an input
	GPIO.setup(percolator, GPIO.OUT)                                 #setup relay gpio as an output
	GPIO.input(ButtonPin, GPIO.LOW)                                   #set initial output of button gpio to low
	GPIO.output(percolator, GPIO.LOW)# is percolator input or output?   #set initial output of button gpio to low
	#GPIO.output(RelayPin, GPIO.HIGH) 

def loop():
	while True:
       
	    # 4-8/9 minutes to boil a litre

	    if GPIO.input(ButtonPin, GPIO.HIGH):                           #button is pressed        we might have to change the button as a trigger
                #GPIO.output(RelayPin, GPIO.HIGH)
                print 'turning on percolator'
                stop = time.time() + 60*7                                   #stop time
                while time.time() < stop:                                   #continue while current time is less than stop time
                    GPIO.input(percolator, GPIO.HIGH)                       #switch on percolator

            elif GPIO.input(ButtonPin, GPIO.LOW):                          #button is not pressed
                print 'turning off percolator'
                GPIO.input(percolator, GPIO.LOW)                           #switch off percolator

            else:
                print 'turning off'

	    	

def destroy():
	GPIO.input(ButtonPin, GPIO.HIGH)
	GPIO.output(percolator, GPIO.HIGH)
	GPIO.cleanup()                  

if __name__ == '__main__':  #start of prog
	setup()
	try:
		loop()
	except KeyboardInterrupt:  
		destroy()

