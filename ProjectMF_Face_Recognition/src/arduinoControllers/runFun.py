from led_controller import LEDController

class Runfun:
    def __init__(self):
        self.led_controller = LEDController(pin_number=2, duration=1)

    def do_LightLed(self):
        # Perform other tasks

        self.led_controller.start()  # Start the LEDController thread

        # Continue performing other tasks while the LED is on
        print("Continue performing other tasks while the LED is on")
        self.led_controller.join()  # Wait for the LEDController thread to finish

        print("Perform more tasks after the LED is turned off")
        # Perform more tasks after the LED is turned off

