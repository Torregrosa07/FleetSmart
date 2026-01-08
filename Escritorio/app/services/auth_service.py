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

    def login(self, email, password):
        """
        Autentica al usuario y devuelve su perfil completo con el rol.
        
        Returns:
            dict: {
                'uid': str,
                'email': str,
                'rol': 'gestor' | 'conductor',
                'perfil_data': dict (datos del perfil),
                'token': str (Firebase Auth token)
            }
        
        Raises:
            Exception: Si las credenciales son incorrectas o el usuario no tiene perfil
        """
        try:
            # 1. Autenticar con Firebase Auth
            user = self.auth.sign_in_with_email_and_password(email, password)
            uid = user['localId']
            
            # 2. Buscar perfil en /gestores/{uid}
            gestor_data = self.db.child('gestores').child(uid).get()
            if gestor_data.val():
                return {
                    'uid': uid,
                    'email': email,
                    'rol': 'gestor',
                    'perfil_data': gestor_data.val(),
                    'token': user['idToken']
                }
            
            # 3. Si no es gestor, buscar en /conductores/{uid}
            conductor_data = self.db.child('conductores').child(uid).get()
            if conductor_data.val():
                return {
                    'uid': uid,
                    'email': email,
                    'rol': 'conductor',
                    'perfil_data': conductor_data.val(),
                    'token': user['idToken']
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