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

    Column(modifier = Modifier.fillMaxSize().background(AppColors.Background)) {

        // --- Header con Progreso ---
        Surface(shadowElevation = 4.dp, color = AppColors.Card) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Volver", tint = AppColors.Foreground)
                    }
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            state.routeName.ifEmpty { "Cargando ruta..." },
                            fontWeight = FontWeight.Bold,
                            color = AppColors.Foreground
                        )
                        Text(
                            "${state.distance} · ${state.duration}",
                            style = MaterialTheme.typography.bodySmall,
                            color = AppColors.MutedForeground
                        )
                    }
                    Text(
                        "${(currentProgress * 100).toInt()}%",
                        color = AppColors.Primary,
                        fontWeight = FontWeight.Bold
                    )
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

        // --- Contenido ---
        if (state.isLoading) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator(color = AppColors.Primary)
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {

                // --- MAPA CON DATOS REALES ---
                item {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(350.dp)
                            .clip(RoundedCornerShape(12.dp))
                            .background(Color.LightGray)
                    ) {
                        // Capturamos los puntos antes del AndroidView para evitar recomposición
                        val routePoints = state.routePoints
                        val centerLat = state.centerLat
                        val centerLon = state.centerLon

                        AndroidView(
                            factory = { ctx ->
                                MapView(ctx).apply {
                                    setTileSource(TileSourceFactory.MAPNIK)
                                    setMultiTouchControls(true)
                                }
                            },
                            update = { mapView ->
                                mapView.overlays.clear()

                                if (routePoints.isNotEmpty()) {
                                    // Centrar el mapa en la primera parada
                                    mapView.controller.setZoom(14.0)
                                    mapView.controller.setCenter(GeoPoint(centerLat, centerLon))

                                    // Dibujar la línea de ruta
                                    val geoPoints = routePoints.map { (lat, lon) -> GeoPoint(lat, lon) }

                                    val line = Polyline()
                                    line.setPoints(geoPoints)
                                    line.outlinePaint.color = android.graphics.Color.parseColor("#2563EB")
                                    line.outlinePaint.strokeWidth = 15f
                                    mapView.overlays.add(line)

                                    // Marcadores para cada parada
                                    geoPoints.forEachIndexed { index, point ->
                                        val marker = Marker(mapView)
                                        marker.position = point
                                        marker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_BOTTOM)
                                        marker.title = when (index) {
                                            0 -> "Inicio"
                                            geoPoints.size - 1 -> "Destino final"
                                            else -> "Parada ${index + 1}"
                                        }
                                        mapView.overlays.add(marker)
                                    }
                                } else {
                                    // Sin coordenadas: vista por defecto de Madrid
                                    mapView.controller.setZoom(12.0)
                                    mapView.controller.setCenter(GeoPoint(40.4168, -3.7038))
                                }

                                mapView.invalidate()
                            },
                            modifier = Modifier.fillMaxSize()
                        )

                        FloatingActionButton(
                            onClick = { /* Centrar en ubicación actual */ },
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
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        OutlinedButton(
                            onClick = { viewModel.togglePauseRoute() },
                            modifier = Modifier.weight(1f),
                            colors = ButtonDefaults.outlinedButtonColors(
                                contentColor = AppColors.Primary
                            ),
                            border = androidx.compose.foundation.BorderStroke(1.dp, AppColors.Primary)
                        ) {
                            Icon(
                                if (state.isPaused) Icons.Default.PlayCircle else Icons.Default.PauseCircle,
                                null
                            )
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

                if (state.stops.isEmpty()) {
                    item {
                        Box(
                            modifier = Modifier.fillMaxWidth().padding(32.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                "No hay paradas registradas para esta ruta",
                                color = AppColors.MutedForeground,
                                style = MaterialTheme.typography.bodyMedium
                            )
                        }
                    }
                } else {
                    items(state.stops) { stop ->
                        Card(
                            colors = CardDefaults.cardColors(
                                containerColor = if (stop.completed) AppColors.Muted else AppColors.Card
                            ),
                            border = androidx.compose.foundation.BorderStroke(1.dp, AppColors.Border)
                        ) {
                            Row(
                                modifier = Modifier.padding(16.dp),
                                verticalAlignment = Alignment.Top
                            ) {
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
                                        textDecoration = if (stop.completed)
                                            androidx.compose.ui.text.style.TextDecoration.LineThrough
                                        else null
                                    )
                                    if (stop.phone != null && !stop.completed) {
                                        Button(
                                            onClick = {},
                                            modifier = Modifier.padding(top = 8.dp).height(32.dp),
                                            contentPadding = PaddingValues(horizontal = 12.dp),
                                            colors = ButtonDefaults.buttonColors(containerColor = AppColors.Primary)
                                        ) {
                                            Icon(
                                                Icons.Default.Phone,
                                                null,
                                                modifier = Modifier.size(12.dp)
                                            )
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
    }
}