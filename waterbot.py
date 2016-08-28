# Must run as root on rpi

from twilio.rest import TwilioRestClient
from datetime import datetime
import RPi.GPIO as GPIO
import time
import json
import sys

OUTPUT_PIN = 17
CONFIG = "config.json"
PRIVATE_CONFIG = "private_config.json"

class WaterBot:
	def __init__(self, output_pin, config, private_config):
		self.config = self._get_config(config);
		self.private_config = self._get_private_config(private_config);
		self.tw_client = self._init_twilio()		
		self._init_gpio(output_pin)

	def water(self):
		self._gpio_out()
 		self._send_text()
		
	def cleanup(self):
		GPIO.cleanup()

	def _gpio_out(self, t=2):
		GPIO.output(OUTPUT_PIN, True)
		time.sleep(t)
		GPIO.output(OUTPUT_PIN, False)

	def _send_text(self):
		message = self.tw_client.messages.create(
			to=self.private_config["receive_number"],
			from_=self.private_config["send_number"],
			body=self.config["msg_body"]
		)

		print datetime.now().time() + " " + self.config["msg_body"]

	def _init_twilio(self):
		return TwilioRestClient(
			self.config["account_sid"], 
			self.private_config["auth_token"]
		)

	def _get_config(self, config):
		with open(config, "r") as f:
			config = f.read().strip()
		return json.loads(config)

	def _get_private_config(self, private_config):
		with open(private_config, "r") as f:
			private = f.read().strip()
		return json.loads(private)	

	def _init_gpio(self, output_pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(output_pin, GPIO.OUT)	


if len(sys.argv) >= 2:
	CONFIG = sys.argv[1]

if len(sys.argv) >= 3:
	PRIVATE_CONFIG = sys.argv[2]

w = WaterBot(OUTPUT_PIN, CONFIG, PRIVATE_CONFIG)
w.water()
w.cleanup()
