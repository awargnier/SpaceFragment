import firebase_admin
import pyrebase
from firebase_admin import credentials
from configs.firebase_config import firebaseConfig
from dotenv import dotenv_values
import json

config = dotenv_values(".env")

if not firebase_admin._apps:
  # cred = credentials.Certificate("configs/spacefragmentsapi-firebase-adminsdk-6isup-ef10c227fe.json")
  cred = credentials.Certificate(json.load(config['FIREBASE_SERVICE_ACCOUNT_KEY']))
  firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(json.load(config['FIREBASE_CONFIG']))
db = firebase.database()
authUser = firebase.auth()