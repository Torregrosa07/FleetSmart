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
import com.fleetsmart.conductor.data.model.IncidentType
import com.fleetsmart.conductor.ui.components.AppCard
import com.fleetsmart.conductor.ui.theme.AppColors
import com.fleetsmart.conductor.ui.viewmodel.IncidentReportViewModel

@Composable
fun ReportIncidentScreen(
    viewModel: IncidentReportViewModel = viewModel()
) {
    val state by viewModel.state.collectAsState()

    if (state.isSubmitted) {
        SuccessScreen()
    } else {
        IncidentFormScreen(
            state = state,
            onTypeSelected = { viewModel.setIncidentType(it) },
            onDescriptionChanged = { viewModel.setDescription(it) },
            onSubmit = { viewModel.submitIncident() },
            canSubmit = viewModel.canSubmit
        )
    }
}

@Composable
private fun SuccessScreen() {
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
            text = "Tu reporte ha sido enviado exitosamente. El equipo de gestión lo revisará pronto.",
            style = MaterialTheme.typography.bodyMedium,
            color = AppColors.MutedForeground,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(horizontal = 32.dp)
        )
    }
}

@Composable
private fun IncidentFormScreen(
    state: com.fleetsmart.conductor.ui.viewmodel.IncidentReportState,
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
            Column(
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
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

        // Form
        item {
            AppCard {
                Column(
                    verticalArrangement = Arrangement.spacedBy(24.dp)
                ) {
                    // Incident Type
                    Column(
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Text(
                            text = "Tipo de Incidencia",
                            style = MaterialTheme.typography.titleMedium
                        )

                        Column(
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
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

                    // Description
                    Column(
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
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
                            colors = OutlinedTextFieldDefaults.colors(
                                unfocusedContainerColor = AppColors.InputBackground,
                                focusedContainerColor = AppColors.InputBackground
                            )
                        )
                    }
                }
            }
        }

        // Submit Button
        item {
            Column(
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Button(
                    onClick = onSubmit,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(48.dp),
                    enabled = canSubmit && !state.isSubmitting
                ) {
                    if (state.isSubmitting) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(20.dp),
                            color = AppColors.PrimaryForeground
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

                // Warning
                AppCard(
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.Top
                    ) {
                        Icon(
                            imageVector = Icons.Default.Warning,
                            contentDescription = null,
                            tint = AppColors.Warning,
                            modifier = Modifier.size(20.dp)
                        )
                        Text(
                            text = "Si se trata de una emergencia, contacta inmediatamente con el centro de operaciones al 900 123 456",
                            style = MaterialTheme.typography.bodySmall,
                            color = AppColors.Warning
                        )
                    }
                }
            }
        }

        item {
            Spacer(modifier = Modifier.height(80.dp))
        }
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