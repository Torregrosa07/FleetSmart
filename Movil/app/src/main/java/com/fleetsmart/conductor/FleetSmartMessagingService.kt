package com.fleetsmart.conductor

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.annotation.RequiresApi
import androidx.core.app.NotificationCompat
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class FleetSmartMessagingService : FirebaseMessagingService() {

    companion object {
        const val CHANNEL_ID = "fleetsmart_notifications"
        const val CHANNEL_NAME = "FleetSmart"
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        // Guardar el nuevo token en Firebase si hay sesión activa
        val prefs = getSharedPreferences("fleetsmart_prefs", Context.MODE_PRIVATE)
        val idConductor = prefs.getString("id_conductor", null)
        if (idConductor != null) {
            guardarTokenEnFirebase(idConductor, token)
        }
    }

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)

        val titulo = remoteMessage.notification?.title ?: "FleetSmart"
        val cuerpo = remoteMessage.notification?.body ?: ""

        mostrarNotificacion(titulo, cuerpo)
    }

    private fun guardarTokenEnFirebase(idConductor: String, token: String) {
        FirebaseDatabase.getInstance()
            .getReference("conductores/$idConductor/fcm_token")
            .setValue(token)
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun mostrarNotificacion(titulo: String, cuerpo: String) {
        val notificationManager =
            getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // Crear canal (Android 8+)
        val channel = NotificationChannel(
            CHANNEL_ID,
            CHANNEL_NAME,
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Notificaciones de FleetSmart"
            enableVibration(true)
        }
        notificationManager.createNotificationChannel(channel)

        // Intent para abrir la app al pulsar la notificación
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle(titulo)
            .setContentText(cuerpo)
            .setStyle(NotificationCompat.BigTextStyle().bigText(cuerpo))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .build()

        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }
}