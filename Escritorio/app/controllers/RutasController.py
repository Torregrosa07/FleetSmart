import folium
import io
from PySide6.QtWidgets import QWidget, QMessageBox
from geopy.geocoders import Nominatim 

from app.views.RutasWidget_ui import Ui_RutasWidget
from app.models.ruta import Ruta
from app.repositories.ruta_repository import RutaRepository

# Ya no necesitamos repositorios de conductores/vehículos aquí
# porque eso se hará en la pantalla de "Asignar Rutas"

class RutasController(QWidget, Ui_RutasWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.setupUi(self)
        
        # 1. Repositorio (Solo Rutas)
        self.repo_rutas = RutaRepository(db_connection)
        
        # 2. Geolocalizador
        self.geolocalizador = Nominatim(user_agent="tfg_fleetsmart_v1")
        
        # 3. Variables de memoria para el mapa
        self.coordenadas_origen = None 
        self.lista_destinos = []        
        
        # 4. Inicialización
        self.dibujar_mapa_vacio()
        
        # 5. Conexiones
        self.leOrigen.editingFinished.connect(self.buscar_origen)
        self.btnAgregarParada.clicked.connect(self.agregar_nueva_parada)
        self.btnEliminarParada.clicked.connect(self.borrar_parada)
        self.btnGuardarRuta.clicked.connect(self.guardar_plantilla_ruta)

    # =========================================================================
    # LÓGICA DEL MAPA (IGUAL QUE ANTES)
    # =========================================================================
    def dibujar_mapa_vacio(self):
        mapa = folium.Map(location=[40.4168, -3.7038], zoom_start=6)
        self.mostrar_mapa_en_pantalla(mapa)

    def mostrar_mapa_en_pantalla(self, mapa_creado):
        datos = io.BytesIO()
        mapa_creado.save(datos, close_file=False)
        self.webMapRuta.setHtml(datos.getvalue().decode())

    def actualizar_mapa_con_ruta(self):
        # Si no tenemos origen, usamos el centro de España
        centro = self.coordenadas_origen if self.coordenadas_origen else [40.4168, -3.7038]
        mapa = folium.Map(location=centro, zoom_start=12)
        
        puntos_para_linea = []

        # 1. Pintar Origen
        if self.coordenadas_origen:
            folium.Marker(
                location=self.coordenadas_origen,
                popup="INICIO: " + self.leOrigen.text(),
                icon=folium.Icon(color="green", icon="play", prefix="fa")
            ).add_to(mapa)
            puntos_para_linea.append(self.coordenadas_origen)

        # 2. Pintar Paradas
        for i, parada in enumerate(self.lista_destinos):
            folium.Marker(
                location=parada['coords'],
                popup=f"Parada {i+1}: {parada['direccion']}",
                icon=folium.Icon(color="red", icon="flag", prefix="fa")
            ).add_to(mapa)
            puntos_para_linea.append(parada['coords'])

        # 3. Línea Azul
        if len(puntos_para_linea) > 1:
            folium.PolyLine(
                locations=puntos_para_linea, color="blue", weight=4, opacity=0.7
            ).add_to(mapa)
            mapa.fit_bounds(puntos_para_linea)

        self.mostrar_mapa_en_pantalla(mapa)

    # =========================================================================
    # GEOCODING (IGUAL QUE ANTES)
    # =========================================================================
    def buscar_origen(self):
        texto = self.leOrigen.text().strip()
        if not texto: return
        try:
            loc = self.geolocalizador.geocode(texto)
            if loc:
                self.coordenadas_origen = [loc.latitude, loc.longitude]
                self.actualizar_mapa_con_ruta()
        except: pass

    def agregar_nueva_parada(self):
        texto = self.leNuevaParada.text().strip()
        if not texto: return
        try:
            loc = self.geolocalizador.geocode(texto)
            if loc:
                dato = {
                    "direccion": texto,
                    "coords": [loc.latitude, loc.longitude],
                    "orden": len(self.lista_destinos) + 1
                }
                self.lista_destinos.append(dato)
                self.listParadas.addItem(f"{dato['orden']}. {texto}")
                self.leNuevaParada.clear()
                self.actualizar_mapa_con_ruta()
            else:
                QMessageBox.warning(self, "Error", "Dirección no encontrada.")
        except Exception as e:
            print(e)
            
    def borrar_parada(self):
        """Borra la parada seleccionada de la lista y del mapa"""
        fila = self.listParadas.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una parada de la lista.")
            return

        # Borrar de la lista de datos interna
        del self.lista_destinos[fila]
        
        # Borrar de la lista visual
        self.listParadas.takeItem(fila)
        
        # Re-dibujar el mapa
        self.actualizar_mapa_con_ruta()    
            
            
            
    def guardar_plantilla_ruta(self):
        """Guarda solo la definición de la ruta para usarla después"""
        
        # 1. Validar nombre (Importante para reusarla)
        nombre = self.leNombreRuta.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Falta Nombre", "Ponle un nombre a la ruta (ej: 'Reparto Centro').")
            return

        # 2. Validar puntos
        if not self.coordenadas_origen:
            QMessageBox.warning(self, "Falta Origen", "Define un origen válido.")
            return
        if not self.lista_destinos:
            QMessageBox.warning(self, "Sin Paradas", "Añade al menos una parada.")
            return

        # 3. Crear Objeto LIMPIO (Sin conductor ni vehículo)
        nueva_plantilla = Ruta(
            nombre=nombre,
            origen=self.leOrigen.text(),
            paradas=self.lista_destinos
        )
        
        # 4. Guardar
        if self.repo_rutas.guardar_ruta(nueva_plantilla):
            QMessageBox.information(self, "Guardado", "Plantilla de ruta creada.\nAhora puedes asignarla desde el menú 'Asignar Rutas'.")
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", "Error al guardar en base de datos.")

    def limpiar_formulario(self):
        self.leNombreRuta.clear()
        self.leOrigen.clear()
        self.leNuevaParada.clear()
        self.listParadas.clear()
        self.coordenadas_origen = None
        self.lista_destinos = []
        self.dibujar_mapa_vacio()