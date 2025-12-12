# Quick Commands to Clean Up .env for Production

# Option 1: Remove PARENT_ALERT_EMAIL line (Recommended)
# On PowerShell:
(Get-Content .env) | Where-Object { $_ -notmatch 'PARENT_ALERT_EMAIL' } | Set-Content .env.clean
Move-Item .env.clean .env -Force

# Option 2: Comment out PARENT_ALERT_EMAIL (for reference)
(Get-Content .env) | ForEach-Object { $_ -replace '^PARENT_ALERT_EMAIL=', '# PARENT_ALERT_EMAIL=' } | Set-Content .env

# Verify the change
type .env | findstr PARENT_ALERT_EMAIL
