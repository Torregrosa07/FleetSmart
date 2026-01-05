package com.fleetsmart.conductor.data

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.os.Looper
import android.util.Log
import androidx.annotation.RequiresPermission
import androidx.core.content.ContextCompat
import com.google.android.gms.location.*
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.tasks.await

/**
 * Servicio para obtener la ubicación GPS del dispositivo.
 * Usa Google Play Services Location API.
 */
class LocationService(private val context: Context) {

    private val fusedLocationClient: FusedLocationProviderClient =
        LocationServices.getFusedLocationProviderClient(context)

    companion object {
        private const val TAG = "LocationService"
    }

    /**
     * Verifica si la app tiene permisos de ubicación.
     */
    fun hasLocationPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
    }

    /**
     * Obtiene actualizaciones de ubicación en tiempo real.
     * Devuelve un Flow que emite ubicaciones cada vez que cambian.
     *
     * @param intervalMillis Intervalo entre actualizaciones (milisegundos)
     */
    fun getLocationUpdates(intervalMillis: Long = 5000): Flow<Location> = callbackFlow {

        if (!hasLocationPermission()) {
            Log.e(TAG, "❌ No hay permisos de ubicación al intentar iniciar updates")
            close(Exception("Sin permisos de ubicación"))
            return@callbackFlow
        }

        Log.d(TAG, "🚀 Iniciando solicitud de ubicación (High Accuracy)...")

        // Configuración de solicitud de ubicación
        val locationRequest = LocationRequest.Builder(
            Priority.PRIORITY_HIGH_ACCURACY,
            intervalMillis
        ).apply {
            setMinUpdateIntervalMillis(intervalMillis)
            setWaitForAccurateLocation(false)
        }.build()

        // Callback que se ejecuta cada vez que hay nueva ubicación
        val locationCallback = object : LocationCallback() {
            override fun onLocationResult(result: LocationResult) {
                // LOG IMPORTANTE: Verifica si llegan resultados
                Log.d(TAG, "📍 Callback recibido. Cantidad de ubicaciones: ${result.locations.size}")

                result.lastLocation?.let { location ->
                    Log.d(TAG, "✅ Coordenadas: Lat=${location.latitude}, Lon=${location.longitude}, Acc=${location.accuracy}")
                    // Emitir ubicación al Flow
                    trySend(location)
                } ?: run {
                    Log.w(TAG, "⚠️ El resultado llegó pero lastLocation es null")
                }
            }

            override fun onLocationAvailability(availability: LocationAvailability) {
                super.onLocationAvailability(availability)
                // LOG IMPORTANTE: Verifica si el hardware GPS está disponible
                val disponible = availability.isLocationAvailable
                Log.d(TAG, "📡 Estado del GPS (Disponibilidad): $disponible")
                if (!disponible) {
                    Log.w(TAG, "⚠️ El dispositivo dice que la ubicación NO está disponible ahora mismo.")
                }
            }
        }

        // Iniciar actualizaciones de ubicación
        try {
            fusedLocationClient.requestLocationUpdates(
                locationRequest,
                locationCallback,
                Looper.getMainLooper()
            )
            Log.d(TAG, "✅ Listener de ubicación registrado correctamente")
        } catch (e: SecurityException) {
            Log.e(TAG, "❌ Error de seguridad solicitando ubicación: ${e.message}")
            close(e)
        } catch (e: Exception) {
            Log.e(TAG, "❌ Error desconocido solicitando ubicación: ${e.message}")
            close(e)
        }

        // Cuando el Flow se cierra, detener actualizaciones
        awaitClose {
            Log.d(TAG, "🛑 Deteniendo actualizaciones de ubicación")
            fusedLocationClient.removeLocationUpdates(locationCallback)
        }
    }

    /**
     * Obtiene la última ubicación conocida (una sola vez).
     * Útil para mostrar ubicación inicial rápidamente.
     */
    @RequiresPermission(allOf = [Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION])
    suspend fun getLastKnownLocation(): Location? {
        if (!hasLocationPermission()) {
            return null
        }

        return try {
            val location = fusedLocationClient.lastLocation.await()
            if (location != null) {
                Log.d(TAG, "📍 Última ubicación conocida: ${location.latitude}, ${location.longitude}")
            } else {
                Log.d(TAG, "xh⚠️ No hay última ubicación conocida almacenada")
            }
            location
        } catch (e: Exception) {
            Log.e(TAG, "Error obteniendo última ubicación: ${e.message}")
            null
        }
    }
}