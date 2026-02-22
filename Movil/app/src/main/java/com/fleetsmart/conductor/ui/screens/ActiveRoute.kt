package com.fleetsmart.conductor.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.Circle
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.viewmodel.compose.viewModel
import com.fleetsmart.conductor.ui.theme.AppColors
import com.fleetsmart.conductor.ui.viewmodel.ActiveRouteViewModel
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapView
import org.osmdroid.views.overlay.Marker
import org.osmdroid.views.overlay.Polyline

@Composable
fun ActiveRouteScreen(
    onBack: () -> Unit,
    viewModel: ActiveRouteViewModel = viewModel()
) {
    val state by viewModel.state.collectAsState()

    val completedCount = state.stops.count { it.completed }
    val totalCount = state.stops.size
    val currentProgress = if (totalCount > 0) completedCount.toFloat() / totalCount else 0f

    // NOTA: Hemos quitado el LaunchedEffect de configuración porque ya está en MainActivity

    Column(modifier = Modifier.fillMaxSize().background(AppColors.Background)) {
        // --- Header con Progreso ---
        Surface(shadowElevation = 4.dp, color = AppColors.Card) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Volver", tint = AppColors.Foreground)
                    }
                    Column(modifier = Modifier.weight(1f)) {
                        Text(state.routeName, fontWeight = FontWeight.Bold, color = AppColors.Foreground)
                        Text("${state.distance} · ${state.duration}", style = MaterialTheme.typography.bodySmall, color = AppColors.MutedForeground)
                    }
                    Text("${(currentProgress * 100).toInt()}%", color = AppColors.Primary, fontWeight = FontWeight.Bold)
                }
                Spacer(modifier = Modifier.height(8.dp))
                LinearProgressIndicator(
                    progress = { currentProgress },
                    modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)),
                    color = AppColors.Primary,
                    trackColor = AppColors.Muted
                )
            }
        }

        // --- Contenido Scrollable ---
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // --- MAPA REAL OSMDROID ---
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(350.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color.LightGray)
                ) {
                    AndroidView(
                        factory = { ctx ->
                            MapView(ctx).apply {
                                setTileSource(TileSourceFactory.MAPNIK)
                                setMultiTouchControls(true)
                                controller.setZoom(14.0)

                                val startPoint = GeoPoint(40.4168, -3.7038) // Puerta del Sol
                                controller.setCenter(startPoint)

                                val routePoints = listOf(
                                    GeoPoint(40.4168, -3.7038),
                                    GeoPoint(40.4200, -3.6960),
                                    GeoPoint(40.4240, -3.6880),
                                    GeoPoint(40.4150, -3.6840)
                                )

                                val line = Polyline()
                                line.setPoints(routePoints)
                                line.outlinePaint.color = android.graphics.Color.parseColor("#2563EB")
                                line.outlinePaint.strokeWidth = 15f
                                overlays.add(line)

                                routePoints.forEachIndexed { index, point ->
                                    val marker = Marker(this)
                                    marker.position = point
                                    marker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_BOTTOM)
                                    marker.title = "Parada ${index + 1}"
                                    overlays.add(marker)
                                }
                            }
                        },
                        modifier = Modifier.fillMaxSize()
                    )

                    FloatingActionButton(
                        onClick = { /* Centrar */ },
                        modifier = Modifier
                            .align(Alignment.BottomEnd)
                            .padding(16.dp)
                            .size(48.dp),
                        containerColor = AppColors.Card,
                        contentColor = AppColors.Primary
                    ) {
                        Icon(Icons.Default.MyLocation, contentDescription = "Mi Ubicación")
                    }
                }
            }

            // --- Controles de la Ruta ---
            item {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    OutlinedButton(
                        onClick = { viewModel.togglePauseRoute() },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.outlinedButtonColors(
                            contentColor = AppColors.Primary
                        ),
                        border = androidx.compose.foundation.BorderStroke(1.dp, AppColors.Primary)
                    ) {
                        Icon(if (state.isPaused) Icons.Default.PlayCircle else Icons.Default.PauseCircle, null)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(if (state.isPaused) "Reanudar" else "Pausar")
                    }
                    Button(
                        onClick = {
                            viewModel.finishRoute()
                            onBack()
                        },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = AppColors.Destructive)
                    ) {
                        Text("Finalizar")
                    }
                }
            }

            // --- Lista de paradas ---
            item {
                Text(
                    "Paradas de la Ruta",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = AppColors.Foreground
                )
            }

            items(state.stops) { stop ->
                Card(
                    colors = CardDefaults.cardColors(
                        containerColor = if (stop.completed) AppColors.Muted else AppColors.Card
                    ),
                    border = androidx.compose.foundation.BorderStroke(1.dp, AppColors.Border)
                ) {
                    Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.Top) {
                        IconButton(
                            onClick = { viewModel.toggleStopComplete(stop.id) },
                            modifier = Modifier.size(24.dp)
                        ) {
                            Icon(
                                if (stop.completed) Icons.Default.CheckCircle else Icons.Outlined.Circle,
                                null,
                                tint = if (stop.completed) AppColors.Success else AppColors.MutedForeground
                            )
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(
                                text = stop.address,
                                color = if (stop.completed) AppColors.MutedForeground else AppColors.Foreground,
                                textDecoration = if (stop.completed) androidx.compose.ui.text.style.TextDecoration.LineThrough else null
                            )
                            if (stop.phone != null && !stop.completed) {
                                Button(
                                    onClick = {},
                                    modifier = Modifier.padding(top = 8.dp).height(32.dp),
                                    contentPadding = PaddingValues(horizontal = 12.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = AppColors.Primary)
                                ) {
                                    Icon(Icons.Default.Phone, null, modifier = Modifier.size(12.dp))
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text("Llamar", fontSize = 12.sp)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}