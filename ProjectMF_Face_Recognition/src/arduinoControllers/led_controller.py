import pyfirmata2
import threading
import time

class LEDController(threading.Thread):
    def __init__(self, pin_number, duration):
        super(LEDController, self).__init__()
        self.pin_number = pin_number
        self.duration = duration
        self.board = None
        self.led_pin = None

    def run(self):
        self.board = pyfirmata2.Arduino("COM10")
        self.led_pin = self.board.get_pin(f"d:{self.pin_number}:o")

        self.led_pin.write(1)  # Turn on the LED
        time.sleep(self.duration)  # Keep the LED on for the specified duration
        self.led_pin.write(0)  # Turn off the LED

        self.board.exit()