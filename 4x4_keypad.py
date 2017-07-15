# try running for me the code for a 4x4 keypad
# this python code is for a 4*4 keypad which outputs either a letter or number when pressed
# taking a consideration that the first four pins are rows and the last four pins are columns

import RPi.GPIO as GPIO

GPIO.setmode(GPIO, BCM)

MATRIX = [[1,2,3,'A'],  
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*', 0, '#', 'D']]  # created a matrix for the values and letters on a keypad

ROW = [11,12,13,15]  #GPIO pins for the rows 
COL = [23,24,25,27]  #GPIO pins for the columns 

for j in range(4):   # in the for loop each of the four outputs is defined and set HIGH (1)  
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1) 

for i range(4):  # also the four row pins are also setup as input  
    GPIO.seetup(ROW[i], GPIO.IN) 

# the program will continue forever untill the input pins are pressed

try:
    while (True):
        for j in range(4):
            GPIO.output(COL[j], 0) # set each of the output pins for the columns to low one at a time
            for i in range[4]:
                if GPIO.input(ROW[i] == 0: # if a button is pressed
                    print MATRIX[i][j]     # print a value as long as a button is pressed
                    while(GPIO.input(ROW[1]) == 0):  # this while loop prevents a value to be printed multiple times is a button is pressed for a long time
                        pass  
            GPIO.output(COL[j], 1) # setting the output pin to high 

except KeyboardInterrupt:
    GPIO.cleanup()            
