package com.fleetsmart.conductor.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fleetsmart.conductor.data.model.Stop
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class ActiveRouteState(
    val routeName: String = "Ruta Centro Madrid",
    val distance: String = "45 km",
    val duration: String = "2h 30min",
    val stops: List<Stop> = emptyList(),
    val isPaused: Boolean = false
)

class ActiveRouteViewModel : ViewModel() {

    private val _state = MutableStateFlow(ActiveRouteState())
    val state: StateFlow<ActiveRouteState> = _state.asStateFlow()

    init {
        loadRouteDetails()
    }

    private fun loadRouteDetails() {
        viewModelScope.launch {
            // Datos mock - aquí se reemplazaría con una llamada al repositorio
            _state.value = _state.value.copy(
                stops = listOf(
                    Stop(
                        id = "1",
                        address = "Calle Mayor 1, Madrid",
                        completed = true,
                        phone = "+34 600 111 222"
                    ),
                    Stop(
                        id = "2",
                        address = "Avenida de la Constitución 5, Madrid",
                        completed = true,
                        phone = "+34 600 333 444"
                    ),
                    Stop(
                        id = "3",
                        address = "Plaza de España 3, Madrid",
                        completed = false,
                        phone = "+34 600 555 666"
                    ),
                    Stop(
                        id = "4",
                        address = "Gran Vía 28, Madrid",
                        completed = false,
                        phone = "+34 600 777 888"
                    ),
                    Stop(
                        id = "5",
                        address = "Calle Alcalá 42, Madrid",
                        completed = false
                    )
                )
            )
        }
    }

    fun toggleStopComplete(stopId: String) {
        viewModelScope.launch {
            val updatedStops = _state.value.stops.map { stop ->
                if (stop.id == stopId) {
                    stop.copy(completed = !stop.completed)
                } else {
                    stop
                }
            }
            _state.value = _state.value.copy(stops = updatedStops)
        }
    }

    fun togglePauseRoute() {
        _state.value = _state.value.copy(isPaused = !_state.value.isPaused)
    }

    fun finishRoute() {
        viewModelScope.launch {
            // Aquí se enviaría la información al backend
        }
    }

    val completedStops: Int
        get() = _state.value.stops.count { it.completed }

    val totalStops: Int
        get() = _state.value.stops.size

    val progress: Float
        get() = if (totalStops > 0) completedStops.toFloat() / totalStops else 0f
}