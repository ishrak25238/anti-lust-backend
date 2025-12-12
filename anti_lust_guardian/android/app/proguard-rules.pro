# Flutter & Dart
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.**  { *; }
-keep class io.flutter.util.**  { *; }
-keep class io.flutter.view.**  { *; }
-keep class io.flutter.**  { *; }
-keep class io.flutter.plugins.**  { *; }

# ML Kit Text Recognition
-dontwarn com.google.mlkit.vision.text.**
-keep class com.google.mlkit.vision.text.** { *; }

# TFLite Flutter
-dontwarn org.tensorflow.lite.**
-keep class org.tensorflow.lite.** { *; }
-dontwarn com.google.android.gms.internal.mlkit_vision_text_common.**

# Stripe
-dontwarn com.stripe.**
-keep class com.stripe.** { *; }
-dontwarn com.reactnativestripesdk.**

# Android General
-dontwarn javax.annotation.**
-keepattributes *Annotation*
-dontwarn sun.misc.**
-keep class com.google.android.gms.** { *; }
-dontwarn com.google.android.gms.**
-keep class androidx.** { *; }
-keep class android.support.** { *; }
-keep class **.R$* { *; }
-keep class **.R { *; }

# Flutter Jailbreak Detection (if used)
-keep class com.jailbreak.** { *; }

# Prevent R8 from removing TFLite classes typically accessed via JNI
-keep class org.tensorflow.lite.Interpreter** { *; }

# Google Play Core (Deferred Components / Split Install)
-dontwarn com.google.android.play.core.**
-keep class com.google.android.play.core.** { *; }

# Flutter Deferred Components
-dontwarn io.flutter.embedding.engine.deferredcomponents.**
-keep class io.flutter.embedding.engine.deferredcomponents.** { *; }
-dontwarn io.flutter.app.FlutterPlayStoreSplitApplication
