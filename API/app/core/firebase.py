"""
Cliente Firebase Admin SDK
"""
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
        """Inicializa Firebase Admin SDK"""
        try:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            
            firebase_admin.initialize_app(cred, {
                'databaseURL': settings.FIREBASE_DATABASE_URL
            })
            
            print("✅ Firebase Admin SDK inicializado")
            
        except Exception as e:
            print(f"❌ Error Firebase: {e}")
            raise
    
    @property
    def messaging(self):
        return messaging
    
    @property
    def database(self):
        return db.reference()


firebase_client = FirebaseClient()