#!/usr/bin/python
# Author: Skyler Ogden

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import Adafruit_DHT
import pigpio
from time import sleep
import logging



pi = pigpio.pi()

heater_pin = 27
sensor_pin = 17
sensor_type = 22    # DHT22

# Parse command line parameters.

if len(sys.argv) == 2:
	tempSet = float(sys.argv[1])
else:
	print 'usage: sudo $1 <desired temperature (F)>'
	print 'example: sudo $1 80F #set control temperature to 80F'
	sys.exit(1)

logging.basicConfig(level=logging.INFO,
                    filename='heaterloop.log', # log to this file
                    format='%(asctime)s %(message)s') # include timestamp

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).


# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

pi.write(heater_pin,0)
while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor_type, sensor_pin)

	if humidity is not None and temperature is not None:
		temperature = temperature * 9/5.0 + 32
		logging.info('%dF/%dF Heater:%s' % (temperature, tempSet, pi.read(heater_pin)))
		print '%dF/%dF' % (temperature, tempSet)
		hum = 'Humidity = %f'.format(humidity)
		print hum

		if temperature < tempSet and pi.read(heater_pin) == False:
			print '==== Now Heating ===='
			pi.write(heater_pin,1)	#Enable

		elif temperature >= tempSet:
			if pi.read(heater_pin) == True:
				print '==== Heater Disabled ===='
				pi.write(heater_pin,0)
			break

	else:
		print 'Failed to get reading. Try again! (Heater Disabled)'
		pi.write(heater_pin,0)
		sys.exit(1)
	sleep(2)










