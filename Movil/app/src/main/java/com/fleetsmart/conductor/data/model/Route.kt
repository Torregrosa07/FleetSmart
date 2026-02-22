package com.fleetsmart.conductor.data.model

data class Route(
    val id: String,
    val name: String,
    val date: String,
    val status: RouteStatus,
    val distance: String,
    val duration: String,
    val stops: Int
)

enum class RouteStatus {
    PENDING,
    IN_PROGRESS,
    COMPLETED
}