package com.fleetsmart.conductor.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.fleetsmart.conductor.data.model.Route
import com.fleetsmart.conductor.data.model.RouteStatus
import com.fleetsmart.conductor.ui.components.AppCard
import com.fleetsmart.conductor.ui.components.Badge
import com.fleetsmart.conductor.ui.components.BadgeVariant
import com.fleetsmart.conductor.ui.theme.AppColors
import com.fleetsmart.conductor.ui.viewmodel.RoutesViewModel

@Composable
fun MyRoutesScreen(
    onStartRoute: (String) -> Unit,
    viewModel: RoutesViewModel = viewModel()
) {
    val routes by viewModel.routes.collectAsState()
    // val isLoading by viewModel.isLoading.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Column(modifier = Modifier.padding(bottom = 16.dp)) {
            Text(
                text = "Mis Rutas",
                style = MaterialTheme.typography.headlineMedium,
                color = AppColors.Primary // Título en Azul
            )
            Text(
                text = "Gestiona tus rutas asignadas",
                style = MaterialTheme.typography.bodyMedium,
                color = AppColors.MutedForeground
            )
        }

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(routes) { route ->
                RouteCard(
                    route = route,
                    onStartRoute = {
                        // LLAMADA EXPLÍCITA: Aquí es donde se dispara la navegación
                        onStartRoute(route.id)
                    }
                )
            }
        }
    }
}

@Composable
private fun RouteCard(
    route: Route,
    onStartRoute: () -> Unit
) {
    // Asegúrate de que AppCard sea un contenedor simple (Card o Surface)
    Card(
        colors = CardDefaults.cardColors(containerColor = AppColors.Card),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // Header: Nombre y Fecha
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = route.name,
                        style = MaterialTheme.typography.titleMedium
                    )
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.CalendarToday,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp),
                            tint = AppColors.MutedForeground
                        )
                        Text(
                            text = route.date,
                            style = MaterialTheme.typography.bodySmall,
                            color = AppColors.MutedForeground
                        )
                    }
                }

                Badge(
                    text = getStatusText(route.status),
                    variant = getStatusVariant(route.status)
                )
            }

            // Stats
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                StatItem(Icons.Default.Navigation, "Distancia", route.distance, Modifier.weight(1f))
                StatItem(Icons.Default.AccessTime, "Duración", route.duration, Modifier.weight(1f))
                StatItem(Icons.Default.Place, "Paradas", route.stops.toString(), Modifier.weight(1f))
            }

            // BOTÓN DE ACCIÓN
            if (route.status != RouteStatus.COMPLETED) {
                Button(
                    onClick = { onStartRoute() }, // Acción de click
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(
                        // Si está en curso -> Fondo Azul (Primary), Texto Blanco
                        // Si está pendiente -> Fondo Azul Claro (Secondary), Texto Azul Oscuro
                        containerColor = if (route.status == RouteStatus.IN_PROGRESS)
                            AppColors.Primary
                        else
                            AppColors.Secondary,
                        contentColor = if (route.status == RouteStatus.IN_PROGRESS)
                            AppColors.PrimaryForeground
                        else
                            AppColors.SecondaryForeground
                    )
                ) {
                    Text(
                        text = if (route.status == RouteStatus.IN_PROGRESS) "Continuar Ruta" else "Iniciar Ruta"
                    )
                    Icon(
                        imageVector = Icons.Default.ChevronRight,
                        contentDescription = null,
                        modifier = Modifier.padding(start = 8.dp).size(20.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun StatItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    label: String,
    value: String,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(16.dp),
            tint = AppColors.MutedForeground
        )
        Column {
            Text(text = label, style = MaterialTheme.typography.labelSmall, color = AppColors.MutedForeground)
            Text(text = value, style = MaterialTheme.typography.bodyMedium)
        }
    }
}

private fun getStatusVariant(status: RouteStatus): BadgeVariant {
    return when (status) {
        RouteStatus.PENDING -> BadgeVariant.SECONDARY
        RouteStatus.IN_PROGRESS -> BadgeVariant.DEFAULT
        RouteStatus.COMPLETED -> BadgeVariant.OUTLINE
    }
}

private fun getStatusText(status: RouteStatus): String {
    return when (status) {
        RouteStatus.PENDING -> "Pendiente"
        RouteStatus.IN_PROGRESS -> "En Curso"
        RouteStatus.COMPLETED -> "Completada"
    }
}