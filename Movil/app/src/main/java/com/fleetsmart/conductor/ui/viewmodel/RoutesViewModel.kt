package com.fleetsmart.conductor.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fleetsmart.conductor.data.SessionManager
import com.fleetsmart.conductor.data.model.Route
import com.fleetsmart.conductor.data.model.RouteStatus
import com.fleetsmart.conductor.data.model.RouteStop
import com.google.firebase.database.FirebaseDatabase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

class RoutesViewModel : ViewModel() {

    private val database = FirebaseDatabase.getInstance(
        "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app"
    )

    private val _routes = MutableStateFlow<List<Route>>(emptyList())
    val routes: StateFlow<List<Route>> = _routes.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    init {
        loadRoutes()
    }

    /**
     * Carga las rutas asignadas al conductor logueado.
     *
     * Flujo:
     * 1. Busca en /asignaciones las que pertenecen al conductor
     * 2. Para cada asignación, carga los datos de /rutas/{id_ruta}
     * 3. Combina ambos datos en el modelo Route
     */
    fun loadRoutes() {
        val uid = SessionManager.getUid() ?: return

        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null

            try {
                // 1. Obtener todas las asignaciones del conductor
                val asignacionesSnap = database.getReference("asignaciones")
                    .get()
                    .await()

                if (!asignacionesSnap.exists()) {
                    _routes.value = emptyList()
                    _isLoading.value = false
                    return@launch
                }

                val rutasCargadas = mutableListOf<Route>()

                for (child in asignacionesSnap.children) {
                    val datos = child.value as? Map<*, *> ?: continue
                    val idConductor = datos["id_conductor"] as? String ?: continue

                    // Solo las asignaciones de este conductor
                    if (idConductor != uid) continue

                    val idRuta = datos["id_ruta"] as? String ?: continue
                    val idAsignacion = child.key ?: continue
                    val matricula = datos["matricula_vehiculo"] as? String ?: ""

                    // 2. Cargar datos de la ruta
                    val ruta = cargarDatosRuta(idRuta, idAsignacion, matricula)
                    if (ruta != null) {
                        rutasCargadas.add(ruta)
                    }
                }

                _routes.value = rutasCargadas

            } catch (e: Exception) {
                _error.value = "Error cargando rutas: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }

    /**
     * Carga los datos de una ruta desde /rutas/{id_ruta}
     * y los combina con la info de la asignación
     */
    private suspend fun cargarDatosRuta(
        idRuta: String,
        idAsignacion: String,
        matricula: String
    ): Route? {
        return try {
            val rutaSnap = database.getReference("rutas")
                .child(idRuta)
                .get()
                .await()

            if (!rutaSnap.exists()) return null

            val datos = rutaSnap.value as? Map<*, *> ?: return null

            // Parsear paradas
            val paradasRaw = datos["paradas"]
            val paradas = parsearParadas(paradasRaw)

            // Determinar estado
            val estadoRuta = datos["estado"] as? String ?: "Pendiente"

            Route(
                id = idRuta,
                name = datos["nombre"] as? String ?: "Ruta sin nombre",
                origin = datos["origen"] as? String ?: "",
                destination = datos["destino"] as? String ?: "",
                date = datos["fecha"] as? String ?: "",
                startTime = datos["hora_inicio_prevista"] as? String ?: "00:00",
                endTime = datos["hora_fin_prevista"] as? String ?: "00:00",
                status = RouteStatus.fromString(estadoRuta),
                stops = paradas,
                assignmentId = idAsignacion,
                vehiclePlate = matricula
            )
        } catch (e: Exception) {
            null
        }
    }

    /**
     * Parsea las paradas de Firebase (pueden venir como List o Map)
     */
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
}