@echo off
title CloudMark - Vultr Status Check
color 0A
cls

echo ========================================================
echo         CloudMark Vultr Status and Access Checker
echo ========================================================
echo.

echo [1/3] Detecting Current Public IP Addresses...
for /f "tokens=*" %%a in ('powershell -Command "(Invoke-WebRequest -Uri https://api.ipify.org -UseBasicParsing).Content"') do set IPV4=%%a
echo   IPv4: %IPV4%

for /f "tokens=*" %%a in ('powershell -Command "try { (Invoke-WebRequest -Uri https://api6.ipify.org -UseBasicParsing -TimeoutSec 3).Content } catch { 'Not Active' }"') do set IPV6=%%a
echo   IPv6: %IPV6%
echo.

echo [2/3] Checking Vultr Account Info and API Access...
echo --------------------------------------------------------
"%~dp0bin\vultr\vultr-cli.exe" account info
if %errorlevel% neq 0 (
    echo.
    echo [!] ACCESS DENIED: Your current IP is not whitelisted on Vultr.
    echo     Please visit: https://my.vultr.com/settings/#settingsapi
    echo     Add IPv4: %IPV4%
    echo     Add IPv6: %IPV6%
    echo     Or enable "Allow All IPv4 / IPv6"
    echo.
) else (
    echo.
    echo [OK] API Access Authorized!
    echo.
)

echo --------------------------------------------------------
echo [3/3] Checking Active Running Instances...
echo --------------------------------------------------------
"%~dp0bin\vultr\vultr-cli.exe" instance list
echo.
echo ========================================================
echo Done. Press any key to exit...
pause >nul
