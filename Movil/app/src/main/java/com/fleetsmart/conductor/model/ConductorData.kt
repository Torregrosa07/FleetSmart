package com.fleetsmart.conductor.model

/**
 * Datos del conductor predefinidos para pruebas.
 * En producción, estos datos vendrían de Firebase Auth.
 */
object ConductorData {
    const val ID_ASIGNACION = "asig_test_001"
    const val NOMBRE_CONDUCTOR = "Juan Pérez"
    const val MATRICULA_VEHICULO = "ABC-1234"
    const val NOMBRE_RUTA = "Ruta Madrid Centro"
}

/**
 * Modelo de ubicación GPS que se envía a Firebase.
 * Debe coincidir con el modelo del desktop (LocalizacionGPS).
 */
data class UbicacionGPS(
    val id_asignacion: String,
    val latitud: Double,
    val longitud: Double,
    val timestamp: String,
    val nombre_conductor: String,
    val matricula_vehiculo: String,
    val nombre_ruta: String
) {
    /**
     * Convierte el objeto a Map para enviar a Firebase.
     */
    fun toMap(): Map<String, Any> {
        return mapOf(
            "id_asignacion" to id_asignacion,
            "latitud" to latitud,
            "longitud" to longitud,
            "timestamp" to timestamp,
            "nombre_conductor" to nombre_conductor,
            "matricula_vehiculo" to matricula_vehiculo,
            "nombre_ruta" to nombre_ruta
        )
    }
}