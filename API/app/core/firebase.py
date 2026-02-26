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
        """
        Inicializa Firebase Admin SDK.
        Prioridad:
        1. Variable de entorno FIREBASE_CREDENTIALS_JSON (producción/Render)
        2. Archivo serviceAccountKey.json (local)
        """
        try:
            # 1. Intentar desde variable de entorno (Render)
            creds_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")

            if creds_json:
                cred_dict = json.loads(creds_json)
                cred = credentials.Certificate(cred_dict)
                print("✅ Firebase: credenciales desde variable de entorno")
            else:
                # 2. Fallback: archivo local
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                print("✅ Firebase: credenciales desde archivo local")

            firebase_admin.initialize_app(cred, {
                'databaseURL': settings.FIREBASE_DATABASE_URL
            })

            print("✅ Firebase Admin SDK inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando Firebase: {e}")
            raise

    @property
    def messaging(self):
        return messaging

    @property
    def database(self):
        return db.reference()


firebase_client = FirebaseClient()