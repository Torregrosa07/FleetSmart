package com.fleetsmart.conductor.data.model

data class Incident(
    val id: String = "",
    val type: IncidentType,
    val description: String,
    val imageUri: String? = null,
    val timestamp: Long = System.currentTimeMillis()
)

enum class IncidentType(val displayName: String, val emoji: String) {
    VEHICLE("Problema con el vehículo", "🚗"),
    ROUTE("Problema con la ruta", "🗺️"),
    TRAFFIC("Incidente de tráfico", "🚦"),
    OTHER("Otro", "📝")
}