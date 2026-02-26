package com.fleetsmart.conductor.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fleetsmart.conductor.data.SessionManager
import com.fleetsmart.conductor.data.model.IncidentType
import com.google.firebase.database.FirebaseDatabase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import java.text.SimpleDateFormat
import java.util.*

data class IncidentReportState(
    val selectedType: IncidentType = IncidentType.VEHICLE,
    val description: String = "",
    val isSubmitting: Boolean = false,
    val isSubmitted: Boolean = false,
    val error: String? = null
)

class IncidentReportViewModel : ViewModel() {

    private val _state = MutableStateFlow(IncidentReportState())
    val state: StateFlow<IncidentReportState> = _state.asStateFlow()

    private val database = FirebaseDatabase.getInstance(
        "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app"
    )

    fun setIncidentType(type: IncidentType) {
        _state.value = _state.value.copy(selectedType = type)
    }

    fun setDescription(description: String) {
        _state.value = _state.value.copy(description = description, error = null)
    }

    fun submitIncident() {
        val descripcion = _state.value.description.trim()
        if (descripcion.isEmpty()) {
            _state.value = _state.value.copy(error = "La descripción es obligatoria")
            return
        }

        val conductor = SessionManager.conductorActual.value
        val asignacion = SessionManager.asignacionActiva.value

        if (conductor == null) {
            _state.value = _state.value.copy(error = "No hay sesión activa")
            return
        }

        viewModelScope.launch {
            _state.value = _state.value.copy(isSubmitting = true, error = null)

            try {
                val ahora = Date()
                val fecha = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(ahora)
                val hora = SimpleDateFormat("HH:mm", Locale.getDefault()).format(ahora)

                // Estructura exacta que usa el escritorio en /incidencias
                val incidenciaData = mutableMapOf<String, Any>(
                    "tipo" to _state.value.selectedType.displayName,
                    "descripcion" to descripcion,
                    "estado" to "Pendiente",
                    "fecha" to fecha,
                    "hora" to hora
                )

                // Datos de vehículo desde la asignación activa
                if (asignacion != null) {
                    incidenciaData["id_vehiculo"] = asignacion.idVehiculo
                    incidenciaData["matricula"] = asignacion.matriculaVehiculo
                }

                // Guardar en /incidencias con ID autogenerado
                database.getReference("incidencias").push().setValue(incidenciaData).await()

                _state.value = _state.value.copy(
                    isSubmitting = false,
                    isSubmitted = true
                )

            } catch (e: Exception) {
                _state.value = _state.value.copy(
                    isSubmitting = false,
                    error = "Error al enviar: ${e.message}"
                )
            }
        }
    }

    fun resetForm() {
        _state.value = IncidentReportState()
    }

    val canSubmit: Boolean
        get() = _state.value.description.trim().isNotEmpty() && !_state.value.isSubmitting
}