"""
Cliente Firebase Admin SDK
Soporta credenciales por archivo (local) o variable de entorno (producción/Render)
"""
import os
import json
import firebase_admin
from firebase_admin import credentials, messaging, db
from app.core.config import settings


class FirebaseClient:
    """Cliente Firebase singleton"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialize()
            self._initialized = True

    def _initialize(self):
        creds_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
        print(f"🔍 FIREBASE_CREDENTIALS_JSON presente: {creds_json is not None}")
        print(f"🔍 Longitud: {len(creds_json) if creds_json else 0}")
        
        if creds_json:
            cred_dict = json.loads(creds_json)
            cred = credentials.Certificate(cred_dict)
            print("✅ Firebase: credenciales desde variable de entorno")
        else:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            print("✅ Firebase: credenciales desde archivo local")

        firebase_admin.initialize_app(cred, {
            'databaseURL': settings.FIREBASE_DATABASE_URL
    
    })
    @property
    def messaging(self):
        return messaging

    @property
    def database(self):
        return db.reference()


firebase_client = FirebaseClient()