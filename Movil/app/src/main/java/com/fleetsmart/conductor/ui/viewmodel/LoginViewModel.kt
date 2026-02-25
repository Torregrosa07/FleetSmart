package com.fleetsmart.conductor.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fleetsmart.conductor.data.SessionManager
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
            _error.value = null

            val resultado = SessionManager.login(
                email = _email.value.trim(),
                password = _password.value
            )

            _isLoading.value = false

            resultado.fold(
                onSuccess = {
                    onLoginSuccess()
                },
                onFailure = { e ->
                    _error.value = interpretarError(e)
                }
            )
        }
    }

    /**
     * Convierte errores de Firebase en mensajes amigables
     */
    private fun interpretarError(error: Throwable): String {
        val mensaje = error.message ?: "Error desconocido"

        return when {
            "INVALID_LOGIN_CREDENTIALS" in mensaje ||
                    "INVALID_EMAIL" in mensaje ||
                    "WRONG_PASSWORD" in mensaje -> "Email o contraseña incorrectos"

            "USER_NOT_FOUND" in mensaje -> "No existe una cuenta con este email"

            "USER_DISABLED" in mensaje -> "Esta cuenta ha sido deshabilitada"

            "TOO_MANY_REQUESTS" in mensaje -> "Demasiados intentos. Espera unos minutos"

            "NETWORK" in mensaje.uppercase() -> "Error de conexión. Comprueba tu internet"

            "No se encontró el perfil" in mensaje -> "Esta cuenta no tiene perfil de conductor"

            else -> "Error al iniciar sesión: $mensaje"
        }
    }
}