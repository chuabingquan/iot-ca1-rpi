# Import relevant packages
from gpiozero import MCP3008
from time import sleep
import paho.mqtt.publish as publish

# Instantiate ADC to listen on channel 0
adc = MCP3008(channel=0)

# Other Declarations
mqttBrokerUrl = '192.168.1.8';

# Run infinite loop to constantly get inputs from FC-109 Microphone Amplifier via MCP3008 ADC
while True:
	# Read FC-109 input and format to 2 decimal places
	soundInput = format(float(adc.value * 1024), '.2f')

	# Print out input
	print('Value: ' + soundInput)

	# Publish input to MQTT Broker
	# Topic is 'soundInput'
	print('Publishing to MQTT Broker...')
	publish.single('soundInput', soundInput, hostname = mqttBrokerUrl)
	print('Published to MQTT Broker!')

	# Sleep/Wait for 3 seconds before looping again 
	sleep(3)




	# ---------------------------------------------------Old obselete testing code ---------------------------------------------------

    # old = adc.value
	# new = adc.value
	# print("Old: ", old*1024)
	# print("New: ", new*1024)
	# print("Diff: ", (new - old)*1024)
    #     sleep(1)
	#
	# Read in a single value
	# inputSample = adc.value * 1024
	#
	# Get the minimum and maximum value
	# inputMin = min(inputMin, inputSample)
	# inputMax = max(inputMax, inputSample)
	#
	# Print out values
	# print("Input Value:", inputSample)
	# print("Min:", inputMin)
	# print("Max:", inputMax)
	# print("Difference:", (inputMax-inputMin))
	# print("----End of Result----")
	# sleep(5)
