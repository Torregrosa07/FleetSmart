"""
MapUtils - Utilidades para gestión de mapas con Folium

Centraliza toda la lógica de creación y manipulación de mapas.
Se usa desde controladores que necesiten mostrar mapas.
"""
import folium
import io
from typing import List, Dict, Any, Optional


class MapUtils:
    """
    Utilidad que encapsula operaciones de Folium.
    Reduce código duplicado entre controladores.
    """
    
    # Coordenadas por defecto
    DEFAULT_CENTER = [40.4168, -3.7038]  # Madrid, España
    DEFAULT_ZOOM = 6
    
    # Estilos de iconos predefinidos
    ICON_STYLES = {
        'origin': {'color': 'green', 'icon': 'play', 'prefix': 'fa'},
        'destination': {'color': 'blue', 'icon': 'stop', 'prefix': 'fa'},
        'waypoint': {'color': 'red', 'icon': 'flag', 'prefix': 'fa'},
        'vehicle': {'color': 'green', 'icon': 'truck', 'prefix': 'fa'},
        'company': {'color': 'blue', 'icon': 'building', 'prefix': 'fa'}
    }
    
    @staticmethod
    def create_base_map(center: List[float] = None, zoom: int = None) -> folium.Map:
        """
        Crea un mapa base de Folium.
        
        Args:
            center: Coordenadas [lat, lon] del centro
            zoom: Nivel de zoom inicial
            
        Returns:
            Mapa de Folium configurado
        """
        if center is None:
            center = MapUtils.DEFAULT_CENTER
        if zoom is None:
            zoom = MapUtils.DEFAULT_ZOOM
        
        return folium.Map(location=center, zoom_start=zoom)
    
    @staticmethod
    def add_marker(
        mapa: folium.Map,
        coords: List[float],
        popup_text: str = "",
        tooltip_text: str = "",
        icon_type: str = 'waypoint'
    ) -> folium.Map:
        """
        Añade un marcador al mapa.
        
        Args:
            mapa: Mapa de Folium
            coords: Coordenadas [lat, lon]
            popup_text: Texto del popup
            tooltip_text: Texto del tooltip
            icon_type: Tipo de icono ('origin', 'destination', 'waypoint', 'vehicle', 'company')
            
        Returns:
            El mismo mapa con el marcador añadido
        """
        icon_style = MapUtils.ICON_STYLES.get(icon_type, MapUtils.ICON_STYLES['waypoint'])
        
        folium.Marker(
            location=coords,
            popup=popup_text if popup_text else None,
            tooltip=tooltip_text if tooltip_text else None,
            icon=folium.Icon(**icon_style)
        ).add_to(mapa)
        
        return mapa
    
    @staticmethod
    def add_polyline(
        mapa: folium.Map,
        points: List[List[float]],
        color: str = 'blue',
        weight: int = 4,
        opacity: float = 0.7
    ) -> folium.Map:
        """
        Añade una línea conectando puntos.
        
        Args:
            mapa: Mapa de Folium
            points: Lista de coordenadas [[lat, lon], ...]
            color: Color de la línea
            weight: Grosor de la línea
            opacity: Opacidad (0.0 a 1.0)
            
        Returns:
            El mismo mapa con la línea añadida
        """
        if len(points) > 1:
            folium.PolyLine(
                locations=points,
                color=color,
                weight=weight,
                opacity=opacity
            ).add_to(mapa)
        
        return mapa
    
    @staticmethod
    def fit_bounds(mapa: folium.Map, points: List[List[float]]) -> folium.Map:
        """
        Ajusta el zoom del mapa para mostrar todos los puntos.
        
        Args:
            mapa: Mapa de Folium
            points: Lista de coordenadas
            
        Returns:
            El mismo mapa con zoom ajustado
        """
        if len(points) > 1:
            mapa.fit_bounds(points)
        return mapa
    
    @staticmethod
    def render_to_html(mapa: folium.Map) -> str:
        """
        Convierte el mapa a HTML para QWebEngineView.
        
        Args:
            mapa: Mapa de Folium
            
        Returns:
            HTML del mapa como string
        """
        data = io.BytesIO()
        mapa.save(data, close_file=False)
        return data.getvalue().decode()
    
    @staticmethod
    def create_route_map(
        origin_coords: Optional[List[float]],
        origin_label: str,
        waypoints: List[Dict[str, Any]],
        center: List[float] = None
    ) -> folium.Map:
        """
        Crea un mapa completo de ruta con origen, paradas y líneas.
        
        Args:
            origin_coords: Coordenadas del origen [lat, lon]
            origin_label: Etiqueta para el popup del origen
            waypoints: Lista de dicts con 'coords', 'direccion', 'orden'
            center: Centro del mapa (si None, usa origen o España)
            
        Returns:
            Mapa completo con la ruta
        """
        # Determinar centro
        if center is None:
            center = origin_coords if origin_coords else MapUtils.DEFAULT_CENTER
        
        # Crear mapa base
        mapa = MapUtils.create_base_map(center=center, zoom=12)
        all_points = []
        
        # Añadir marcador de origen
        if origin_coords:
            MapUtils.add_marker(
                mapa,
                coords=origin_coords,
                popup_text=f"INICIO: {origin_label}",
                icon_type='origin'
            )
            all_points.append(origin_coords)
        
        # Añadir marcadores de paradas
        for i, waypoint in enumerate(waypoints):
            is_last = (i == len(waypoints) - 1)
            icon_type = 'destination' if is_last else 'waypoint'
            
            MapUtils.add_marker(
                mapa,
                coords=waypoint['coords'],
                popup_text=f"Parada {waypoint.get('orden', i+1)}: {waypoint['direccion']}",
                icon_type=icon_type
            )
            all_points.append(waypoint['coords'])
        
        # Añadir línea y ajustar zoom
        if len(all_points) > 1:
            MapUtils.add_polyline(mapa, all_points)
            MapUtils.fit_bounds(mapa, all_points)
        
        return mapa
    
    @staticmethod
    def create_fleet_map(
        company_coords: List[float],
        company_name: str,
        vehicles: List[Dict[str, Any]],
        fit_to_bounds: bool = True
    ) -> folium.Map:
        """
        Crea un mapa con la empresa y vehículos activos.
        
        Args:
            company_coords: Coordenadas de la empresa [lat, lon]
            company_name: Nombre de la empresa
            vehicles: Lista de dicts con info de vehículos
            fit_to_bounds: Si True, ajusta el zoom
            
        Returns:
            Mapa completo con empresa y vehículos
        """
        # Crear mapa base
        mapa = MapUtils.create_base_map(center=company_coords, zoom=MapUtils.DEFAULT_ZOOM)
        
        # Añadir marcador de empresa
        MapUtils.add_marker(
            mapa,
            coords=company_coords,
            popup_text=f"<b>Centro de Operaciones</b><br>{company_name}",
            icon_type='company'
        )
        
        all_coords = [company_coords]
        
        # Añadir vehículos
        for vehicle in vehicles:
            coords = [vehicle['latitud'], vehicle['longitud']]
            all_coords.append(coords)
            
            popup_text = (
                f"<b>Vehículo:</b> {vehicle.get('matricula_vehiculo', 'N/A')}<br>"
                f"<b>Conductor:</b> {vehicle.get('nombre_conductor', 'N/A')}<br>"
                f"<b>Ruta:</b> {vehicle.get('nombre_ruta', 'N/A')}<br>"
                f"<small>{vehicle.get('timestamp', '')}</small>"
            )
            
            MapUtils.add_marker(
                mapa,
                coords=coords,
                popup_text=popup_text,
                tooltip_text=vehicle.get('matricula_vehiculo', ''),
                icon_type='vehicle'
            )
        
        # Ajustar zoom si hay varios puntos
        if fit_to_bounds and len(all_coords) > 1:
            MapUtils.fit_bounds(mapa, all_coords)
        
        return mapa