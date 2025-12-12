package com.antilust.guardian

import android.app.admin.DeviceAdminReceiver
import android.app.admin.DevicePolicyManager
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.net.HttpURLConnection
import java.net.URL

class AntiLustDeviceAdminReceiver : DeviceAdminReceiver() {
    
    override fun onEnabled(context: Context, intent: Intent) {
        super.onEnabled(context, intent)
        Log.d("DeviceAdmin", "Device Admin enabled")
    }
    
    override fun onDisabled(context: Context, intent: Intent) {
        super.onDisabled(context, intent)
        Log.d("DeviceAdmin", "Device Admin disabled - sending alert")
        
        // Send uninstall alert to backend
        sendUninstallAlert(context)
    }
    
    override fun onDisableRequested(context: Context, intent: Intent): CharSequence {
        // Show warning before allowing Device Admin to be disabled
        return "Warning: Disabling Device Admin will allow the app to be uninstalled. Parent will be notified."
    }
    
    private fun sendUninstallAlert(context: Context) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val backendUrl = "https://anti-lust-backend-77553493618.us-central1.run.app"
                val url = URL("$backendUrl/api/alerts/uninstall-attempt")
                val connection = url.openConnection() as HttpURLConnection
                
connection.requestMethod = "POST"
                connection.setRequestProperty("Content-Type", "application/json")
                connection.doOutput = true
                
                val jsonPayload = """
                    {
                        "event": "uninstall_attempt",
                        "timestamp": "${System.currentTimeMillis()}",
                        "severity": "critical"
                    }
                """.trimIndent()
                
                connection.outputStream.use { it.write(jsonPayload.toByteArray()) }
                
                val responseCode = connection.responseCode
                Log.d("DeviceAdmin", "Alert sent. Response code: $responseCode")
                
                connection.disconnect()
            } catch (e: Exception) {
                Log.e("DeviceAdmin", "Failed to send alert: ${e.message}")
            }
        }
    }
}

class DeviceAdminHelper(private val context: Context) {
    
    private val devicePolicyManager: DevicePolicyManager =
        context.getSystemService(Context.DEVICE_POLICY_SERVICE) as DevicePolicyManager
    
    private val componentName: ComponentName =
        ComponentName(context, AntiLustDeviceAdminReceiver::class.java)
    
    fun isDeviceAdmin(): Boolean {
        return devicePolicyManager.isAdminActive(componentName)
    }
    
    fun requestDeviceAdmin(activity: android.app.Activity) {
        if (!isDeviceAdmin()) {
            val intent = Intent(DevicePolicyManager.ACTION_ADD_DEVICE_ADMIN)
            intent.putExtra(DevicePolicyManager.EXTRA_DEVICE_ADMIN, componentName)
            intent.putExtra(
                DevicePolicyManager.EXTRA_ADD_EXPLANATION,
                "Anti-Lust Guardian requires Device Admin to prevent unauthorized uninstallation and protect your digital well-being."
            )
            activity.startActivityForResult(intent, REQUEST_CODE_DEVICE_ADMIN)
        }
    }
    
    companion object {
        const val REQUEST_CODE_DEVICE_ADMIN = 1002
    }
}
