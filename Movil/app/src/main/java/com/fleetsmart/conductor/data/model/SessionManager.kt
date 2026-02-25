package com.fleetsmart.conductor.data

import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.FirebaseDatabase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.tasks.await

/**
 * Gestiona la sesión del conductor autenticado.
 * Singleton que reemplaza a ConductorData (que tenía datos hardcodeados).
 *
 * Después del login, carga los datos del conductor desde /conductores/{uid}
 * y los mantiene disponibles para toda la app.
 */
object SessionManager {

    private val auth = FirebaseAuth.getInstance()
    private val database = FirebaseDatabase.getInstance(
        "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app"
    )

    // Datos del conductor logueado
    private val _conductorActual = MutableStateFlow<ConductorSesion?>(null)
    val conductorActual: StateFlow<ConductorSesion?> = _conductorActual.asStateFlow()

    // Asignación activa (se carga después del login)
    private val _asignacionActiva = MutableStateFlow<AsignacionActiva?>(null)
    val asignacionActiva: StateFlow<AsignacionActiva?> = _asignacionActiva.asStateFlow()

    /**
     * Autentica al conductor con email y contraseña.
     * Después carga su perfil desde Firebase Database.
     *
     * @return Result.success si todo OK, Result.failure con el error si falla
     */
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

            // 4. Cargar asignación activa (si tiene)
            cargarAsignacionActiva(uid)

            Result.success(conductor)

        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Busca si el conductor tiene una asignación activa en /asignaciones
     */
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

    /**
     * Recarga la asignación activa (útil después de cambios)
     */
    suspend fun refrescarAsignacion() {
        val uid = _conductorActual.value?.uid ?: return
        _asignacionActiva.value = null
        cargarAsignacionActiva(uid)
    }

    /**
     * Cierra la sesión
     */
    fun logout() {
        auth.signOut()
        _conductorActual.value = null
        _asignacionActiva.value = null
    }

    /**
     * Verifica si hay sesión activa
     */
    fun estaLogueado(): Boolean {
        return auth.currentUser != null && _conductorActual.value != null
    }

    /**
     * Obtiene el UID del conductor actual
     */
    fun getUid(): String? = auth.currentUser?.uid
}

/**
 * Datos del conductor en sesión
 */
data class ConductorSesion(
    val uid: String,
    val nombre: String,
    val email: String,
    val dni: String,
    val licencia: String,
    val telefono: String,
    val estado: String
)

/**
 * Datos de la asignación activa del conductor
 */
data class AsignacionActiva(
    val idAsignacion: String,
    val idRuta: String,
    val nombreRuta: String,
    val idVehiculo: String,
    val matriculaVehiculo: String,
    val estado: String
)