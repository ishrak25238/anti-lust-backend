# Anti-Lust Guardian - Flutter Installation Script
# Run this in PowerShell (Administrator)

Write-Host "`n🚀 Anti-Lust Guardian - Automated Setup`n" -ForegroundColor Cyan

# Step 1: Download Flutter SDK
Write-Host "[Step 1/4] Downloading Flutter SDK..." -ForegroundColor Yellow
$flutterUrl = "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.16.0-stable.zip"
$downloadPath = "$env:USERPROFILE\Downloads\flutter_sdk.zip"

try {
    Invoke-WebRequest -Uri $flutterUrl -OutFile $downloadPath -UseBasicParsing
    Write-Host "✅ Download complete!" -ForegroundColor Green
} catch {
    Write-Host "❌ Download failed: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Extract Flutter
Write-Host "`n[Step 2/4] Extracting Flutter to C:\flutter..." -ForegroundColor Yellow

if (Test-Path "C:\flutter") {
    Write-Host "⚠️  Flutter already exists at C:\flutter. Skipping extraction." -ForegroundColor Yellow
} else {
    try {
        Expand-Archive -Path $downloadPath -DestinationPath "C:\" -Force
        Write-Host "✅ Extraction complete!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Extraction failed: $_" -ForegroundColor Red
        exit 1
    }
}

# Step 3: Add to PATH
Write-Host "`n[Step 3/4] Adding Flutter to PATH..." -ForegroundColor Yellow

$flutterBin = "C:\flutter\bin"
$currentPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')

if ($currentPath -like "*$flutterBin*") {
    Write-Host "✅ Flutter already in PATH!" -ForegroundColor Green
} else {
    try {
        $newPath = "$currentPath;$flutterBin"
        [System.Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
        Write-Host "✅ Flutter added to PATH!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to update PATH: $_" -ForegroundColor Red
        exit 1
    }
}

# Refresh PATH for current session
$env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'User')

# Step 4: Verify Installation
Write-Host "`n[Step 4/4] Verifying Flutter installation..." -ForegroundColor Yellow

try {
    $flutterVersion = & "C:\flutter\bin\flutter.bat" --version 2>&1
    Write-Host "✅ Flutter installed successfully!" -ForegroundColor Green
    Write-Host "`n$flutterVersion`n" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Flutter verification failed" -ForegroundColor Red
    Write-Host "Please close and reopen PowerShell, then run: flutter --version" -ForegroundColor Yellow
}

# Next Steps
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ Flutter SDK Installation Complete!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Close and reopen PowerShell (to reload PATH)" -ForegroundColor White
Write-Host "  2. Run: flutter doctor" -ForegroundColor White
Write-Host "  3. Setup your .env file (copy from .env.example)" -ForegroundColor White
Write-Host "  4. Run: cd 'e:\Anti-Lust app\anti_lust_guardian'" -ForegroundColor White
Write-Host "  5. Run: flutter pub get" -ForegroundColor White
Write-Host "  6. Run: flutter run -d windows`n" -ForegroundColor White

Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "  - QUICK_START.md - Full setup guide" -ForegroundColor White
Write-Host "  - DEPLOYMENT.md - Production builds" -ForegroundColor White
Write-Host "  - walkthrough.md - Complete project overview`n" -ForegroundColor White

Write-Host "🎉 Your Anti-Lust Guardian app is ready to run!" -ForegroundColor Green
