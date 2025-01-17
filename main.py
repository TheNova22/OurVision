import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from state import State
from button_handler import ButtonHandler
from audio import play_audio
import os
from tests import Test
from time import sleep
from tts import tts

focus=162
value = (focus<<4) & 0x3ff0
dat1 = (value>>8)&0x3f
dat2 = value & 0xf0
os.system("i2cset -y 22 0x0c %d %d" % (dat1,dat2))

cycle_pin=11
select_pin=13
cancel_pin=15

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(cycle_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(select_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(cancel_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(cycle_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(select_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(cancel_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge

print("models Loaded")
play_audio("DocumentOCRMode.mp3")
debug = True
if __name__ == "__main__":
    handler = ButtonHandler()
    #handler.select()
    sleep(5)
    while True:
        if debug:inp = int(input("option 1,2 or 3:"))
        if (debug and inp == 1) or GPIO.event_detected(cycle_pin):
            print('cycle_pin_pushed')
            handler.cycle()
            print(f"Currently in {State.name(handler.state)} mode")

        if (debug and inp == 2) or GPIO.event_detected(select_pin):
            print(f"Currently in {State.name(handler.state)} mode")
            print('select_pin_pushed')
            handler.select()

        if (debug and inp == 3) or GPIO.event_detected(cancel_pin):
            print('cancel_pin_pushed')
            handler.cancel()

    GPIO.cleanup() # Clean up
