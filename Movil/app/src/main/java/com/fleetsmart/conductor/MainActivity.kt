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
import androidx.compose.ui.Modifier
import androidx.lifecycle.lifecycleScope
import com.fleetsmart.conductor.data.FirebaseRepository
import com.fleetsmart.conductor.data.LocationService
import com.fleetsmart.conductor.model.ConductorData
import com.fleetsmart.conductor.model.UbicacionGPS
import com.fleetsmart.conductor.ui.navigation.FleetDriverApp
import com.fleetsmart.conductor.ui.theme.MockUpsFleetSmartMovilTheme
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var locationService: LocationService
    private lateinit var firebaseRepo: FirebaseRepository

    // Estado interno para saber si ya estamos enviando ubicación
    private var enviando = false

    companion object {
        private const val TAG = "MainActivity"
    }

    // Launcher para pedir permisos de ubicación al usuario
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        val fineLocationGranted = permissions[Manifest.permission.ACCESS_FINE_LOCATION] ?: false
        val coarseLocationGranted = permissions[Manifest.permission.ACCESS_COARSE_LOCATION] ?: false

        if (fineLocationGranted || coarseLocationGranted) {
            Log.d(TAG, "✅ Permisos concedidos por el usuario")
            iniciarEnvioUbicaciones()
        } else {
            Log.e(TAG, "❌ Permisos denegados")
            Toast.makeText(this, "Se necesitan permisos de ubicación para realizar la ruta", Toast.LENGTH_LONG).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Inicializar servicios ligeros
        locationService = LocationService(this)
        firebaseRepo = FirebaseRepository()

        // 🔧 1. MOVER OSMDROID A UN HILO SECUNDARIO PARA QUE NO CONGELE LA PANTALLA
        lifecycleScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            org.osmdroid.config.Configuration.getInstance().load(
                applicationContext,
                getSharedPreferences("osmdroid", android.content.Context.MODE_PRIVATE)
            )
        }

        setContent {
            // USAMOS TU TEMA AQUÍ
            MockUpsFleetSmartMovilTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = com.fleetsmart.conductor.ui.theme.AppColors.Background
                ) {
                    FleetDriverApp(
                        onIniciarRuta = { solicitarPermisosYArrancar() },
                        onDetenerRuta = { detenerEnvioUbicaciones() }
                    )
                }
            }
        }
    }

    /**
     * Solicitado por Navigation.kt cuando el usuario hace clic en "Iniciar Ruta"
     */
    private fun solicitarPermisosYArrancar() {
        if (locationService.hasLocationPermission()) {
            iniciarEnvioUbicaciones()
        } else {
            requestPermissionLauncher.launch(
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                )
            )
        }
    }

    /**
     * Inicia el flujo de GPS y lo manda a Firebase en segundo plano
     */
    private fun iniciarEnvioUbicaciones() {
        if (enviando) return
        enviando = true
        Toast.makeText(this, "Iniciando ruta y GPS...", Toast.LENGTH_SHORT).show()

        lifecycleScope.launch {
            locationService.getLocationUpdates(intervalMillis = 5000)
                .catch { e ->
                    Log.e(TAG, "Error en GPS: ${e.message}")
                    enviando = false
                }
                .collect { location ->
                    val ubicacion = UbicacionGPS(
                        id_asignacion = ConductorData.ID_ASIGNACION,
                        latitud = location.latitude,
                        longitud = location.longitude,
                        timestamp = obtenerTimestamp(),
                        nombre_conductor = ConductorData.NOMBRE_CONDUCTOR,
                        matricula_vehiculo = ConductorData.MATRICULA_VEHICULO,
                        nombre_ruta = ConductorData.NOMBRE_RUTA
                    )
                    // Enviar a Firebase de forma transparente (sin molestar a la UI)
                    firebaseRepo.enviarUbicacion(ubicacion)
                }
        }
    }

    /**
     * Solicitado por Navigation.kt cuando el usuario hace clic en "Finalizar" o "Volver"
     */
    private fun detenerEnvioUbicaciones() {
        if (!enviando) return
        enviando = false
        Toast.makeText(this, "Ruta y GPS detenidos", Toast.LENGTH_SHORT).show()

        // Borra el rastro de la BD cuando el conductor termina
        lifecycleScope.launch {
            firebaseRepo.limpiarUbicacion(ConductorData.ID_ASIGNACION)
        }
    }

    private fun obtenerTimestamp(): String {
        val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
        return sdf.format(Date())
    }

    override fun onDestroy() {
        super.onDestroy()
        if (enviando) {
            detenerEnvioUbicaciones()
        }
    }
}