import time
import struct
from bluetooth import ble

import util


class MyGATTRequester(ble.GATTRequester):
	_callback = None

	def on_notification(self, handle, data):
		self._callback(data[0])

	def on_indication(self, handle, data):
		if data != None and len(data) > 2:
			data = data[2:]

		self._callback(data.decode('utf-8'))

	def set_callback(self, callback):
		self._callback = callback


class BleUartDevice:
	address = ''
	gattRequester = None

	def __init__(self, address):
		self.address = address

	def connect(self):
		self.gattRequester = MyGATTRequester(self.address, False)
		self.gattRequester.connect(True, 'random')
		time.sleep(1)

	def readTemperature(self):
		temp = self.gattRequester.read_by_handle(0x27)
		# temp=self.gattRequester.read_by_uuid('e95d9250-251d-470a-a062-fa1922dfa9a8')
		temp = util.convertMicrobitValue(temp)
		return temp

	def enable_temperature_receive(self, callback):
		self.gattRequester.set_callback(callback)
		self.gattRequester.write_by_handle(0x28, b'\x01\x00')


	def disable_temperature_receive(self):
		self.gattRequester.write_by_handle(0x28, '\x00\x00')

	def readAccelerometer(self):
		# accelerometer = self.gattRequester.read_by_handle(27)
		accelerometer = self.gattRequester.read_by_uuid("e95dca4b-251d-470a-a062-fa1922dfa9a8")
		accelerometer = accelerometer[0]

		x_bytes = bytes([accelerometer[0], accelerometer[1]])
		y_bytes = bytes([accelerometer[2], accelerometer[3]])
		z_bytes = bytes([accelerometer[4], accelerometer[5]])

		x_short = struct.unpack('<h', x_bytes)[0]
		y_short = struct.unpack('<h', y_bytes)[0]
		z_short = struct.unpack('<h', z_bytes)[0]

		return [x_short / 1000.0, y_short / 1000.0, z_short / 1000.0]

	def send(self, strData):
		txData = util.marshalStringForBleUartSending(strData)
		self.gattRequester.write_by_handle(0x2a, txData)
		time.sleep(1)

	def enable_uart_receive(self, callback):
		self.gattRequester.set_callback(callback)
		self.gattRequester.write_by_handle(0x28, '\x02\x00')

	def disable_uart_receive(self, callback):
		self.gattRequester.set_callback(callback)
		self.gattRequester.write_by_handle(0x28, '\x00\x00')

	def disconnect(self):
		if self.gattRequester != None and self.gattRequester.is_connected():
			time.sleep(1)
			self.gattRequester.disconnect()
			self.gattRequester = None
			time.sleep(1)

# import time
# from bluetooth import ble
#
# import util
#
#
#
# class MyGATTRequester(ble.GATTRequester):
#
# 	_callback = None
#
#
#
# 	def on_notification(self, handle, data):
#
# 		self._callback(data[0])
#
#
#
# 	def on_indication(self, handle, data):
#
# 		if data != None and len(data) > 2:
#
# 			data = data[2:]
#
# 		self._callback(data.decode('utf-8'))
#
#
#
# 	def set_callback(self, callback):
#
# 		self._callback = callback
#
#
#
# class BleUartDevice:
#
# 	address = ''
# 	gattRequester = None
#
#
#
# 	def __init__(self, address):
#
# 		self.address = address
#
#
#
# 	def connect(self):
#
# 		self.gattRequester = MyGATTRequester(self.address, False)
# 		self.gattRequester.connect(True, 'random')
# 		time.sleep(1)
#
#
#
# 	def readTemperature(self):
#
# 		temp = self.gattRequester.read_by_handle(27)
#
# 		# print(temp)
# 		temp = util.convertMicrobitValue(temp)
# 		return temp
#
#
# 	def readAcc(self):
# 		temp = self.gattRequester.read_by_handle(27)
# 		test=temp[0]
# 		return temp[0]
#
#
#
# 	def enable_temperature_receive(self, callback):
#
# 		# self.gattRequester.set_callback(callback)
# 		self.gattRequester.write_by_handle(0x28, '\x01\x00')
#
#
#
# 	def disable_temperature_receive(self):
#
# 		self.gattRequester.write_by_handle(0x28, '\x00\x00')
#
#
#
# 	def send(self, strData):
#
# 		txData = util.marshalStringForBleUartSending(strData)
# 		self.gattRequester.write_by_handle(0x2a, txData)
# 		time.sleep(1)
#
# 	# def receive(self):
# 	# 	rxd = self.gattRequester.read_by_handle(0x27)
# 	# 	rxd = util.convertMicrobitValue(rxd)
# 	# 	return rxd
#
# 	def enable_uart_receive(self, callback):
#
# 		self.gattRequester.set_callback(callback)
# 		self.gattRequester.write_by_handle(0x28, '\x02\x00')
# 		# self.gattRequester.write_by_handle(0x28, '\x02')
#
# 	def disable_uart_receive(self, callback):
#
# 		self.gattRequester.set_callback(callback)
# 		self.gattRequester.write_by_handle(0x28, '\x00\x00')
#
#
# 	def disconnect(self):
#
# 		if self.gattRequester != None and self.gattRequester.is_connected():
#
# 			time.sleep(1)
# 			self.gattRequester.disconnect()
# 			self.gattRequester = None
# 			time.sleep(1)
