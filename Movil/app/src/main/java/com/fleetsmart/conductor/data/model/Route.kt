package com.fleetsmart.conductor.data.model

/**
 * Modelo de ruta con datos reales de Firebase.
 * Combina datos de /rutas/{id} y /asignaciones/{id}
 */
data class Route(
    val id: String,
    val name: String,
    val origin: String,
    val destination: String,
    val date: String,
    val startTime: String,
    val endTime: String,
    val status: RouteStatus,
    val stops: List<RouteStop>,
    // Datos de la asignación
    val assignmentId: String = "",
    val vehiclePlate: String = ""
) {
    val distance: String
        get() = "${stops.size * 15} km"  // Estimación simple

    val duration: String
        get() {
            // Calcular duración desde hora inicio y fin
            try {
                val inicio = startTime.split(":")
                val fin = endTime.split(":")
                val minutos = (fin[0].toInt() * 60 + fin[1].toInt()) -
                        (inicio[0].toInt() * 60 + inicio[1].toInt())
                val horas = minutos / 60
                val mins = minutos % 60
                return if (horas > 0) "${horas}h ${mins}min" else "${mins}min"
            } catch (e: Exception) {
                return "--"
            }
        }
}

/**
 * Parada de una ruta (viene del campo "paradas" en Firebase)
 */
data class RouteStop(
    val id: String,
    val address: String,
    val order: Int,
    val latitude: Double = 0.0,
    val longitude: Double = 0.0,
    val completed: Boolean = false
)

enum class RouteStatus {
    PENDING,
    IN_PROGRESS,
    COMPLETED;

    companion object {
        fun fromString(estado: String): RouteStatus {
            return when (estado.lowercase()) {
                "pendiente", "asignada" -> PENDING
                "en curso", "en progreso" -> IN_PROGRESS
                "completada" -> COMPLETED
                else -> PENDING
            }
        }

        fun toDisplayString(status: RouteStatus): String {
            return when (status) {
                PENDING -> "Pendiente"
                IN_PROGRESS -> "En Curso"
                COMPLETED -> "Completada"
            }
        }
    }
}