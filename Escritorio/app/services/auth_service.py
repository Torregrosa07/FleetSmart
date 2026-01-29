import pyrebase
from app.config.config import FIREBASE_CONFIG

class AuthService:
    def __init__(self):
        try:
            self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
            self.auth = self.firebase.auth()
            self.db = self.firebase.database()
        except Exception as e:
            print(f"Error al conectar con Firebase: {e}")

    # Escritorio/app/services/auth_service.py

    def login(self, email, password):
        """
        Autentica al usuario y devuelve su perfil completo con el rol.
        """
        try:
            # 1. Autenticar con Firebase Auth
            user = self.auth.sign_in_with_email_and_password(email, password)
            uid = user['localId']
            token = user['idToken']  # <--- GUARDAMOS EL TOKEN
            
            # 2. Buscar perfil en /gestores/{uid} USANDO EL TOKEN
            # Pasamos el token como argumento al método get()
            gestor_data = self.db.child('gestores').child(uid).get(token) 
            
            if gestor_data.val():
                return {
                    'uid': uid,
                    'email': email,
                    'rol': 'gestor',
                    'perfil_data': gestor_data.val(),
                    'token': token
                }
            
            # 3. Si no es gestor, buscar en /conductores/{uid} USANDO EL TOKEN
            conductor_data = self.db.child('conductores').child(uid).get(token)
            
            if conductor_data.val():
                return {
                    'uid': uid,
                    'email': email,
                    'rol': 'conductor',
                    'perfil_data': conductor_data.val(),
                    'token': token
                }
            
            # 4. Si no tiene perfil, lanzar error
            raise Exception("Usuario autenticado pero sin perfil en la base de datos")
            
        except Exception as e:
            raise e
    
    def crear_conductor(self, email, password):
        """
        Crea una cuenta de conductor en Firebase Auth.
        El perfil se guarda después desde ConductoresController.
        
        Args:
            email: Email del conductor
            password: Contraseña temporal
        
        Returns:
            dict: {'uid': str, 'email': str} si tiene éxito
        
        Raises:
            Exception: Si falla la creación
        """
        try:
            # Crear usuario en Firebase Auth
            user = self.auth.create_user_with_email_and_password(email, password)
            uid = user['localId']
            
            print(f"Cuenta de conductor creada con UID: {uid}")
            return {'uid': uid, 'email': email}
            
        except Exception as e:
            print(f"Error al crear cuenta de conductor: {e}")
            raise e