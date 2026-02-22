package com.fleetsmart.conductor.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class LoginViewModel : ViewModel() {

    private val _email = MutableStateFlow("")
    val email: StateFlow<String> = _email.asStateFlow()

    private val _password = MutableStateFlow("")
    val password: StateFlow<String> = _password.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    fun onEmailChange(newValue: String) {
        _email.value = newValue
        _error.value = null
    }

    fun onPasswordChange(newValue: String) {
        _password.value = newValue
        _error.value = null
    }

    fun login(onLoginSuccess: () -> Unit) {
        if (_email.value.isBlank() || _password.value.isBlank()) {
            _error.value = "Por favor, rellena todos los campos"
            return
        }

        viewModelScope.launch {
            _isLoading.value = true
            delay(1500)
            _isLoading.value = false
            onLoginSuccess()
        }
    }
}