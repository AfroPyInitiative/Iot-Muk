import RPi.GPIO as GPIO

led = 11
tilt = 12
touch = 13
led2 = 25

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led, GPIO.OUT)
    GPIO.setup(led2, GPIO.OUT)
    GPIO.setup(tilt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(touch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(TiltPin, GPIO.BOTH, callback=detect, bouncetime=200)

def loop():
    while True:
        if GPIO.input(touch) == LOW:
           GPIO.ouput(led2, GPOI.LOW)
           print 'not touched'
           
        elif GPIO.input(touch) == HIGH:
             GPIO.ouput(led2, GPOI.HIGH)
           print 'touched'

        elif GPIO.input(touch) == HIGH and GPIO.input(tilt) == HIGH:
            GPIO.output(led2, GPIO.HIGH)
            GPIO.output(led, GPIO.HIGH)
            print 'touched and tilted'
           
        elif GPIO.input(tilt) == LOW:
            GPIO.ouput(led, GPIO.LOW)
            print 'not tilited'
        else:
            GPIO.ouput(led, GPOI.HIGH)
            print 'tilted'

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':     
	setup()
	try:
            loop()

	except KeyboardInterrupt:
            destroy()
		
    
