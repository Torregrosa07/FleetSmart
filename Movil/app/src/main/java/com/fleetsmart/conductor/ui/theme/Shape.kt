package com.fleetsmart.conductor.ui.theme

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Shapes
import androidx.compose.ui.unit.dp

val Shapes = Shapes(
    small = RoundedCornerShape(6.dp),      // 0.625rem - 4px = 6dp
    medium = RoundedCornerShape(8.dp),     // 0.625rem - 2px = 8dp
    large = RoundedCornerShape(10.dp),     // 0.625rem = 10dp
    extraLarge = RoundedCornerShape(14.dp) // 0.625rem + 4px = 14dp
)