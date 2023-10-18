import firebase_admin
import pyrebase 
from firebase_admin import credentials
from configs.firebase_config import firebaseConfig

if not firebase_admin._apps:
  cred = credentials.Certificate("configs/spacefragmentsapi-firebase-adminsdk-6isup-28aa0cdc2c.json")
  firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()