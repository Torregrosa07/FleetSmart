package com.fleetsmart.conductor

import android.Manifest
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.lifecycle.lifecycleScope
import com.fleetsmart.conductor.data.FirebaseRepository
import com.fleetsmart.conductor.data.LocationService
import com.fleetsmart.conductor.model.ConductorData
import com.fleetsmart.conductor.model.UbicacionGPS
import com.fleetsmart.conductor.ui.MainScreen
import com.fleetsmart.conductor.ui.theme.FleetSmartConductorTheme
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

class MainActivity : ComponentActivity() {

    private lateinit var locationService: LocationService
    private lateinit var firebaseRepo: FirebaseRepository

    // Estados para la UI
    private var latitud by mutableStateOf<Double?>(null)
    private var longitud by mutableStateOf<Double?>(null)
    private var enviando by mutableStateOf(false)
    private var ultimaActualizacion by mutableStateOf("")

    companion object {
        private const val TAG = "MainActivity"
    }

    // Launcher para pedir permisos
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        val fineLocationGranted = permissions[Manifest.permission.ACCESS_FINE_LOCATION] ?: false
        val coarseLocationGranted = permissions[Manifest.permission.ACCESS_COARSE_LOCATION] ?: false

        if (fineLocationGranted || coarseLocationGranted) {
            Log.d(TAG, "✅ Permisos concedidos por el usuario")
            iniciarEnvioUbicaciones()
        } else {
            Log.e(TAG, "❌ Permisos denegados por el usuario")
            Toast.makeText(
                this,
                "Se necesitan permisos de ubicación para usar la app",
                Toast.LENGTH_LONG
            ).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Inicializar servicios
        locationService = LocationService(this)
        firebaseRepo = FirebaseRepository()

        // Configurar UI
        setContent {
            FleetSmartConductorTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MainScreen(
                        conductor = ConductorData.NOMBRE_CONDUCTOR,
                        vehiculo = ConductorData.MATRICULA_VEHICULO,
                        ruta = ConductorData.NOMBRE_RUTA,
                        latitud = latitud,
                        longitud = longitud,
                        enviando = enviando,
                        ultimaActualizacion = ultimaActualizacion,
                        onDetener = { detenerEnvioUbicaciones() }
                    )
                }
            }
        }

        // Pedir permisos y empezar
        solicitarPermisos()
    }

    /**
     * Solicita permisos de ubicación al usuario.
     */
    private fun solicitarPermisos() {
        if (locationService.hasLocationPermission()) {
            Log.d(TAG, "✅ Ya tenía permisos, iniciando...")
            iniciarEnvioUbicaciones()
        } else {
            Log.d(TAG, "⚠️ No tiene permisos, solicitando...")
            requestPermissionLauncher.launch(
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                )
            )
        }
    }

    /**
     * Inicia el servicio de envío de ubicaciones a Firebase.
     */
    private fun iniciarEnvioUbicaciones() {
        if (enviando) return
        enviando = true
        Log.d(TAG, "▶️ Iniciando flujo de ubicaciones...")

        lifecycleScope.launch {
            locationService.getLocationUpdates(intervalMillis = 5000)
                .catch { e ->
                    Log.e(TAG, "❌ Error en Flow de ubicación: ${e.message}")
                    Toast.makeText(
                        this@MainActivity,
                        "Error obteniendo ubicación: ${e.message}",
                        Toast.LENGTH_SHORT
                    ).show()
                    enviando = false
                }
                .collect { location ->
                    // Nueva ubicación recibida
                    Log.d(TAG, "📍 UI recibiendo ubicación: ${location.latitude}, ${location.longitude}")

                    latitud = location.latitude
                    longitud = location.longitude

                    // Crear objeto para enviar a Firebase
                    val ubicacion = UbicacionGPS(
                        id_asignacion = ConductorData.ID_ASIGNACION,
                        latitud = location.latitude,
                        longitud = location.longitude,
                        timestamp = obtenerTimestamp(),
                        nombre_conductor = ConductorData.NOMBRE_CONDUCTOR,
                        matricula_vehiculo = ConductorData.MATRICULA_VEHICULO,
                        nombre_ruta = ConductorData.NOMBRE_RUTA
                    )

                    // Enviar a Firebase
                    val enviado = firebaseRepo.enviarUbicacion(ubicacion)

                    if (enviado) {
                        ultimaActualizacion = obtenerHoraActual()
                    } else {
                        Log.w(TAG, "⚠️ Fallo al enviar a Firebase (revisar auth o reglas)")
                    }
                }
        }
    }

    /**
     * Detiene el envío de ubicaciones.
     */
    private fun detenerEnvioUbicaciones() {
        Log.d(TAG, "⏹️ Deteniendo envío...")
        enviando = false

        // Limpiar ubicación en Firebase
        lifecycleScope.launch {
            firebaseRepo.limpiarUbicacion(ConductorData.ID_ASIGNACION)
        }

        Toast.makeText(this, "Envío de ubicación detenido", Toast.LENGTH_SHORT).show()
    }

    /**
     * Obtiene el timestamp actual en formato ISO.
     */
    private fun obtenerTimestamp(): String {
        val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
        return sdf.format(Date())
    }

    /**
     * Obtiene la hora actual en formato legible.
     */
    private fun obtenerHoraActual(): String {
        val sdf = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
        return sdf.format(Date())
    }

    override fun onDestroy() {
        super.onDestroy()
        // Limpiar ubicación al cerrar la app
        if (enviando) {
            detenerEnvioUbicaciones()
        }
    }
}