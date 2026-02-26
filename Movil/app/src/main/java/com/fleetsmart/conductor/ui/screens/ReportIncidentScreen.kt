package com.fleetsmart.conductor.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
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
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.fleetsmart.conductor.data.SessionManager
import com.fleetsmart.conductor.data.model.IncidentType
import com.fleetsmart.conductor.ui.components.AppCard
import com.fleetsmart.conductor.ui.theme.AppColors
import com.fleetsmart.conductor.ui.viewmodel.IncidentReportState
import com.fleetsmart.conductor.ui.viewmodel.IncidentReportViewModel

@Composable
fun ReportIncidentScreen(
    viewModel: IncidentReportViewModel = viewModel()
) {
    val state by viewModel.state.collectAsState()
    val asignacion by SessionManager.asignacionActiva.collectAsState()

    when {
        state.isSubmitted -> {
            SuccessScreen(onNuevaIncidencia = { viewModel.resetForm() })
        }
        else -> {
            IncidentFormScreen(
                state = state,
                tieneAsignacion = asignacion != null,
                onTypeSelected = { viewModel.setIncidentType(it) },
                onDescriptionChanged = { viewModel.setDescription(it) },
                onSubmit = { viewModel.submitIncident() },
                canSubmit = viewModel.canSubmit
            )
        }
    }
}

@Composable
private fun SuccessScreen(onNuevaIncidencia: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Box(
            modifier = Modifier
                .size(80.dp)
                .background(AppColors.SuccessBackground, CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Default.CheckCircle,
                contentDescription = null,
                modifier = Modifier.size(48.dp),
                tint = AppColors.Success
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = "Incidencia Reportada",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(12.dp))

        Text(
            text = "Tu reporte ha sido enviado al equipo de gestión. Lo revisarán lo antes posible.",
            style = MaterialTheme.typography.bodyMedium,
            color = AppColors.MutedForeground,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(horizontal = 32.dp)
        )

        Spacer(modifier = Modifier.height(32.dp))

        OutlinedButton(
            onClick = onNuevaIncidencia,
            colors = ButtonDefaults.outlinedButtonColors(contentColor = AppColors.Primary)
        ) {
            Icon(Icons.Default.Add, null, modifier = Modifier.size(18.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text("Reportar otra incidencia")
        }
    }
}

@Composable
private fun IncidentFormScreen(
    state: IncidentReportState,
    tieneAsignacion: Boolean,
    onTypeSelected: (IncidentType) -> Unit,
    onDescriptionChanged: (String) -> Unit,
    onSubmit: () -> Unit,
    canSubmit: Boolean
) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        // Header
        item {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    text = "Reportar Incidencia",
                    style = MaterialTheme.typography.headlineMedium
                )
                Text(
                    text = "Informa sobre cualquier problema durante tu ruta",
                    style = MaterialTheme.typography.bodyMedium,
                    color = AppColors.MutedForeground
                )
            }
        }

        // Aviso si no hay asignación activa
        if (!tieneAsignacion) {
            item {
                AppCard(modifier = Modifier.fillMaxWidth()) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.Top
                    ) {
                        Icon(
                            imageVector = Icons.Default.Info,
                            contentDescription = null,
                            tint = AppColors.Info,
                            modifier = Modifier.size(20.dp)
                        )
                        Text(
                            text = "No tienes una ruta activa. La incidencia se registrará sin datos de vehículo ni ruta.",
                            style = MaterialTheme.typography.bodySmall,
                            color = AppColors.Info
                        )
                    }
                }
            }
        }

        // Formulario
        item {
            AppCard {
                Column(verticalArrangement = Arrangement.spacedBy(24.dp)) {

                    // Tipo de incidencia
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        Text(
                            text = "Tipo de Incidencia",
                            style = MaterialTheme.typography.titleMedium
                        )
                        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(12.dp)
                            ) {
                                IncidentType.entries.take(2).forEach { type ->
                                    IncidentTypeCard(
                                        type = type,
                                        isSelected = state.selectedType == type,
                                        onClick = { onTypeSelected(type) },
                                        modifier = Modifier.weight(1f)
                                    )
                                }
                            }
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(12.dp)
                            ) {
                                IncidentType.entries.drop(2).forEach { type ->
                                    IncidentTypeCard(
                                        type = type,
                                        isSelected = state.selectedType == type,
                                        onClick = { onTypeSelected(type) },
                                        modifier = Modifier.weight(1f)
                                    )
                                }
                            }
                        }
                    }

                    // Descripción
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(
                            text = "Descripción del Problema",
                            style = MaterialTheme.typography.titleMedium
                        )
                        OutlinedTextField(
                            value = state.description,
                            onValueChange = onDescriptionChanged,
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(150.dp),
                            placeholder = {
                                Text("Describe el problema con el mayor detalle posible...")
                            },
                            isError = state.error != null,
                            colors = OutlinedTextFieldDefaults.colors(
                                unfocusedContainerColor = AppColors.InputBackground,
                                focusedContainerColor = AppColors.InputBackground,
                                focusedBorderColor = AppColors.Primary,
                                errorBorderColor = AppColors.Destructive
                            )
                        )
                        if (state.error != null) {
                            Text(
                                text = state.error,
                                style = MaterialTheme.typography.bodySmall,
                                color = AppColors.Destructive
                            )
                        }
                    }
                }
            }
        }

        // Botón enviar
        item {
            Button(
                onClick = onSubmit,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp),
                enabled = canSubmit && !state.isSubmitting,
                colors = ButtonDefaults.buttonColors(containerColor = AppColors.Primary)
            ) {
                if (state.isSubmitting) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(20.dp),
                        color = AppColors.PrimaryForeground,
                        strokeWidth = 2.dp
                    )
                } else {
                    Icon(
                        imageVector = Icons.Default.Send,
                        contentDescription = null,
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Enviar Reporte")
                }
            }
        }

        item { Spacer(modifier = Modifier.height(80.dp)) }
    }
}

@Composable
private fun IncidentTypeCard(
    type: IncidentType,
    isSelected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val borderColor = if (isSelected) AppColors.Primary else AppColors.Border
    val backgroundColor = if (isSelected) AppColors.Primary.copy(alpha = 0.05f) else AppColors.Card

    Column(
        modifier = modifier
            .height(100.dp)
            .border(
                width = 2.dp,
                color = borderColor,
                shape = MaterialTheme.shapes.medium
            )
            .background(
                color = backgroundColor,
                shape = MaterialTheme.shapes.medium
            )
            .clickable(onClick = onClick)
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = type.emoji,
            style = MaterialTheme.typography.headlineLarge
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = type.displayName,
            style = MaterialTheme.typography.bodySmall,
            textAlign = TextAlign.Center,
            maxLines = 2
        )
    }
}