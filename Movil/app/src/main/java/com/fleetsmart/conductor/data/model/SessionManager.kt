package com.fleetsmart.conductor.data

import android.util.Log
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.messaging.FirebaseMessaging
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.tasks.await

object SessionManager {

    private val auth = FirebaseAuth.getInstance()
    private val database = FirebaseDatabase.getInstance(
        "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app"
    )

    private val _conductorActual = MutableStateFlow<ConductorSesion?>(null)
    val conductorActual: StateFlow<ConductorSesion?> = _conductorActual.asStateFlow()

    private val _asignacionActiva = MutableStateFlow<AsignacionActiva?>(null)
    val asignacionActiva: StateFlow<AsignacionActiva?> = _asignacionActiva.asStateFlow()

    suspend fun login(email: String, password: String): Result<ConductorSesion> {
        return try {
            // 1. Autenticar con Firebase Auth
            val authResult = auth.signInWithEmailAndPassword(email, password).await()
            val uid = authResult.user?.uid
                ?: return Result.failure(Exception("No se pudo obtener el UID"))

            // 2. Cargar perfil desde /conductores/{uid}
            val snapshot = database.getReference("conductores")
                .child(uid)
                .get()
                .await()

            if (!snapshot.exists()) {
                auth.signOut()
                return Result.failure(Exception("No se encontró el perfil de conductor"))
            }

            val datos = snapshot.value as? Map<*, *>
                ?: return Result.failure(Exception("Datos de conductor inválidos"))

            // 3. Crear objeto de sesión
            val conductor = ConductorSesion(
                uid = uid,
                nombre = datos["nombre"] as? String ?: "",
                email = datos["email"] as? String ?: email,
                dni = datos["dni"] as? String ?: "",
                licencia = datos["licencia"] as? String ?: "",
                telefono = datos["telefono"] as? String ?: "",
                estado = datos["estado"] as? String ?: "Activo"
            )

            _conductorActual.value = conductor

            // 4. Guardar FCM token en Firebase
            guardarFcmToken(uid)

            // 5. Cargar asignación activa
            cargarAsignacionActiva(uid)

            Result.success(conductor)

        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Obtiene el token FCM del dispositivo y lo guarda en /conductores/{uid}/fcm_token
     */
    private suspend fun guardarFcmToken(uid: String) {
        try {
            val token = FirebaseMessaging.getInstance().token.await()
            database.getReference("conductores")
                .child(uid)
                .child("fcm_token")
                .setValue(token)
                .await()
            Log.d("SessionManager", "✅ FCM token guardado: $token")
        } catch (e: Exception) {
            Log.e("SessionManager", "❌ Error guardando FCM token: ${e.message}")
            // No es crítico, el login sigue adelante
        }
    }

    private suspend fun cargarAsignacionActiva(uid: String) {
        try {
            val snapshot = database.getReference("asignaciones")
                .get()
                .await()

            if (!snapshot.exists()) return

            for (child in snapshot.children) {
                val datos = child.value as? Map<*, *> ?: continue
                val idConductor = datos["id_conductor"] as? String ?: continue

                if (idConductor == uid) {
                    _asignacionActiva.value = AsignacionActiva(
                        idAsignacion = child.key ?: "",
                        idRuta = datos["id_ruta"] as? String ?: "",
                        nombreRuta = datos["nombre_ruta"] as? String ?: "",
                        idVehiculo = datos["id_vehiculo"] as? String ?: "",
                        matriculaVehiculo = datos["matricula_vehiculo"] as? String ?: "",
                        estado = datos["estado"] as? String ?: ""
                    )
                    return
                }
            }
        } catch (e: Exception) {
            // Sin asignación activa, no es un error crítico
        }
    }

    suspend fun refrescarAsignacion() {
        val uid = _conductorActual.value?.uid ?: return
        _asignacionActiva.value = null
        cargarAsignacionActiva(uid)
    }

    fun logout() {
        auth.signOut()
        _conductorActual.value = null
        _asignacionActiva.value = null
    }

    fun estaLogueado(): Boolean {
        return auth.currentUser != null && _conductorActual.value != null
    }

    fun getUid(): String? = auth.currentUser?.uid
}

data class ConductorSesion(
    val uid: String,
    val nombre: String,
    val email: String,
    val dni: String,
    val licencia: String,
    val telefono: String,
    val estado: String
)

data class AsignacionActiva(
    val idAsignacion: String,
    val idRuta: String,
    val nombreRuta: String,
    val idVehiculo: String,
    val matriculaVehiculo: String,
    val estado: String
)