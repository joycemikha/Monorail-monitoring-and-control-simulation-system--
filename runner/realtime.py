import re
import pyrebase

from train import train

firebaseConfig={"apiKey": "AIzaSyA2_a11HPKU3jMGllmeBXLvxxxdhLmWmEU",
  "authDomain": "monorail-34377.firebaseapp.com",
  "databaseURL": "https://monorail-34377-default-rtdb.firebaseio.com",
  "projectId": "monorail-34377",
  "storageBucket": "monorail-34377.appspot.com",
  "messagingSenderId": "411503744552",
  "appId": "1:411503744552:web:a681e0df39144cf4a6071d",
  "measurementId": "G-0T5E5YZ0HG"}

firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
#Create paths using child
data={"isEmergency":"0", "location":"Mahmoudabdel aziz street (station 1)"}
db.child("emergency").set(data)
v=0
def stream_handler(message):
  global v
  print(message["event"]) # put
  print(message["path"]) # /-K7yGTTEp7O549EzTYtI
  print(message["data"])
  v=message["data"]
     # {'title': 'Pyrebase', "body": "etc..."}

my_stream = db.stream(stream_handler)
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

# # Fetch the service account key JSON file contents
# cred = credentials.Certificate('monorail-34377-firebase-adminsdk-dmp2e-e79f123d39.json')

# # Initialize the app with a service account, granting admin privileges
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://monorail-34377-default-rtdb.firebaseio.com'
# })

# # As an admin, the app has access to read and write all data, regradless of Security Rules
# ref = db.reference('emergency')
# v=ref.child("isEmergency").get()
# print(ref.child("isEmergency").get())