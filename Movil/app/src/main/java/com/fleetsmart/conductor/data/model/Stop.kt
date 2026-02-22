package com.fleetsmart.conductor.data.model

data class Stop(
    val id: String,
    val address: String,
    val completed: Boolean = false,
    val phone: String? = null
)