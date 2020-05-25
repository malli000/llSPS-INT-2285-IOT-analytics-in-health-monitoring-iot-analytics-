import time
import sys
import ibmiotf.application
import ibmiotf.device
import random#node-red apitoken R0!0YdZ90ot8hEc7g6
#Provide your IBM Watson Device Credentials
organization = "azu7j9" #azu7j9
deviceType = "raspberrypi"#raspberrypi
deviceId = "123456"#123456
authMethod = "token"
authToken = "12345678"#12345678

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        pul=random.randrange(40,100,4)
        #print(pulse)
        temp = random.randrange(75,105,2)
        sys=random.randrange(100,141,2)
        dia=random.randrange(60,101,2)
        #Send Temperature & pulse to IBM Watson
        data = { 'Temperature' : temp, 'Pulse': pul ,"Sys":sys,"Dia":dia}
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %d F" % temp, "Pulse = %d" % pul,"Blood Pressure = %d/" % sys,"%d"% dia, "to IBM Watson")

        success = deviceCli.publishEvent("Health Monitoring", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback #subscription

# Disconnect the device and application from the cloud
deviceCli.disconnect()
