#Drive 16x2 LCD screen for Raspberry Pi

import dht11
import RPi.GPIO as GPIO
import time
import MySQLdb
from time import sleep

# Define GPIO to LCD mapping
LCD_RS = 25
LCD_E  = 5
LCD_D4 = 21
LCD_D5 = 20
LCD_D6 = 16
LCD_D7 = 12

Temp_sensor = 24
Buzzer_sensor = 18
receiver_in = 27
blue_led = 7
white_led = 4

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  instance = dht11.DHT11(pin = Temp_sensor)
  GPIO.setup(LCD_E, GPIO.OUT)  # Enable
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(Buzzer_sensor,GPIO.OUT)
  GPIO.setup(blue_led,GPIO.OUT)
  GPIO.output(blue_led,GPIO.LOW)
  GPIO.output(Buzzer_sensor,GPIO.LOW)
  GPIO.setup(receiver_in, GPIO.IN)
  
  alpha = 0.75
  period = 20
  change = 0.0
  oldValue = 0
  oldChange = 0
    
  # Initialise display
  lcd_init()

  while True:
	#get DHT11 sensor value
	result = instance.read()
	premor_id = 1
	# Send some test

	if result.is_valid():
		lcd_string("Temp :"+str(result.temperature)+"C",LCD_LINE_1)
		lcd_string("Humid:"+str(result.humidity)+"%",LCD_LINE_2)
		print 'Temperature: '+str(result.temperature)
		print 'Humidity: '+str(result.humidity)
		time.sleep(1) # 3 second delay

		if str(result.temperature) > 36.7 or str(result.humidity) > 70:
                  print 'Conditions too HIGH'
                  #Turn On LED and Buzzer
                  beep(2)
                  
                  
                elif str(result.temperature) < 36.5 or str(result.humidity) < 54:
                  print 'Conditions too LOW'
                  #Turn On LED and Buzzer
                  beep(2)

              
		getValue = GPIO.input(receiver_in)
                value = alpha * oldValue + (1 - alpha) * getValue
                change = value - oldValue    
                print(getValue)
                print 'BPM: '+str(value/0.01)
                oldValue = value
                olcChange = change
                breath = ((value/0.01)/5)
                pulse_rate = (value/0.01)
                print 'Breathing Rate: '+str(breath)
                sleep(period)
               
                lcd_string("PBM: "+str(value/0.01)+"",LCD_LINE_1)
		lcd_string("Res: "+str(breath)+"/20",LCD_LINE_2)
		sleep(period)
		
		#Connection to the Database
		#db = MySQLdb.connect('localhost','trevor','Avenger123!','pbm')
		#cursor = db.cursor()

		#prepare sql querry
		#sql = """INSERT INTO reading(body_temperature,environment_temperature,
                #pulse_rate,premor_id)
                #VALUES('temperature','temperature','pulse_rate','premor_id')"""

		#try:
                  #cursor.execute(sql)
                  #db.commit()
                #except:
                  #db.rollback()

                  #disconnect from server
                  #db.close()



def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  
  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def on():
  GPIO.output(Buzzer_sensor,GPIO.HIGH)
  print 'Buzzer On'

def off():
  GPIO.output(Buzzer_sensor,GPIO.LOW)
  print 'Buzzer Off'

def beep(x):
  on()
  time.sleep(x)
  off()
  time.sleep(x)
  

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
