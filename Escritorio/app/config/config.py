
import pyrebase
import firebase_admin
from firebase_admin import credentials, db as admin_db
import os


# ============================================================================
# API DE NOTIFICACIONES
# ============================================================================

API_BASE_URL = "http://localhost:8000"
API_NOTIFICACIONES_URL = f"{API_BASE_URL}/api/notificaciones"

# ============================================================================
# PYREBASE - Para Auth, CRUD básico, la mayoría del proyecto
# ============================================================================

FIREBASE_CONFIG = {
"apiKey": "AIzaSyBnRzdV_hnzIQL6D_ie1Ckho83WLLIzUC0",
  "authDomain": "fleetsmart-1.firebaseapp.com",
  "databaseURL": "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "fleetsmart-1",
  "storageBucket": "fleetsmart-1.firebasestorage.app",
  "messagingSenderId": "602477520072",
  "appId": "1:602477520072:web:79d132f469e0e5a9a371fd"

}

# Inicializar Pyrebase (global)
firebase_pyrebase = None
auth_service = None
database_pyrebase = None

try:
    firebase_pyrebase = pyrebase.initialize_app(FIREBASE_CONFIG)
    auth_service = firebase_pyrebase.auth()
    database_pyrebase = firebase_pyrebase.database()
    print("Pyrebase inicializado correctamente")
except Exception as e:
    print(f"Error al inicializar Pyrebase: {e}")


# ============================================================================
# FIREBASE ADMIN SDK - Solo para listeners en tiempo real
# ============================================================================

admin_initialized = False
admin_db_ref = None

# Ruta al archivo de credenciales (dentro de app/config/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_PATH = os.path.join(SCRIPT_DIR, "serviceAccountKey.json")


def init_firebase_admin():
    """
    Inicializa Firebase Admin SDK para listeners en tiempo real.
    Busca serviceAccountKey.json en app/config/
    """
    global admin_initialized, admin_db_ref
    
    if admin_initialized:
        print("Firebase Admin SDK ya está inicializado")
        return True
    
    # Verificar que existe el archivo
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        print(f"Archivo serviceAccountKey.json NO encontrado en:")
        print(f"{SERVICE_ACCOUNT_PATH}")
        print("   Los listeners en tiempo real NO funcionarán")
        print("   Descárgalo desde Firebase Console → Settings → Service Accounts")
        return False
    
    try:
        # Inicializar Admin SDK
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': FIREBASE_CONFIG['databaseURL']
        })
        
        # Obtener referencia a la base de datos
        admin_db_ref = admin_db.reference()
        
        admin_initialized = True
        print(f"Firebase Admin SDK inicializado correctamente")
        print(f"   Archivo: {SERVICE_ACCOUNT_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Error al inicializar Firebase Admin SDK: {e}")
        return False


def get_admin_db():
    """
    Obtiene la referencia a la base de datos de Admin SDK.
    
    Returns:
        Reference de Admin SDK o None si no está inicializado
    """
    if not admin_initialized:
        print("Firebase Admin SDK no inicializado. Llamando a init_firebase_admin()...")
        init_firebase_admin()
    
    return admin_db_ref


def is_admin_available():
    """
    Verifica si Admin SDK está disponible y funcionando.
    
    Returns:
        True si está disponible, False si no
    """
    return admin_initialized and admin_db_ref is not None


# ============================================================================
# INICIALIZACIÓN AUTOMÁTICA DE ADMIN SDK
# ============================================================================

# Intentar inicializar Admin SDK automáticamente al importar el módulo
try:
    init_firebase_admin()
except Exception as e:
    print(f"No se pudo inicializar Admin SDK automáticamente: {e}")
    print("El sistema funcionará con Pyrebase (sin listeners en tiempo real)")
