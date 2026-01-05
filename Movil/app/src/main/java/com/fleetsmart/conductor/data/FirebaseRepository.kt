package com.fleetsmart.conductor.data

import android.util.Log
import com.fleetsmart.conductor.model.UbicacionGPS
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.ktx.auth
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase
import kotlinx.coroutines.tasks.await

/**
 * Repositorio para interactuar con Firebase Realtime Database.
 * Envía ubicaciones GPS a la base de datos.
 */
class FirebaseRepository {

    private val auth: FirebaseAuth = Firebase.auth
    private val database: FirebaseDatabase = Firebase.database(
        "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app"
    )

    private val ubicacionesRef = database.getReference("localizaciones_actuales")
    private val historialRef = database.getReference("historial_localizaciones")

    companion object {
        private const val TAG = "FirebaseRepository"
    }

    /**
     * Autentica anónimamente si no está autenticado
     */
    suspend fun ensureAuthenticated(): Boolean {
        return try {
            if (auth.currentUser == null) {
                Log.d(TAG, "🔐 Autenticando anónimamente...")
                auth.signInAnonymously().await()
                Log.d(TAG, "✅ Autenticación exitosa: ${auth.currentUser?.uid}")
            } else {
                Log.d(TAG, "✅ Ya autenticado: ${auth.currentUser?.uid}")
            }
            true
        } catch (e: Exception) {
            Log.e(TAG, "❌ Error autenticando: ${e.message}", e)
            false
        }
    }

    /**
     * Envía la ubicación actual a Firebase.
     * Actualiza /localizaciones_actuales/{id_asignacion}
     */
    suspend fun enviarUbicacion(ubicacion: UbicacionGPS): Boolean {
        // Asegurar autenticación
        if (!ensureAuthenticated()) {
            Log.e(TAG, "❌ No se pudo autenticar")
            return false
        }

        return try {
            ubicacionesRef
                .child(ubicacion.id_asignacion)
                .setValue(ubicacion.toMap())
                .await()

            Log.d(TAG, "✅ Ubicación enviada: ${ubicacion.latitud}, ${ubicacion.longitud}")
            true

        } catch (e: Exception) {
            Log.e(TAG, "❌ Error enviando ubicación: ${e.message}", e)
            false
        }
    }

    /**
     * Envía la ubicación al historial.
     */
    suspend fun enviarHistorial(ubicacion: UbicacionGPS): Boolean {
        if (!ensureAuthenticated()) {
            return false
        }

        return try {
            historialRef
                .child(ubicacion.id_asignacion)
                .push()
                .setValue(ubicacion.toMap())
                .await()

            Log.d(TAG, "📝 Ubicación guardada en historial")
            true

        } catch (e: Exception) {
            Log.e(TAG, "❌ Error guardando historial: ${e.message}", e)
            false
        }
    }

    /**
     * Limpia la ubicación actual cuando termina la ruta.
     */
    suspend fun limpiarUbicacion(idAsignacion: String): Boolean {
        if (!ensureAuthenticated()) {
            return false
        }

        return try {
            ubicacionesRef.child(idAsignacion).removeValue().await()
            Log.d(TAG, "🗑️ Ubicación limpiada")
            true
        } catch (e: Exception) {
            Log.e(TAG, "❌ Error limpiando ubicación: ${e.message}", e)
            false
        }
    }
}