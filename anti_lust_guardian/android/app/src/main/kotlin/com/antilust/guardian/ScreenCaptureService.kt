package com.antilust.guardian

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.PixelFormat
import android.hardware.display.DisplayManager
import android.hardware.display.VirtualDisplay
import android.media.Image
import android.media.ImageReader
import android.media.projection.MediaProjection
import android.media.projection.MediaProjectionManager
import android.os.Handler
import android.os.Looper
import android.util.DisplayMetrics
import io.flutter.plugin.common.MethodChannel
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer

class ScreenCaptureService(private val activity: Activity) {
    private var mediaProjection: MediaProjection? = null
    private var imageReader: ImageReader? = null
    private var virtualDisplay: VirtualDisplay? = null
    private val handler = Handler(Looper.getMainLooper())
    
    companion object {
        const val REQUEST_CODE_SCREEN_CAPTURE = 1001
        private var pendingResult: MethodChannel.Result? = null
    }
    
    fun requestScreenCapture(result: MethodChannel.Result) {
        pendingResult = result
        
        val mediaProjectionManager = activity.getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        val captureIntent = mediaProjectionManager.createScreenCaptureIntent()
        activity.startActivityForResult(captureIntent, REQUEST_CODE_SCREEN_CAPTURE)
    }
    
    fun handleActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode == REQUEST_CODE_SCREEN_CAPTURE) {
            if (resultCode == Activity.RESULT_OK && data != null) {
                startScreenCapture(data)
            } else {
                pendingResult?.error("PERMISSION_DENIED", "Screen capture permission denied", null)
                pendingResult = null
            }
        }
    }
    
    private fun startScreenCapture(data: Intent) {
        val mediaProjectionManager = activity.getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        mediaProjection = mediaProjectionManager.getMediaProjection(Activity.RESULT_OK, data)
        
        val metrics = DisplayMetrics()
        activity.windowManager.defaultDisplay.getMetrics(metrics)
        val density = metrics.densityDpi
        val width = metrics.widthPixels
        val height = metrics.heightPixels
        
        imageReader = ImageReader.newInstance(width, height, PixelFormat.RGBA_8888, 2)
        
        virtualDisplay = mediaProjection?.createVirtualDisplay(
            "AntiLustScreenCapture",
            width, height, density,
            DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
            imageReader?.surface, null, handler
        )
        
        // Capture after a short delay to let display stabilize
        handler.postDelayed({
            captureScreen()
        }, 100)
    }
    
    private fun captureScreen() {
        try {
            val image: Image? = imageReader?.acquireLatestImage()
            if (image != null) {
                val planes = image.planes
                val buffer: ByteBuffer = planes[0].buffer
                val pixelStride = planes[0].pixelStride
                val rowStride = planes[0].rowStride
                val rowPadding = rowStride - pixelStride * image.width
                
                val bitmap = Bitmap.createBitmap(
                    image.width + rowPadding / pixelStride,
                    image.height,
                    Bitmap.Config.ARGB_8888
                )
                bitmap.copyPixelsFromBuffer(buffer)
                
                // Convert bitmap to JPEG bytes
                val stream = ByteArrayOutputStream()
                bitmap.compress(Bitmap.CompressFormat.JPEG, 85, stream)
                val imageBytes = stream.toByteArray()
                
                // Return to Flutter
                pendingResult?.success(imageBytes)
                pendingResult = null
                
                image.close()
                bitmap.recycle()
                
                // Cleanup
                cleanup()
            } else {
                pendingResult?.error("CAPTURE_FAILED", "Failed to acquire image", null)
                pendingResult = null
                cleanup()
            }
        } catch (e: Exception) {
            pendingResult?.error("CAPTURE_ERROR", e.message, null)
            pendingResult = null
            cleanup()
        }
    }
    
    private fun cleanup() {
        virtualDisplay?.release()
        imageReader?.close()
        mediaProjection?.stop()
        virtualDisplay = null
        imageReader = null
        mediaProjection = null
    }
}
