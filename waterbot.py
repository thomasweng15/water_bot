# Must run as root on rpi

from datetime import datetime
from twilio_client import TwilioClient
import RPi.GPIO as GPIO
import time
import json
import sys

TIME=2
OUTPUT_PIN = 17
CONFIG = "config.json"
PRIVATE_CONFIG = "private_config.json"

class WaterBot:
	def __init__(self, output_pin, config, private_config):
		self.config = self._get_config(config);
		self.private_config = self._get_private_config(private_config);
		self.tw_client = TwilioClient(
			self.config["account_sid"], 
			self.private_config["auth_token"]
		)		
		self._init_gpio(output_pin)

	def water(self):
#		self._gpio_out()
		self._send_text()

	def cleanup(self):
		GPIO.cleanup()

	def _gpio_out(self, t=TIME):
		GPIO.output(OUTPUT_PIN, True)
		time.sleep(t)
		GPIO.output(OUTPUT_PIN, False)

	def _send_text(self):
		self.tw_client.send(
			self.private_config["receive_number"],
			self.private_config["send_number"],
			self.config["msg_body"]
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
