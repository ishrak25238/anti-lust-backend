
package com.antilust.guardian

import android.content.Intent
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity: FlutterFragmentActivity() {
    private val SCREEN_CAPTURE_CHANNEL = "anti_lust/screen_capture"
    private val DEVICE_ADMIN_CHANNEL = "anti_lust/device_admin"
    
    private lateinit var screenCaptureService: ScreenCaptureService
    private lateinit var deviceAdminHelper: DeviceAdminHelper
    
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        
        screenCaptureService = ScreenCaptureService(this)
        deviceAdminHelper = DeviceAdminHelper(this)
        
        // Screen Capture Channel
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, SCREEN_CAPTURE_CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "captureScreen" -> {
                    screenCaptureService.requestScreenCapture(result)
                }
                else -> {
                    result.notImplemented()
                }
            }
        }
        
        // Device Admin Channel
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, DEVICE_ADMIN_CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "requestDeviceAdmin" -> {
                    deviceAdminHelper.requestDeviceAdmin(this)
                    result.success(null)
                }
                "isDeviceAdmin" -> {
                    result.success(deviceAdminHelper.isDeviceAdmin())
                }
                else -> {
                    result.notImplemented()
                }
            }
        }
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        
        // Handle screen capture result
        if (requestCode == ScreenCaptureService.REQUEST_CODE_SCREEN_CAPTURE) {
            screenCaptureService.handleActivityResult(requestCode, resultCode, data)
        }
        
        // Handle device admin result
        if (requestCode == DeviceAdminHelper.REQUEST_CODE_DEVICE_ADMIN) {
            // Device admin result handled automatically
        }
    }
}
