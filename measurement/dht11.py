###############################################################
# Author : Vasilis Pagalos (vpagal)
# email  : pagalosb@gmail.com
# Desc   : package for DHT-11 temperature and humidity sensor
###############################################################

import RPi.GPIO as GPIO
import time

class DHT11:
	_gpio_pin    = -1
	_error_code  = ''
	_temperature = -256
	_humidity    = 0
 
	def __init__(self, GPIOpin):
		# Constructor of DHT11 - set data pin
		self._gpio_pin = GPIOpin

	def _getData(self):
		# Private method for get sensor data
		# we will need first to send a high and then a low
		# then we can get data listening on the same pin
		# first set pin as out and then set it as input
		GPIO.setmode(GPIO.BCM)

		# set it as output. we will have to send a high and a low
		GPIO.setup(self._gpio_pin, GPIO.OUT)

		GPIO.output(self._gpio_pin,GPIO.HIGH)
		sleep(0.05)

		GPIO.output(self._gpio_pin,GPIO.LOW)
		sleep(0.02)

		# set it as input in order to read data from dht11
		GPIO.setup(self._gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		# get data
		raw_data = self._collect_data()

		# parse data taken
		data = self._parse_data()

		return

	def _collect_data(self):
		unchanged_cnt     = 0
		max_unchanged_cnt = 100

		last_bit = -1
		data     = []

		while True:
			set current = GPIO.input(self._gpio_pin)
			if current != last:
				unchanged_cnt = 0
				last = current
			else:
				unchanged_cnt += 1
				if unchanged_cnt > max_unchanged_cnt:
					break

		return data

	def _parse_data(self):
		return ''

	def getTemperature(self):
		# Getter for temperature
		return self._temperature

	def getHumidity(self):
		# Getter for humidity
		return self._humidity
