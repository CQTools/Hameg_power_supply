# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 17:23:06 2015

@author: Nick Lewty

Python software for communicating with Hameg power supply

Simple serial communication based on GPIB commands

For more info on commands see data sheet

http://www.hameg.com/manuals.0.html?&no_cache=1&tx_hmdownloads_pi1[mode]=download&tx_hmdownloads_pi1[uid]=7465 

"""

import serial

class Hameg(object):
	baudrate = 115200
	
	def __init__(self, port):
		self.serial = self._open_port(port)
		
	def _open_port(self, port):
		ser = serial.Serial(port, self.baudrate, timeout=1)
		ser.readline()
		ser.timeout = 1
		return ser
		
	def _serial_write(self, string):
		self.serial.write(string + '\n')
		
	def _serial_read(self):
		msg_string = self.serial.readline()
		# Remove any linefeeds etc
		msg_string = msg_string.rstrip()
		return msg_string
	
	def reset(self):
		self._serial_write('*RST')
		
	def serial_number(self):
		self._serial_write('*IDN?')
		return self._serial_read()
		
	def set_voltage(self,channel,value):
		self._serial_write('INST OUT'+str(channel))
		self._serial_write('VOLT ' + str(value))
		
	def get_voltage(self,channel):
		self._serial_write('INST OUT'+str(channel))
		self._serial_write('MEAS:VOLT?')
		return self._serial_read()
		
	def set_current(self,channel,value):
		self._serial_write('INST OUT'+str(channel))
		self._serial_write('CURR ' + str(value))
		
	def get_current(self,channel):
		self._serial_write('INST OUT'+str(channel))
		self._serial_write('MEAS:CURR?')
		return self._serial_read()
	
	def output_on(self,channel):
		self._serial_write('INST OUT'+str(channel))
		self._serial_write('OUTP ON')
		
	def output_off(self,channel):
		self._serial_write('INST OUT'+str(channel))
		self._serial_write('OUTP OFF')