import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

import firebase_admin, datetime, time, multiprocessing
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firesbaseraspberry-firebase-adminsdk-mcq96-8e311d5c7e.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def motor(rotate):
  step_seq_num=0 
  for i in range(4096):
   for pin in range(0,4):
     Pattern_Pin=control_pins[pin]
     if halfstep_seq[step_seq_num][pin]==1:
       GPIO.output(Pattern_Pin,True)
     else :
       GPIO.output(Pattern_Pin,False)
   step_seq_num+=rotate
   if (step_seq_num >=8):
     step_seq_num=0
   elif step_seq_num < 0 :
     step_seq_num=7
   time.sleep(0.001)

def ouvrir():
  while True:
    motor(1)



def fermer():
  while True:
    motor(-1)

def default():
  while True:
    continue

proc = multiprocessing.Process(target=default, args=())
proc.start()

GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]
j=0
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
step_seq_num=0
rot_spd=0.001
rotate=4096

halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ENIT_STR")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global proc
    
    a=str(msg.payload.decode('UTF-8'))
    print(msg.topic+" "+a)
    if a == "ouvrir" :
      proc.terminate()
      proc = multiprocessing.Process(target=ouvrir, args=())
      proc.start()
      uploadHistroy(a)
      
       
    if a == "arrêter" :
      rotate_dir=0
      proc.terminate()
      motor(rotate_dir)
      uploadHistroy(a)  
 
            
    if a == "fermer" :
      proc.terminate()
      proc = multiprocessing.Process(target=fermer, args=())
      proc.start()
      uploadHistroy(a)
 

def uploadHistroy(action):
  db.collection(u'History').add({
    u'Action': action,
    u'Time': datetime.datetime.now()
})



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
