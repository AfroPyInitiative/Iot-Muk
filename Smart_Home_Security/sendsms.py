#the code sends an sms via an API, when the tilt tilts and the sensor detects something

import RPi.GPIO as GPIO
import urllib
import urllib2
import time

senssor=13
tiltpin=23
ledpin=15

def setup():
	GPIO.setwarnings(FALSE)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(sensor,GPIO.IN)
	GPIO.setup(tiltpin,GPIO.IN)
	GPIO.setup(ledpin,GPIO.IN)

def email():
	
message = 'your needed' # define your messadge

username = 'naomekizzan@gmail.com' # Africa's talking account details
sender = 'Africa\'stalking'
    
hash = 'c61f5fd631f964b4a923fbbd3391080f53d91fdb3e89262e30a3a20cb44835e3' #Get this when logged in at https://account.africastalking.com/auth/api
   
numbers = 256706074507, # Message details
test_flag =1  #set flag to 1 to stimulate sending

vaues= ('test'		:test_flag,
	    'uname'		:username,
	    'hash'		:hash,
	    'massage'   :massadge,
	    'numbers='  :numbers )

    
$data = 'username=' . username . 'hash=' . hash   # Prepare data for POST request
     . 'numbers=' . numbers . "sender=" . sender . "message=" . message;
  

def loop():
	while True:
		if GPIO.input(sensor)==GPIO.HIGH:
   			GPIO.output(tiltpin,GPIO.HIGH)
   			GPIO.output(ledpin,GPIO.HIGH)
   			email()
  	 	else:
  	 		print('no one there')
  	 		GPIO.output(tiltpin,GPIO.LOW)
  	 		GPIO.output(ledpin,GPIO.LOW)
	
def destroy():
	GPIO.cleanup()    



if __name__=='__main__':
	setup()
	
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
	