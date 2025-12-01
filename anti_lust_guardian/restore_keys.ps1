# Fix Key parameters - add them back properly with super.key
$replacements = @{
    "lib\screens\auth\login_screen.dart"        = @{
        "const LoginScreen({super.key})" = "const LoginScreen({Key? key}) : super(key: key)"
    }
    "lib\screens\auth\signup_screen.dart"       = @{
        "const SignUpScreen({super.key})" = "const SignUpScreen({Key? key}) : super(key: key)"
    }
    "lib\screens\block_page.dart"               = @{
        "const BlockPageScreen({super.key})" = "const BlockPageScreen({Key? key}) : super(key: key)"
    }
    "lib\screens\dashboard.dart"                = @{
        "const DashboardScreen({super.key})" = "const DashboardScreen({Key? key}) : super(key: key)"
    }
    "lib\screens\focus_horizon.dart"            = @{
        "const FocusHorizonScreen({super.key})" = "const FocusHorizonScreen({Key? key}) : super(key: key)"
    }
    "lib\screens\paywall_screen.dart"           = @{
        "const PaywallScreen({super.key})" = "const PaywallScreen({Key? key}) : super(key: key)"
    }
    "lib\screens\premium_dashboard_screen.dart" = @{
        "const PremiumDashboardScreen({super.key})" = "const PremiumDashboardScreen({Key? key}) : super(key: key)"
    }
    "lib\ui\education_hub.dart"                 = @{
        "const EducationHub({super.key})" = "const EducationHub({Key? key}) : super(key: key)"
    }
    "lib\ui\holographic_dashboard.dart"         = @{
        "const HolographicDashboard({super.key})" = "const HolographicDashboard({Key? key}) : super(key: key)"
    }
    "lib\ui\parent_dashboard.dart"              = @{
        "const ParentDashboard({super.key})" = "const ParentDashboard({Key? key}) : super(key: key)"
    }
    "lib\ui\privacy_dashboard.dart"             = @{
        "const PrivacyDashboard({super.key})" = "const PrivacyDashboard({Key? key}) : super(key: key)"
    }
}

foreach ($file in $replacements.Keys) {
    $path = Join-Path "e:\Anti-Lust app\anti_lust_guardian" $file
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        foreach ($old in $replacements[$file].Keys) {
            $new = $replacements[$file][$old]
            $content = $content -replace [regex]::Escape($old), $new
        }
        Set-Content -Path $path -Value $content -NoNewline
        Write-Host "Fixed: $file"
    }
}
Write-Host "Done! Key parameters restored."
