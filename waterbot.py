# Must run as root on rpi

from twilio_client import TwilioClient
from gpio_out import GpioOut
import json
import sys

TIME=2
OUTPUT_PIN = 17
CONFIG = "config.json"
PRIVATE_CONFIG = "private_config.json"

class WaterBot:
	def __init__(self, output_pin, config, private_config):
		self._config = self._get_config(config);
		self._private_config = self._get_private_config(private_config);
		self._tw_client = TwilioClient(
			self._config["account_sid"], 
			self._private_config["auth_token"]
		)		
		self._gpio = GpioOut(output_pin)

	def water(self):
		self._gpio.send(TIME)
		self._tw_client.send(
			self._private_config["receive_number"],
			self._private_config["send_number"],
			self._config["msg_body"]
		)

	def cleanup(self):
		self._gpio.cleanup()

	def _get_config(self, config):
		with open(config, "r") as f:
			config = f.read().strip()
		return json.loads(config)

	def _get_private_config(self, private_config):
		with open(private_config, "r") as f:
			private = f.read().strip()
		return json.loads(private)	

if len(sys.argv) >= 2:
	CONFIG = sys.argv[1]

if len(sys.argv) >= 3:
	PRIVATE_CONFIG = sys.argv[2]

w = WaterBot(OUTPUT_PIN, CONFIG, PRIVATE_CONFIG)
w.water()
w.cleanup()
