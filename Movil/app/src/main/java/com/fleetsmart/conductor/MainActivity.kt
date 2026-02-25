package com.fleetsmart.conductor

import android.Manifest
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.lifecycle.lifecycleScope
import com.fleetsmart.conductor.data.FirebaseRepository
import com.fleetsmart.conductor.data.LocationService
import com.fleetsmart.conductor.data.SessionManager
import com.fleetsmart.conductor.model.UbicacionGPS
import com.fleetsmart.conductor.ui.navigation.FleetDriverApp
import com.fleetsmart.conductor.ui.theme.MockUpsFleetSmartMovilTheme
import com.fleetsmart.conductor.ui.theme.AppColors
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var locationService: LocationService
    private lateinit var firebaseRepo: FirebaseRepository

    private var enviando = false

    companion object {
        private const val TAG = "MainActivity"
    }

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        val fineLocationGranted = permissions[Manifest.permission.ACCESS_FINE_LOCATION] ?: false
        val coarseLocationGranted = permissions[Manifest.permission.ACCESS_COARSE_LOCATION] ?: false

        if (fineLocationGranted || coarseLocationGranted) {
            iniciarEnvioUbicaciones()
        } else {
            Toast.makeText(this, "Se necesitan permisos de ubicación", Toast.LENGTH_LONG).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        locationService = LocationService(this)
        firebaseRepo = FirebaseRepository()

        lifecycleScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            org.osmdroid.config.Configuration.getInstance().load(
                applicationContext,
                getSharedPreferences("osmdroid", android.content.Context.MODE_PRIVATE)
            )
        }

        setContent {
            MockUpsFleetSmartMovilTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = AppColors.Background
                ) {
                    FleetDriverApp(
                        onIniciarRuta = { solicitarPermisosYArrancar() },
                        onDetenerRuta = { detenerEnvioUbicaciones() }
                    )
                }
            }
        }
    }

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
     * Inicia el flujo de GPS usando datos reales de SessionManager
     */
    private fun iniciarEnvioUbicaciones() {
        if (enviando) return

        // Verificar que hay sesión y asignación activa
        val conductor = SessionManager.conductorActual.value
        val asignacion = SessionManager.asignacionActiva.value

        if (conductor == null || asignacion == null) {
            Toast.makeText(this, "No hay asignación activa", Toast.LENGTH_SHORT).show()
            return
        }

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
                        id_asignacion = asignacion.idAsignacion,
                        latitud = location.latitude,
                        longitud = location.longitude,
                        timestamp = obtenerTimestamp(),
                        nombre_conductor = conductor.nombre,
                        matricula_vehiculo = asignacion.matriculaVehiculo,
                        nombre_ruta = asignacion.nombreRuta
                    )
                    firebaseRepo.enviarUbicacion(ubicacion)
                }
        }
    }

    private fun detenerEnvioUbicaciones() {
        if (!enviando) return
        enviando = false
        Toast.makeText(this, "Ruta y GPS detenidos", Toast.LENGTH_SHORT).show()

        val asignacion = SessionManager.asignacionActiva.value
        if (asignacion != null) {
            lifecycleScope.launch {
                firebaseRepo.limpiarUbicacion(asignacion.idAsignacion)
            }
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