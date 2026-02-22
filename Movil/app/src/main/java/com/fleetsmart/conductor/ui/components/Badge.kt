package com.fleetsmart.conductor.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.fleetsmart.conductor.ui.theme.AppColors

enum class BadgeVariant {
    DEFAULT,
    SECONDARY,
    OUTLINE,
    SUCCESS,
    WARNING,
    DESTRUCTIVE
}

@Composable
fun Badge(
    text: String,
    modifier: Modifier = Modifier,
    variant: BadgeVariant = BadgeVariant.DEFAULT
) {
    val (backgroundColor, textColor) = when (variant) {
        BadgeVariant.DEFAULT -> AppColors.Primary to AppColors.PrimaryForeground
        BadgeVariant.SECONDARY -> AppColors.Secondary to AppColors.SecondaryForeground
        BadgeVariant.OUTLINE -> Color.Transparent to AppColors.Foreground
        BadgeVariant.SUCCESS -> AppColors.SuccessBackground to AppColors.Success
        BadgeVariant.WARNING -> AppColors.WarningBackground to AppColors.Warning
        BadgeVariant.DESTRUCTIVE -> AppColors.Destructive to AppColors.DestructiveForeground
    }

    Box(
        modifier = modifier
            .background(
                color = backgroundColor,
                shape = RoundedCornerShape(6.dp)
            )
            .padding(horizontal = 10.dp, vertical = 4.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.labelSmall,
            color = textColor
        )
    }
}