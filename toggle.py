#!/usr/bin/env python

import pigpio

pi = pigpio.pi() # Connect to local Pi.

GPIOS=[17]

# make sure pins are outputs and toggle level

for g in GPIOS:
   pi.set_mode(g, pigpio.OUTPUT)
   if pi.read(g):
      print("Input on GPIO{} is HIGH...setting to LOW".format(g))
      pi.write(g, 0)
   else:
      print("Input on GPIO{} is LOW...setting to HIGH".format(g))
      pi.write(g, 1)

pi.stop() # Disconnect from local Pi.
