# Import relevant packages
from gpiozero import MCP3008, LED
from time import sleep
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json

# Declarations
adc = MCP3008(channel=0)
led = LED(18)
mqttBrokerUrl = '169.254.222.34';

# Define callback function for connecting to Broker
def on_connect(client, userdata, flags, rc):
    m = "Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id  "+str(client)
    print(m)

# Define callback function for recieving subscribed information
def on_message(client, userdata, message):
	print('From Web Application:\n')
	msg = str(message.payload.decode("utf-8"))
	print('Received: ' + msg)

	deserialized = json.loads(msg)
	type = deserialized['type']
	status = deserialized['status']

	if type == 'led':
		if status == 'on':
			ledON()
			print('LED turned ON from Web Application\n')
			sleep(20)
		elif status == 'off':
			ledOFF()
			print('LED turned OFF from Web Application\n')


# Instantiate MQTT client
client = mqtt.Client('rpi')
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttBrokerUrl)
client.loop_start()
client.subscribe('toggle')


# Define led blink function
def ledON():
	led.blink()
	print('LED is blinking.')


# Define led off function
def ledOFF():
	led.off()
	print('LED is off.')


# Run infinite loop to constantly get inputs from FC-109 Microphone Amplifier via MCP3008 ADC
while True:
	# Read FC-109 input and format to 2 decimal places
	soundInput = format(float(adc.value * 1024), '.2f')

	ledStatus = False;

	# Print out input
	print('Value: ' + soundInput)

	val = int(round(float(soundInput)))

	if val > 450:
		ledON()
		ledStatus = True
		print('Sound Input > 450, LED On')
		sleep(5)
	else:
		ledOFF()
		ledStatus = False
		print('Sound Input < 450, LED Off')

	# Publish input to MQTT Broker
	# Topic is 'soundInput'
	print('Publishing to MQTT Broker...')
	publish.single('soundInput', '{ "soundValue": ' + soundInput + ', "ledStatus": ' + str(ledStatus).lower() + ' }', hostname = mqttBrokerUrl)
	print('Published to MQTT Broker!\n')

	# Sleep/Wait for 3 seconds before looping again
	sleep(3)
