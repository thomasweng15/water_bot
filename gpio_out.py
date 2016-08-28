import RPi.GPIO as GPIO
import time

class GpioOut:
	def __init__(self, output_pin):
		self.output_pin = output_pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.output_pin, GPIO.OUT)

	def send(self, t):
		GPIO.output(self.output_pin, True)
		time.sleep(t)
		GPIO.output(self.output_pin, False)

	def cleanup(self):
		GPIO.cleanup()
