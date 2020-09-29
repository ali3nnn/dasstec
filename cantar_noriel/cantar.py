import serial
import os
import requests
import paho.mqtt.client as mqtt

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=.1)

client = mqtt.Client()


while True:
	data = ser.readline();
	if data:
		weight = 0
		try:
			if weight < 2000:
				weight = float(data.rstrip()) * 0.96
			if weight > 2000 and weight < 4000:
				weight = float(data.rstrip()) * 0.98
			if weight > 4001 and weight < 5000:
				weight = float(data.rstrip()) * 0.99 - 15
			if weight > 5001 :
                                weight = float(data.rstrip()) * 0.99 + 30
				weight = weight + 30
		except:
			pass
		client.connect("192.168.5.254", 1883, 60)
		if os.path.getsize("/home/pi/Desktop/cantar/barcode.txt")>1:
			file = open("/home/pi/Desktop/cantar/barcode.txt","r")
			box_code = file.read()
			box_code = box_code.rstrip()
			file.close()
			file = open("/home/pi/Desktop/cantar/barcode.txt","w")
			file.write("")
			file.close()
			print str(int(weight)) +  " "  + box_code
			jsn = '{"barcode":"'+box_code+'","weight":'+str(int(weight))+'}'
			client.publish("noriel/scale/out",jsn)
		#else:
		#	box_code = "ERROR"
		#	print str(int(weight)) +  " "  + "ERROR"
		#	jsn = '{"barcode":"ERROR","weight":'+str(int(weight))+'}'
		#	client.publish("noriel/scale/out",jsn)
			link = 'https://anysensor.dasstec.ro/api/v2/send-scale-recordings?username=noriel&barcode="'+box_code+'"&weight='+str(int(weight))
			x = requests.get(link)
			print (x.status_code)
