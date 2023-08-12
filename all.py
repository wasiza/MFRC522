from RPLCD.i2c import CharLCD
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time

# Set up GPIO mode and define relay pin
GPIO.setmode(GPIO.BCM)
relay_pin = 18  # Change this to the actual GPIO pin connected to the relay

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Initialize the LCD
lcd = CharLCD('PCF8574', 0x27)

# Display initial message
lcd.clear()
lcd.write_string("Place card on")
lcd.crlf()
lcd.write_string("the reader...")

# Initialize the RFID reader
reader = SimpleMFRC522()

# Initialize relay state
relay_state = False

try:
    while True:
        id, text = reader.read()

        # Display the card information on the LCD
        lcd.clear()
        lcd.write_string(f"ID:{id}")
        lcd.crlf()
        lcd.write_string(f"{text}")

        if not relay_state:
            # Turn ON the relay when a card is detected
            GPIO.setup(relay_pin, GPIO.OUT)
            GPIO.output(relay_pin, GPIO.HIGH)
            relay_state = True
            print("Turning ON relay")
        else:
            # Turn OFF the relay when a card is detected again
            GPIO.setup(relay_pin, GPIO.OUT)
            GPIO.output(relay_pin, GPIO.LOW)
            relay_state = False
            print("Turning OFF relay")

        time.sleep(1)  # Wait for 1 second before updating the display

except KeyboardInterrupt:
    lcd.clear()
    lcd.write_string("Exiting...")
    time.sleep(2)
    lcd.clear()
    GPIO.cleanup()
