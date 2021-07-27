import serial
import time

# ThingSpeak Update Using MQTT
# Copyright 2016, MathWorks, Inc
# This is an example of publishing to multiple fields simultaneously.
# Connections over standard TCP, websocket or SSL are possible by setting
# the parameters below.
#
# CPU and RAM usage is collected every 20 seconds and published to a
# ThingSpeak channel using an MQTT Publish
#
# This example requires the Paho MQTT client package which
# is available at: http://eclipse.org/paho/clients/python

import paho.mqtt.publish as publish
###   Start of user configuration   ###
#  ThingSpeak Channel Settings
# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = "1455110"
# The Write API Key for the channel
# Replace this with your Write API key
apiKey = "OPDIOP04L8MTHPGF"
#  MQTT Connection Methods
# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system resources.
useUnsecuredTCP = False
# Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False
# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resources, but the connection
# will be secured by SSL.
useSSLWebsockets = True
###   End of user configuration   ###
# The Hostname of the ThinSpeak MQTT service
mqttHost = "mqtt.thingspeak.com"
# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None
if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None
if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443
# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey
# Run a loop which calculates the system performance every
#   20 seconds and published that to a ThingSpeak channel
#   using MQTT.

ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)

while(True):
    # get the system performance data
    msg = ser.readline()
    smsg = msg.decode('utf-8').strip()
    if len(smsg) > 0:
        print('RX:{}'.format(smsg))
        # build the payload string
        tPayload = "field1=" + str(smsg)
        # attempt to publish this data to the topic
        try:
            publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
            time.sleep(15)
        except (KeyboardInterrupt):
            break
        except:
            print ("There was an error while publishing the data.")



# try:
#
#     print("Listening on /dev/ttyACM0... Press CTRL+C to exit")
#
#     ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
#
#     response = input('commend: ')
#     ser.write(str.encode(response))
#     while True:
#         msg = ser.readline()
#         smsg = msg.decode('utf-8').strip()
#         if len(smsg) > 0:
#             print('RX:{}'.format(smsg))
#
#         time.sleep(1)
#
# except KeyboardInterrupt:
#
#     if ser.is_open:
#         ser.close()
#
#     print("Program terminated!")