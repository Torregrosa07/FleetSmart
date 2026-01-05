class GestorDAO:
    
    def __init__(self, db_connection):
        """
        Inicializa el DAO con la conexión a Firebase
        """
        self.db = db_connection
        self.collection_name = "gestores"

    def insertar(self, gestor_dict):
        """
        Envía el diccionario del gestor a Firebase
        """
        return self.db.child(self.collection_name).push(gestor_dict)
    
    def insertar_con_id(self, id_gestor, gestor_dict):
        """
        Inserta un gestor con un ID específico (el UID de Firebase Auth).
        """
        return self.db.child(self.collection_name).child(id_gestor).set(gestor_dict)
    
    def leer_todos(self):
        """
        Descarga todos los gestores de la nube
        """
        return self.db.child(self.collection_name).get()
    
    def leer_por_id(self, id_gestor):
        """
        Obtiene un gestor específico por su ID
        """
        return self.db.child(self.collection_name).child(id_gestor).get()
    
    def eliminar(self, id_gestor):
        """
        Borra el nodo del gestor
        """
        return self.db.child(self.collection_name).child(id_gestor).remove()

    def actualizar(self, id_gestor, datos_dict):
        """
        Actualiza los datos de un gestor existente
        """
        return self.db.child(self.collection_name).child(id_gestor).update(datos_dict)