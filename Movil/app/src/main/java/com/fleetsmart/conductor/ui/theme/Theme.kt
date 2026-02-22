package com.fleetsmart.conductor.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val LightColorScheme = lightColorScheme(
    primary = AppColors.Primary,
    onPrimary = AppColors.PrimaryForeground,

    secondary = AppColors.Secondary,
    onSecondary = AppColors.SecondaryForeground,

    tertiary = AppColors.Accent,
    onTertiary = AppColors.AccentForeground,

    background = AppColors.Background,
    onBackground = AppColors.Foreground,

    surface = AppColors.Card,
    onSurface = AppColors.CardForeground,

    // Importante para Inputs y Cards secundarios
    surfaceVariant = AppColors.Muted,
    onSurfaceVariant = AppColors.MutedForeground,

    error = AppColors.Destructive,
    onError = AppColors.DestructiveForeground,

    outline = AppColors.Border
)

@Composable
fun MockUpsFleetSmartMovilTheme(
    darkTheme: Boolean = isSystemInDarkTheme(), // Forzamos modo claro por ahora si lo prefieres
    content: @Composable () -> Unit
) {
    // Usamos siempre el esquema claro basado en tus colores azules
    MaterialTheme(
        colorScheme = LightColorScheme,
        typography = Typography, // Asegúrate de tener Typography definido o usa MaterialTheme.typography
        content = content
    )
}