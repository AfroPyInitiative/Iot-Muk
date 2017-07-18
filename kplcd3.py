import RPi.GPIO as GPIO
import RPLCD
from time import sleep
from operator import eq

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13
LCD_D5 = 17
LCD_D6 = 27
LCD_D7 = 22

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

MATRIX = [[1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'#','D'] ]

ROW = [18,23,24,25]
COL = [12,16,21,20]

for j in range (4):
    GPIO.setup(COL[j],GPIO.OUT)
    GPIO.output(COL[j],1)

for i in range (4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

def matrix():
    main()
  
    while (True):
        for j in range (4):
            GPIO.output(COL[j],0)
            for i in range (4):
                if GPIO.input(ROW[i]) == 0:
                    lcd_string("NO:"+str(MATRIX [i][j])+"",LCD_LINE_1)#comment out?
                    x= MATRIX [i][j]
                    for i in range(5):#5 or more
                        password=[2,3,1,4]
                        data=[]
                        data.append(x)
                        if len(data)<5:
                            lcd.cursor_mode = CursorMode.line#comment out?
                            lcd_string(str(x),LCD_LINE_2)
                            lcd.cursor_pos(2,i)
                        else:
                            if any(map(eq,password,data))== True:#GIVES BOOLEAN OF TRUE OR FALSE
                                print 'ACCESS GRANTED'
                            else:
                                print 'ACCESS DENIED'
                            
                        
                    
                    #lcd_string("CLICKED :"+str(MATRIX [i][j])+"",LCD_LINE_2)
                    #sleep(5)
                    #lcd_byte(0x01,LCD_CMD)
                    #if str(MATRIX[i][j])=="1":
                        #lcd_string("GADHETS",LCD_LINE_1)
                    
                        
                    #elif str(MATRIX[i][j])=="2":
                        
                        #lcd_string("LIGHTS:",LCD_LINE_1)
               


                        
                    

                    while (GPIO.input(ROW[i]) == 0):
                        pass
            GPIO.output(COL[j],1)
    time.sleep(1)



    
def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  
  GPIO.setup(LCD_E, GPIO.OUT)  # Enable
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7



    
  # Initialise display
  lcd_init()

 
      
		
		
		
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





 
if __name__ == '__main__':

  try:
    matrix()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
