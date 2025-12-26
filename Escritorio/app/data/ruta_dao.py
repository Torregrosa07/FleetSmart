class RutaDAO:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection_name = "rutas"

    def insertar(self, ruta_dict):
        """Guarda una nueva ruta en la nube"""
        return self.db.child(self.collection_name).push(ruta_dict)

    def leer_todas(self):
        """Descarga todas las rutas existentes"""
        return self.db.child(self.collection_name).get()