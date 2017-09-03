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

	# Start of public methods

	def loadData(self):
		# Private method for get sensor data
		# we will need first to send a high and then a low
		# then we can get data listening on the same pin
		# first set pin as out and then set it as input
		GPIO.setmode(GPIO.BCM)

		# set it as output. we will have to send a high and a low
		GPIO.setup(self._gpio_pin, GPIO.OUT)

		GPIO.output(self._gpio_pin,GPIO.HIGH)
		time.sleep(0.05)

		GPIO.output(self._gpio_pin,GPIO.LOW)
		time.sleep(0.02)

		# set it as input in order to read data from dht11
		GPIO.setup(self._gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		# get data
		raw_data = self._collect_data()

		if len(raw_data) == 0:
			print("ERROR : No data returned!!")
			return

		# parse data taken
		pull_up_lengths = self.__parse_data_pull_up_lengths(raw_data)

		# if bit count mismatch, return error (4 byte data + 1 byte checksum)
		if len(pull_up_lengths) != 40:
			print ("ERROR : Missing data!!")
			return

		# calculate bits from lengths of the pull up periods
		bits = self.__calculate_bits(pull_up_lengths)

		# we have the bits, calculate bytes
		the_bytes = self.__bits_to_bytes(bits)

		# calculate checksum and check
		checksum = self.__calculate_checksum(the_bytes)
		if the_bytes[4] != checksum:
			print ("ERROR : No checksum match!!")
			return

		# Now we are done so populate the relevant variable with their values
		self._temperature = the_bytes[2]
		self._humidity    = the_bytes[0]

		return

	def getTemperature(self):
		# Getter for temperature
		return self._temperature

	def getHumidity(self):
		# Getter for humidity
		return self._humidity

	# End of public methods

	# Start of private methods

	def _collect_data(self):
		unchanged_cnt     = 0
		max_unchanged_cnt = 100

		last = -1
		data = []

		while True:
			current = GPIO.input(self._gpio_pin)
			data.append(current)
			if current != last:
				unchanged_cnt = 0
				last = current
			else:
				unchanged_cnt += 1
				if unchanged_cnt > max_unchanged_cnt:
					break

		return data

	#def _parse_data(self, data):
	#	return ''

	##########################################################################################
	# External libraries
	# Taken from other github contributor : szazo
	##########################################################################################
	def __parse_data_pull_up_lengths(self, data):
		STATE_INIT_PULL_DOWN = 1
		STATE_INIT_PULL_UP = 2
		STATE_DATA_FIRST_PULL_DOWN = 3
		STATE_DATA_PULL_UP = 4
		STATE_DATA_PULL_DOWN = 5

		state = STATE_INIT_PULL_DOWN

		lengths = [] # will contain the lengths of data pull up periods
		current_length = 0 # will contain the length of the previous period

		for i in range(len(data)):
			current = data[i]
			current_length + 1

			if state == STATE_INIT_PULL_DOWN:
				if current == GPIO.LOW:
					# ok, we got the initial pull down
					state = STATE_INIT_PULL_UP
					continue
				else:
					continue
			if state == STATE_INIT_PULL_UP:
				if current == GPIO.HIGH:
					# ok, we got the initial pull up
					state = STATE_DATA_FIRST_PULL_DOWN
					continue
				else:
					continue
			if state == STATE_DATA_FIRST_PULL_DOWN:
				if current == GPIO.LOW:
					# we have the initial pull down, the next will be the data pull up
					state = STATE_DATA_PULL_UP
					continue
				else:
					continue
			if state == STATE_DATA_PULL_UP:
				if current == GPIO.HIGH:
					# data pulled up, the length of this pull up will determine whether it is 0 or 1
					current_length = 0
					state = STATE_DATA_PULL_DOWN
					continue
				else:
					continue
			if state == STATE_DATA_PULL_DOWN:
				if current == GPIO.LOW:
					# pulled down, we store the length of the previous pull up period
					lengths.append(current_length)
					state = STATE_DATA_PULL_UP
					continue
				else:
					continue
		return lengths

	def __calculate_bits(self, pull_up_lengths):
		# find shortest and longest period
		shortest_pull_up = 1000
		longest_pull_up  = 0
		for i in range(0, len(pull_up_lengths)):
			length = pull_up_lengths[i]
			if length < shortest_pull_up:
				shortest_pull_up = length
			if length > longest_pull_up:
				longest_pull_up = length

		# use the halfway to determine whether the period it is long or short
		halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up) / 2
		bits = []

		for i in range(0, len(pull_up_lengths)):
			bit = False
			if pull_up_lengths[i] > halfway:
				bit = True
			bits.append(bit)

		return bits

	def __bits_to_bytes(self, bits):
		the_bytes = []
		byte = 0
		for i in range(0, len(bits)):
			byte = byte << 1
			if (bits[i]):
				byte = byte | 1
			else:
				byte = byte | 0
			if ((i + 1) % 8 == 0):
				the_bytes.append(byte)
				byte = 0
		return the_bytes

	def __calculate_checksum(self, the_bytes):
		return the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3] & 255

	##########################################################################################
	# End of external libraries
	##########################################################################################

	# End of private methods
