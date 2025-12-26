import pyrebase
from app.config import FIREBASE_CONFIG

class AuthService:
    def __init__(self):
        try:
            self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
            self.auth = self.firebase.auth()
            print("Firebase inicializado correctamente.")
        except Exception as e:
            print(f"Error al conectar con Firebase: {e}")

    def login(self, email, password):
        """
        Devuelve el usuario si el login es correcto, 
        o lanza una excepción si falla.
        """
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            return user
        except Exception as e:
            raise e