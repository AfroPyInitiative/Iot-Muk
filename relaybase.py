import RPi.GPIO as GPIO
import time

RelayPin = 23
ButtonPin = 11

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RelayPin, GPIO.OUT)
	GPIO.setup(ButtonPin, GPIO.IN)
	GPIO.output(ButtonPin, GPIO.LOW)
	#GPIO.output(RelayPin, GPIO.HIGH) 

def loop():
	while True:
		
		GPIO.output(RelayPin, GPIO.HIGH)
		print '...relay on'
		time.sleep(0.5)
		
		GPIO.output(RelayPin, GPIO.LOW)
		print 'relay off...'
		time.sleep(0.5)

def destroy():
	GPIO.output(RelayPin, GPIO.HIGH)
	GPIO.cleanup()                  

if __name__ == '__main__':  #start of prog
	setup()
	try:
		loop()
	except KeyboardInterrupt:  
		destroy()

