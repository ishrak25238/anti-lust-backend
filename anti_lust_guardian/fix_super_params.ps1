# PowerShell script to fix all super parameter warnings
# This converts `{Key? key} : super(key: key)` to `{super.key}`

$files = @(
    "lib\app.dart",
    "lib\main.dart",
    "lib\screens\auth\login_screen.dart",
    "lib\screens\auth\role_selection_screen.dart",
    "lib\screens\auth\signup_screen.dart",
    "lib\screens\block_page.dart",
    "lib\screens\dashboard.dart",
    "lib\screens\focus_horizon.dart",
    "lib\screens\paywall_screen.dart",
    "lib\screens\premium_dashboard_screen.dart",
    "lib\ui\consent_modal.dart",
    "lib\ui\education_hub.dart",
    "lib\ui\holographic_dashboard.dart",
    "lib\ui\parent_dashboard.dart",
    "lib\ui\particle_background.dart",
    "lib\ui\privacy_dashboard.dart"
)

foreach ($file in $files) {
    $path = Join-Path "e:\Anti-Lust app\anti_lust_guardian" $file
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        
        # Pattern 1: {Key? key} : super(key: key)  →  {super.key}
        $content = $content -replace '\{Key\? key\}(\s*):(\s*)super\(key:\s*key\)', '{super.key}'
        
        # Pattern 2: {Key? key, other params} : super(key: key)  →  {super.key, other params}
        $content = $content -replace '\{Key\? key,\s*', '{super.key, '
        $content = $content -replace '\}\s*:\s*super\(key:\s*key\)', '}'
        
        Set-Content -Path $path -Value $content -NoNewline
        Write-Host "Fixed: $file"
    }
}

Write-Host "Done! All super parameters fixed."
