package com.fleetsmart.conductor.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.fleetsmart.conductor.data.SessionManager
import com.fleetsmart.conductor.ui.components.AppCard
import com.fleetsmart.conductor.ui.theme.AppColors

@Composable
fun ProfileScreen(
    onLogout: () -> Unit = {}
) {
    val conductor by SessionManager.conductorActual.collectAsState()
    val asignacion by SessionManager.asignacionActiva.collectAsState()

    // Iniciales del conductor
    val iniciales = conductor?.nombre
        ?.split(" ")
        ?.take(2)
        ?.mapNotNull { it.firstOrNull()?.uppercaseChar()?.toString() }
        ?.joinToString("")
        ?: "??"

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        // Avatar e info básica
        item {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.fillMaxWidth()
            ) {
                Box(
                    modifier = Modifier
                        .size(96.dp)
                        .background(AppColors.Primary, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = iniciales,
                        style = MaterialTheme.typography.headlineLarge,
                        color = AppColors.PrimaryForeground
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))

                Text(
                    text = conductor?.nombre ?: "Cargando...",
                    style = MaterialTheme.typography.headlineMedium
                )
                Text(
                    text = "Conductor Profesional",
                    style = MaterialTheme.typography.bodyMedium,
                    color = AppColors.MutedForeground
                )
            }
        }

        // Tarjetas de info
        item {
            Column(
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                ProfileInfoCard(
                    label = "DNI",
                    value = conductor?.dni ?: "-",
                    icon = Icons.Default.Badge
                )
                ProfileInfoCard(
                    label = "Licencia",
                    value = conductor?.licencia ?: "-",
                    icon = Icons.Default.CreditCard
                )
                ProfileInfoCard(
                    label = "Teléfono",
                    value = conductor?.telefono ?: "-",
                    icon = Icons.Default.Phone
                )
                ProfileInfoCard(
                    label = "Email",
                    value = conductor?.email ?: "-",
                    icon = Icons.Default.Email
                )
                ProfileInfoCard(
                    label = "Vehículo Asignado",
                    value = asignacion?.let {
                        "${it.matriculaVehiculo} - ${it.nombreRuta}"
                    } ?: "Sin asignación",
                    icon = Icons.Default.DirectionsCar
                )
            }
        }

        // Configuración
        item {
            Column(
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Text(
                    text = "Configuración",
                    style = MaterialTheme.typography.titleMedium
                )

                AppCard {
                    Column {
                        SettingsItem(
                            icon = Icons.Default.Notifications,
                            title = "Notificaciones",
                            onClick = { }
                        )
                        HorizontalDivider(color = AppColors.Border)
                        SettingsItem(
                            icon = Icons.Default.Language,
                            title = "Idioma",
                            onClick = { }
                        )
                        HorizontalDivider(color = AppColors.Border)
                        SettingsItem(
                            icon = Icons.Default.Help,
                            title = "Ayuda y soporte",
                            onClick = { }
                        )
                        HorizontalDivider(color = AppColors.Border)
                        SettingsItem(
                            icon = Icons.Default.Info,
                            title = "Acerca de",
                            onClick = { }
                        )
                    }
                }
            }
        }

        // Botón de logout
        item {
            OutlinedButton(
                onClick = onLogout,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.outlinedButtonColors(
                    contentColor = AppColors.Destructive
                )
            ) {
                Icon(
                    imageVector = Icons.Default.Logout,
                    contentDescription = null,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("Cerrar Sesión")
            }
        }

        item {
            Spacer(modifier = Modifier.height(80.dp))
        }
    }
}

@Composable
private fun ProfileInfoCard(
    label: String,
    value: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector
) {
    AppCard {
        Row(
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = AppColors.Primary,
                modifier = Modifier.size(24.dp)
            )
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = label,
                    style = MaterialTheme.typography.bodySmall,
                    color = AppColors.MutedForeground
                )
                Text(
                    text = value,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}

@Composable
private fun SettingsItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    title: String,
    onClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = AppColors.MutedForeground,
            modifier = Modifier.size(24.dp)
        )
        Text(
            text = title,
            style = MaterialTheme.typography.bodyMedium,
            modifier = Modifier.weight(1f)
        )
        Icon(
            imageVector = Icons.Default.ChevronRight,
            contentDescription = null,
            tint = AppColors.MutedForeground,
            modifier = Modifier.size(20.dp)
        )
    }
}