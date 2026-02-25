package com.fleetsmart.conductor.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.fleetsmart.conductor.data.model.Route
import com.fleetsmart.conductor.data.model.RouteStatus
import com.fleetsmart.conductor.ui.viewmodel.RoutesViewModel

@Composable
fun RoutesScreen(
    onRouteClick: (Route) -> Unit = {},
    viewModel: RoutesViewModel = viewModel()
) {
    val routes by viewModel.routes.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF5F5F5))
            .padding(16.dp)
    ) {
        // Encabezado
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Mis Rutas",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF1A1A2E)
            )
            IconButton(onClick = { viewModel.loadRoutes() }) {
                Icon(
                    Icons.Default.Refresh,
                    contentDescription = "Recargar",
                    tint = Color(0xFF4A90D9)
                )
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Contador de rutas
        if (routes.isNotEmpty()) {
            Text(
                text = "${routes.size} ruta(s) asignada(s)",
                fontSize = 14.sp,
                color = Color.Gray
            )
            Spacer(modifier = Modifier.height(12.dp))
        }

        // Estados
        when {
            isLoading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator(color = Color(0xFF4A90D9))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Cargando rutas...", color = Color.Gray)
                    }
                }
            }

            error != null -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = error ?: "Error desconocido",
                            color = Color(0xFFE74C3C),
                            fontSize = 14.sp
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(
                            onClick = { viewModel.loadRoutes() },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color(0xFF4A90D9)
                            )
                        ) {
                            Text("Reintentar")
                        }
                    }
                }
            }

            routes.isEmpty() -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.Default.LocationOn,
                            contentDescription = null,
                            tint = Color.LightGray,
                            modifier = Modifier.size(64.dp)
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "No tienes rutas asignadas",
                            fontSize = 16.sp,
                            color = Color.Gray,
                            fontWeight = FontWeight.Medium
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "Las rutas aparecerán aquí cuando te sean asignadas",
                            fontSize = 13.sp,
                            color = Color.LightGray
                        )
                    }
                }
            }

            else -> {
                LazyColumn(
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(routes) { route ->
                        RouteCard(
                            route = route,
                            onClick = { onRouteClick(route) }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun RouteCard(
    route: Route,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            // Nombre ruta + estado
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = route.name,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF1A1A2E),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )
                Spacer(modifier = Modifier.width(8.dp))
                StatusChip(status = route.status)
            }

            Spacer(modifier = Modifier.height(10.dp))

            // Origen → Destino
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    Icons.Default.LocationOn,
                    contentDescription = null,
                    tint = Color(0xFF4A90D9),
                    modifier = Modifier.size(16.dp)
                )
                Spacer(modifier = Modifier.width(6.dp))
                Text(
                    text = "${route.origin}  →  ${route.destination}",
                    fontSize = 13.sp,
                    color = Color.Gray,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Info adicional: fecha, horario, vehículo
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                // Fecha
                if (route.date.isNotEmpty()) {
                    InfoTag(label = route.date)
                }

                // Horario
                InfoTag(label = "${route.startTime} - ${route.endTime}")

                // Vehículo
                if (route.vehiclePlate.isNotEmpty()) {
                    InfoTag(label = route.vehiclePlate)
                }
            }

            // Paradas
            if (route.stops.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "${route.stops.size} parada(s)",
                    fontSize = 12.sp,
                    color = Color(0xFF4A90D9)
                )
            }
        }
    }
}

@Composable
fun StatusChip(status: RouteStatus) {
    val (bgColor, textColor) = when (status) {
        RouteStatus.PENDING -> Color(0xFFFFF3CD) to Color(0xFF856404)
        RouteStatus.IN_PROGRESS -> Color(0xFFD4EDDA) to Color(0xFF155724)
        RouteStatus.COMPLETED -> Color(0xFFD1ECF1) to Color(0xFF0C5460)
    }

    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(16.dp))
            .background(bgColor)
            .padding(horizontal = 10.dp, vertical = 4.dp)
    ) {
        Text(
            text = RouteStatus.toDisplayString(status),
            fontSize = 11.sp,
            fontWeight = FontWeight.Medium,
            color = textColor
        )
    }
}

@Composable
fun InfoTag(label: String) {
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(6.dp))
            .background(Color(0xFFF0F0F0))
            .padding(horizontal = 8.dp, vertical = 3.dp)
    ) {
        Text(
            text = label,
            fontSize = 11.sp,
            color = Color(0xFF666666)
        )
    }
}