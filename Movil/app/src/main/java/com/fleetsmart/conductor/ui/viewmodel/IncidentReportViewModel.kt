package com.fleetsmart.conductor.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fleetsmart.conductor.data.model.Incident
import com.fleetsmart.conductor.data.model.IncidentType
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class IncidentReportState(
    val selectedType: IncidentType = IncidentType.VEHICLE,
    val description: String = "",
    val imageUri: String? = null,
    val isSubmitting: Boolean = false,
    val isSubmitted: Boolean = false,
    val error: String? = null
)

class IncidentReportViewModel : ViewModel() {

    private val _state = MutableStateFlow(IncidentReportState())
    val state: StateFlow<IncidentReportState> = _state.asStateFlow()

    fun setIncidentType(type: IncidentType) {
        _state.value = _state.value.copy(selectedType = type)
    }

    fun setDescription(description: String) {
        _state.value = _state.value.copy(description = description)
    }

    fun setImageUri(uri: String?) {
        _state.value = _state.value.copy(imageUri = uri)
    }

    fun submitIncident() {
        if (_state.value.description.trim().isEmpty()) {
            _state.value = _state.value.copy(error = "La descripción es obligatoria")
            return
        }

        viewModelScope.launch {
            _state.value = _state.value.copy(isSubmitting = true, error = null)

            try {
                // Aquí se enviaría el reporte al backend
                val incident = Incident(
                    type = _state.value.selectedType,
                    description = _state.value.description,
                    imageUri = _state.value.imageUri
                )

                // Simulación de envío
                delay(1000)

                _state.value = _state.value.copy(
                    isSubmitting = false,
                    isSubmitted = true
                )

                // Reset después de 3 segundos
                delay(3000)
                resetForm()

            } catch (e: Exception) {
                _state.value = _state.value.copy(
                    isSubmitting = false,
                    error = "Error al enviar el reporte: ${e.message}"
                )
            }
        }
    }

    private fun resetForm() {
        _state.value = IncidentReportState()
    }

    val canSubmit: Boolean
        get() = _state.value.description.trim().isNotEmpty() && !_state.value.isSubmitting
}