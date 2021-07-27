from urllib3 import PoolManager
import json
import time
import paho.mqtt.publish as publish

# from paho.mqtt import subscribe
#
# channelID = "1455110"
#
# apiKey = "DJ52R1IHM38DHRUH"
#
# useUnsecuredTCP = False
#
# useUnsecuredWebsockets = False
#
# useSSLWebsockets = True
#
# mqttHost = "mqtt.thingspeak.com"
# # Set up the connection parameters based on the connection type
# if useUnsecuredTCP:
#     tTransport = "tcp"
#     tPort = 1883
#     tTLS = None
# if useUnsecuredWebsockets:
#     tTransport = "websockets"
#     tPort = 80
#     tTLS = None
# if useSSLWebsockets:
#     import ssl
#     tTransport = "websockets"
#     tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
#     tPort = 443
# # Create the topic string
# topic = "channels/" + channelID + "/subscribe/" + apiKey
# # Run a loop which calculates the system performance every
# #   20 seconds and published that to a ThingSpeak channel
# #   using MQTT.
#
#
# def on_message_print(client, userdata, message):
#     print("%s %s" % (message.topic, message.payload))
#
#
#
# subscribe.callback(on_message_print, topic, hostname=mqttHost)




READ_API_KEY='DJ52R1IHM38DHRUH'
CHANNEL_ID= '1455110'


http = PoolManager()


while True:
    try:
        TS = http.request('GET',"http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (CHANNEL_ID,READ_API_KEY))

        response = TS.data
        data=json.loads(response)


        a = data['created_at']
        b = data['field1']
        print(b)
        time.sleep(5)

        TS.close()
    except :
        print('error with thingspeak.')
        TS.close()