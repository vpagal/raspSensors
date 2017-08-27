###############################################################
# Author : Vasilis Pagalos (vpagal)
# email  : pagalosb@gmail.com
# Desc   : package for DHT-11 temperature and humidity sensor
###############################################################

import RPi.GPIO as GPIO

class DHT11:
	_error_code  = ''
	_temperature = -256
	_humidity    = 0
 
	def __init__(self, GPIOpin):
		# Constructor of DHT11 - set data pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(GPIOpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	def _getData():
		# Private method for get sensor data
		return

	def getTemperature(self):
		# Getter for temperature
		return self._temperature

	def getHumidity(self):
		# Getter for humidity
		return self._humidity