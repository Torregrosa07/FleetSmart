class IncidenciaDAO:
    """
    Data Access Object para Incidencias.
    Maneja la comunicación con Firebase Realtime Database.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection_name = "incidencias"

    def insertar(self, incidencia_dict):
        """
        Guarda una nueva incidencia en Firebase.
        Firebase genera el ID automáticamente.
        """
        return self.db.child(self.collection_name).push(incidencia_dict)
    
    def leer_todos(self):
        """Obtiene todas las incidencias"""
        return self.db.child(self.collection_name).get()
    
    def leer_por_id(self, id_incidencia):
        """Obtiene una incidencia específica por su ID"""
        return self.db.child(self.collection_name).child(id_incidencia).get()
    
    def leer_por_vehiculo(self, id_vehiculo):
        """
        Obtiene todas las incidencias de un vehículo específico.
        
        Nota: Firebase Realtime Database no soporta queries complejas,
        así que obtenemos todas y filtramos en el repository.
        """
        return self.db.child(self.collection_name).get()
    
    def eliminar(self, id_incidencia):
        """Elimina una incidencia"""
        return self.db.child(self.collection_name).child(id_incidencia).remove()

    def actualizar(self, id_incidencia, datos_dict):
        """Actualiza los datos de una incidencia"""
        return self.db.child(self.collection_name).child(id_incidencia).update(datos_dict)