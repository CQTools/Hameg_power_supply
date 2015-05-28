#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 15:26:04 2015

@author: nick
"""

import sys
import glob
import serial
import json
import urllib2
import hameg_control as hc
from PyQt4 import QtGui, uic
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QPixmap
import datetime


form_class = uic.loadUiType("hamegcontrol.ui")[0] 

def serial_ports():
    
	"""Lists serial ports
	:raises EnvironmentError:
	On unsupported or unknown platforms
	:returns:
	A list of available serial ports
	"""				
	if sys.platform.startswith('win'):
		ports = ['COM' + str(i + 1) for i in range(256)]
	elif sys.platform.startswith('linux'):
	# this is to exclude your current terminal "/dev/tty"
		ports = glob.glob('/dev/serial/by-id/usb-H*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	
	else:
		raise EnvironmentError('Unsupported platform')
	
	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except serial.SerialException:
			pass
	return result
    




class MyWindowClass(QtGui.QMainWindow, form_class):
	connected = bool(False)
	hameg = None 
	time = 0


	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.ButtonOn_channel_1.clicked.connect(self.ButtonOn_channel1_clicked)# Bind the event handlers
		self.ButtonOn_channel_2.clicked.connect(self.ButtonOn_channel2_clicked)
		self.ButtonOn_channel_3.clicked.connect(self.ButtonOn_channel3_clicked)
		self.ButtonOn_channel_4.clicked.connect(self.ButtonOn_channel4_clicked)
		self.currentZero_1.clicked.connect(self.set_currentzero1)
		self.currentZero_2.clicked.connect(self.set_currentzero2)
		self.currentZero_3.clicked.connect(self.set_currentzero3)
		self.currentZero_4.clicked.connect(self.set_currentzero4)
		self.horizontalSlider_1.valueChanged.connect(self.slider_value_changed1)
		self.horizontalSlider_2.valueChanged.connect(self.slider_value_changed2)
		self.horizontalSlider_3.valueChanged.connect(self.slider_value_changed3)
		self.horizontalSlider_4.valueChanged.connect(self.slider_value_changed4)
		self.doubleSpinBox_1.editingFinished.connect(self.spinbox_value_changed1)
		self.doubleSpinBox_2.editingFinished.connect(self.spinbox_value_changed2)
		self.doubleSpinBox_3.editingFinished.connect(self.spinbox_value_changed3)
		self.doubleSpinBox_4.editingFinished.connect(self.spinbox_value_changed4)
		self.doubleSpinBox_volt1.editingFinished.connect(self.spinbox_value_changedvolt1)
		self.doubleSpinBox_volt2.editingFinished.connect(self.spinbox_value_changedvolt2)
		self.doubleSpinBox_volt3.editingFinished.connect(self.spinbox_value_changedvolt3)
		self.doubleSpinBox_volt4.editingFinished.connect(self.spinbox_value_changedvolt4)
		
		self.ButtonConnect.clicked.connect(self.ButtonConnect_clicked)
		self.comboSerialBox.addItems(serial_ports()) #Gets a list of avaliable serial ports to connect to and adds to combo box
		
		
	def ButtonConnect_clicked(self,connection):
		if not self.connected:
			self.hameg = hc.Hameg(str(self.comboSerialBox.currentText()))
			self.timer = QTimer()
			self.connected = True
			self.timer.timeout.connect(self.update)
			self.timer.start(500)
			self.control_label.setText('connected to ' + str(self.comboSerialBox.currentText()))
			self.hameg.set_voltage(1,7)
			self.hameg.set_voltage(2,7)
			self.hameg.set_voltage(3,7)
			self.hameg.set_voltage(4,7)
			self.current1 = float(self.hameg.get_current(1))
			self.current2 = float(self.hameg.get_current(2))
			self.current3 = float(self.hameg.get_current(3))
			self.current4 = float(self.hameg.get_current(4))
			self.horizontalSlider_1.setValue(int(25*self.current1))
			self.horizontalSlider_2.setValue(int(10*self.current2))
			self.horizontalSlider_3.setValue(int(10*self.current3))
			self.horizontalSlider_4.setValue(int(10*self.current4))
			self.doubleSpinBox_1.setValue(self.current1)
			self.doubleSpinBox_2.setValue(self.current2)
			self.doubleSpinBox_3.setValue(self.current3)
			self.doubleSpinBox_4.setValue(self.current4)
			

	def ButtonOn_channel1_clicked(self):
		if self.ButtonOn_channel_1.isChecked():
			self.hameg.output_on(1)
			self.ButtonOn_channel_1.setStyleSheet("background-color: green")
		else:
			self.hameg.output_off(1)
			self.ButtonOn_channel_1.setStyleSheet("background-color: red")

	def ButtonOn_channel2_clicked(self):
		if self.ButtonOn_channel_2.isChecked():
			self.hameg.output_on(2)
			self.ButtonOn_channel_2.setStyleSheet("background-color: green")
		else:
			self.hameg.output_off(2)
			self.ButtonOn_channel_2.setStyleSheet("background-color: red")

	def ButtonOn_channel3_clicked(self):
		if self.ButtonOn_channel_3.isChecked():
			self.hameg.output_on(3)
			self.ButtonOn_channel_3.setStyleSheet("background-color: green")
		else:
			self.hameg.output_off(3)
			self.ButtonOn_channel_3.setStyleSheet("background-color: red")

	def ButtonOn_channel4_clicked(self):
		if self.ButtonOn_channel_4.isChecked():
			self.hameg.output_on(4)
			self.ButtonOn_channel_4.setStyleSheet("background-color: green")
		else:
			self.hameg.output_off(4)
			self.ButtonOn_channel_4.setStyleSheet("background-color: red")
			
	def set_currentzero1(self):
		self.value = 0.0
		self.doubleSpinBox_1.setValue(self.value)
		self.horizontalSlider_1.setValue(int(self.value))
		self.hameg.set_current(1,self.value)
		
	def set_currentzero2(self):
		self.value = 0.0
		self.doubleSpinBox_2.setValue(self.value)
		self.horizontalSlider_2.setValue(int(self.value))
		self.hameg.set_current(2,self.value)

	def set_currentzero3(self):
		self.value = 0.0
		self.doubleSpinBox_3.setValue(self.value)
		self.horizontalSlider_3.setValue(int(self.value))
		self.hameg.set_current(3,self.value)
		
	def set_currentzero4(self):
		self.value = 0.0
		self.doubleSpinBox_4.setValue(self.value)
		self.horizontalSlider_4.setValue(int(self.value))
		self.hameg.set_current(4,self.value)
		
			
	def slider_value_changed1(self):
		self.value = float(self.horizontalSlider_1.value())*0.04
		self.doubleSpinBox_1.setValue(self.value)
		self.hameg.set_current(1,self.value)
	
	def slider_value_changed2(self):
		self.value = float(self.horizontalSlider_2.value())*0.1
		self.doubleSpinBox_2.setValue(self.value)
		self.hameg.set_current(2,self.value)
		
	def slider_value_changed3(self):
		self.value = float(self.horizontalSlider_3.value())*0.1
		self.doubleSpinBox_3.setValue(self.value)
		self.hameg.set_current(3,self.value)
		
	def slider_value_changed4(self):
		self.value = float(self.horizontalSlider_4.value())*0.1
		self.doubleSpinBox_4.setValue(self.value)
		self.hameg.set_current(4,self.value)
		

	def spinbox_value_changed1(self):
		self.value = self.doubleSpinBox_1.value()
		self.horizontalSlider_1.setValue(int(25*self.value))
		self.hameg.set_current(1,self.value)

		
	def spinbox_value_changed2(self):
		self.value = self.doubleSpinBox_2.value()
		self.horizontalSlider_2.setValue(int(10*self.value))
		self.hameg.set_current(2,self.value)

	def spinbox_value_changed3(self):
		self.value = self.doubleSpinBox_3.value()
		self.horizontalSlider_3.setValue(int(10*self.value))
		self.hameg.set_current(3,self.value)
		
	def spinbox_value_changed4(self):
		self.value = self.doubleSpinBox_4.value()
		self.horizontalSlider_4.setValue(int(10*self.value))
		self.hameg.set_current(4,self.value)
		
	def spinbox_value_changedvolt1(self):
		self.value = self.doubleSpinBox_1.value()
		self.hameg.set_voltage(1,self.value)

	def spinbox_value_changedvolt2(self):
		self.value = self.doubleSpinBox_volt2.value()
		self.hameg.set_voltage(2,self.value)

	def spinbox_value_changedvolt3(self):
		self.value = self.doubleSpinBox_volt3.value()
		self.hameg.set_voltage(3,self.value)
		
	def spinbox_value_changedvolt4(self):
		self.value = self.doubleSpinBox_volt4.value()
		self.hameg.set_voltage(4,self.value)
		
	def update(self):
		self.volt_labels = [self.volt_1,self.volt_2,self.volt_3,self.volt_4]
		self.current_labels = [self.current_1,self.current_2,self.current_3,self.current_4]
		for i in range(1,5,1):
			self.current = self.hameg.get_current(i)
			self.voltage = self.hameg.get_voltage(i)
			self.labelv = self.volt_labels[i-1]
			self.labelv.setText(str(self.voltage)+'V')
			self.labelc = self.current_labels[i-1]
			self.labelc.setText(str(self.current)+'A')


	
		
		

app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
