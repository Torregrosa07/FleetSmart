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
    
    def leer_una(self, id_ruta):
        """Obtiene una ruta específica por su ID"""
        return self.db.child(self.collection_name).child(id_ruta).get().val()
    
    def eliminar(self, id_ruta):
        """Elimina una ruta de Firebase"""
        return self.db.child(self.collection_name).child(id_ruta).remove()
    
    def actualizar(self, id_ruta, ruta_dict):
        """Actualiza una ruta completa"""
        return self.db.child(self.collection_name).child(id_ruta).update(ruta_dict)