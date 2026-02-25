package com.fleetsmart.conductor.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fleetsmart.conductor.data.SessionManager
import com.fleetsmart.conductor.data.model.Route
import com.fleetsmart.conductor.data.model.RouteStop
import com.fleetsmart.conductor.data.model.Stop
import com.google.firebase.database.FirebaseDatabase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

data class ActiveRouteState(
    val routeName: String = "",
    val distance: String = "--",
    val duration: String = "--",
    val stops: List<Stop> = emptyList(),
    val routePoints: List<Pair<Double, Double>> = emptyList(), // lat, lon
    val centerLat: Double = 40.4168,
    val centerLon: Double = -3.7038,
    val isPaused: Boolean = false,
    val isLoading: Boolean = true
)

class ActiveRouteViewModel : ViewModel() {

    private val _state = MutableStateFlow(ActiveRouteState())
    val state: StateFlow<ActiveRouteState> = _state.asStateFlow()

    private val database = FirebaseDatabase.getInstance(
        "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app"
    )

    init {
        loadActiveRoute()
    }

    /**
     * Carga la ruta activa del conductor desde SessionManager + Firebase.
     * Reutiliza la asignación activa ya cargada en SessionManager.
     */
    private fun loadActiveRoute() {
        viewModelScope.launch {
            val asignacion = SessionManager.asignacionActiva.value

            if (asignacion == null) {
                _state.value = _state.value.copy(
                    routeName = "Sin ruta activa",
                    isLoading = false
                )
                return@launch
            }

            try {
                // Cargar datos de la ruta desde /rutas/{id_ruta}
                val rutaSnap = database.getReference("rutas")
                    .child(asignacion.idRuta)
                    .get()
                    .await()

                if (!rutaSnap.exists()) {
                    _state.value = _state.value.copy(
                        routeName = asignacion.nombreRuta,
                        isLoading = false
                    )
                    return@launch
                }

                val datos = rutaSnap.value as? Map<*, *> ?: return@launch

                // Parsear paradas
                val paradasRaw = datos["paradas"]
                val paradas = parsearParadas(paradasRaw)

                // Convertir RouteStop → Stop para la UI
                val stops = paradas.map { routeStop ->
                    Stop(
                        id = routeStop.id,
                        address = routeStop.address,
                        completed = false
                    )
                }

                // Calcular puntos del mapa (filtrar coordenadas válidas)
                val routePoints = paradas
                    .filter { it.latitude != 0.0 || it.longitude != 0.0 }
                    .sortedBy { it.order }
                    .map { Pair(it.latitude, it.longitude) }

                // Centro del mapa: primera parada o Madrid por defecto
                val centerLat = routePoints.firstOrNull()?.first ?: 40.4168
                val centerLon = routePoints.firstOrNull()?.second ?: -3.7038

                // Calcular distancia aproximada (número de paradas × 15 km)
                val distancia = "${paradas.size * 15} km"

                // Calcular duración desde hora inicio/fin
                val horaInicio = datos["hora_inicio_prevista"] as? String ?: "00:00"
                val horaFin = datos["hora_fin_prevista"] as? String ?: "00:00"
                val duracion = calcularDuracion(horaInicio, horaFin)

                _state.value = _state.value.copy(
                    routeName = asignacion.nombreRuta,
                    distance = distancia,
                    duration = duracion,
                    stops = stops,
                    routePoints = routePoints,
                    centerLat = centerLat,
                    centerLon = centerLon,
                    isLoading = false
                )

            } catch (e: Exception) {
                _state.value = _state.value.copy(
                    routeName = asignacion.nombreRuta,
                    isLoading = false
                )
            }
        }
    }

    private fun parsearParadas(paradasRaw: Any?): List<RouteStop> {
        if (paradasRaw == null) return emptyList()
        val paradas = mutableListOf<RouteStop>()

        when (paradasRaw) {
            is List<*> -> {
                for ((index, item) in paradasRaw.withIndex()) {
                    val map = item as? Map<*, *> ?: continue
                    paradas.add(crearParada(index, map))
                }
            }
            is Map<*, *> -> {
                for ((key, value) in paradasRaw) {
                    val map = value as? Map<*, *> ?: continue
                    val index = (key as? String)?.toIntOrNull()
                        ?: (key as? Long)?.toInt()
                        ?: paradas.size
                    paradas.add(crearParada(index, map))
                }
            }
        }

        return paradas.sortedBy { it.order }
    }

    private fun crearParada(index: Int, map: Map<*, *>): RouteStop {
        val coords = map["coords"]
        var lat = 0.0
        var lon = 0.0

        when (coords) {
            is List<*> -> {
                lat = (coords.getOrNull(0) as? Number)?.toDouble() ?: 0.0
                lon = (coords.getOrNull(1) as? Number)?.toDouble() ?: 0.0
            }
        }

        return RouteStop(
            id = index.toString(),
            address = map["direccion"] as? String ?: "Dirección desconocida",
            order = (map["orden"] as? Number)?.toInt() ?: (index + 1),
            latitude = lat,
            longitude = lon
        )
    }

    private fun calcularDuracion(inicio: String, fin: String): String {
        return try {
            val partsInicio = inicio.split(":")
            val partsFin = fin.split(":")
            val minutos = (partsFin[0].toInt() * 60 + partsFin[1].toInt()) -
                    (partsInicio[0].toInt() * 60 + partsInicio[1].toInt())
            val horas = minutos / 60
            val mins = minutos % 60
            if (horas > 0) "${horas}h ${mins}min" else "${mins}min"
        } catch (e: Exception) {
            "--"
        }
    }

    fun toggleStopComplete(stopId: String) {
        val updatedStops = _state.value.stops.map { stop ->
            if (stop.id == stopId) stop.copy(completed = !stop.completed) else stop
        }
        _state.value = _state.value.copy(stops = updatedStops)
    }

    fun togglePauseRoute() {
        _state.value = _state.value.copy(isPaused = !_state.value.isPaused)
    }

    fun finishRoute() {
        // La limpieza de ubicación ya se hace en MainActivity.detenerEnvioUbicaciones()
    }

    val completedStops: Int get() = _state.value.stops.count { it.completed }
    val totalStops: Int get() = _state.value.stops.size
    val progress: Float get() = if (totalStops > 0) completedStops.toFloat() / totalStops else 0f
}