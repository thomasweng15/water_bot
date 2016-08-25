# Must run as root on rpi

from twilio.rest import TwilioRestClient
import RPi.GPIO as GPIO
import time
import json

OUTPUT_PIN = 11

class WaterBot:
	def __init__(self, output_pin):
		self.config = self._get_config();
		self.tw_client = self._init_twilio()		
		self._init_gpio(output_pin)

	def water(self):
		self._gpio_out()
		# self._send_text()
		
	def _gpio_out(self, t=5):
		GPIO.output(OUTPUT_PIN, True)
		time.sleep(t)
		GPIO.output(OUTPUT_PIN, False)
		GPIO.cleanup()

	def _send_text(self):
		message = self.tw_client.messages.create(
			to=self.config["receive_number"],
			from_=self.config["send_number"],
			body=self.config["msg_body"]
		)

		print self.config["msg_body"]

	def _init_twilio(self):
		self.auth_token = self._get_token();
		return TwilioRestClient(self.config["account_sid"], self.auth_token)

	def _get_config(self):
		with open("config.json", "r") as f:
			config = f.read().strip()
		return json.loads(config)

	def _get_token(self):
		with open("auth_token.txt", "r") as f:
			token = f.read().strip()
		return token	

	def _init_gpio(self, output_pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(output_pin, GPIO.OUT)	

w = WaterBot(OUTPUT_PIN)
w.water()
