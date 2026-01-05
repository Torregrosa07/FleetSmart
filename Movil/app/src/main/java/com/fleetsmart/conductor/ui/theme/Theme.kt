package com.fleetsmart.conductor.ui.theme

import  androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF2196F3),
    primaryContainer = Color(0xFFBBDEFB),
    secondary = Color(0xFF4CAF50),
    secondaryContainer = Color(0xFFC8E6C9),
    background = Color(0xFFF5F5F5),
    surface = Color.White
)

@Composable
fun FleetSmartConductorTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = LightColorScheme,
        content = content
    )
}
