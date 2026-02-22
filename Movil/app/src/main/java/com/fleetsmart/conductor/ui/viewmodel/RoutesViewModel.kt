package com.fleetsmart.conductor.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fleetsmart.conductor.data.model.Route
import com.fleetsmart.conductor.data.model.RouteStatus
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class RoutesViewModel : ViewModel() {

    private val _routes = MutableStateFlow<List<Route>>(emptyList())
    val routes: StateFlow<List<Route>> = _routes.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    init {
        loadRoutes()
    }

    private fun loadRoutes() {
        viewModelScope.launch {
            _isLoading.value = true

            _routes.value = listOf(
                Route(
                    id = "1",
                    name = "Ruta Centro Madrid",
                    date = "14 Dic 2024",
                    status = RouteStatus.IN_PROGRESS,
                    distance = "45 km",
                    duration = "2h 30min",
                    stops = 8
                ),
                Route(
                    id = "2",
                    name = "Ruta Norte Barcelona",
                    date = "15 Dic 2024",
                    status = RouteStatus.PENDING,
                    distance = "62 km",
                    duration = "3h 15min",
                    stops = 12
                ),
                Route(
                    id = "3",
                    name = "Ruta Sur Valencia",
                    date = "13 Dic 2024",
                    status = RouteStatus.COMPLETED,
                    distance = "38 km",
                    duration = "2h",
                    stops = 6
                )
            )

            _isLoading.value = false
        }
    }
}