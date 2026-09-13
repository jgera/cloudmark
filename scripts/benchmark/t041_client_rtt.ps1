<#
.SYNOPSIS
    CBP-1.0 / T041 — End-User RTT / Geographic Latency
.DESCRIPTION
    Measures interactive network latency from the client's local network (e.g., North India)
    to the target instance. Logs raw output and calculates min/avg/max RTT.
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$HostIp,

    [Parameter(Mandatory=$true)]
    [string]$RunId,

    [int]$Count = 50
)

$rawDir = "d:\Projects\CloudMark\runs\$RunId\raw"
if (-not (Test-Path $rawDir)) {
    New-Item -ItemType Directory -Force -Path $rawDir | Out-Null
}
$rawFile = "$rawDir\T041_raw.log"

Write-Host "========================================="
Write-Host "=== CBP-1.0 / T041: CLIENT RTT TO $HostIp ==="
Write-Host "=== Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC' -AsUTC) ==="
Write-Host "========================================="

$logHeader = @"
=========================================
=== CBP-1.0 / T041: CLIENT RTT TO $HostIp ===
=== Client Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC' -AsUTC) ===
=== Target IP: $HostIp ===
=========================================
"@
$logHeader | Out-File -FilePath $rawFile -Encoding utf8

Write-Host "Executing $Count ICMP echo requests to $HostIp..."
$pingOutput = ping -n $Count $HostIp
$pingOutput | Out-File -FilePath $rawFile -Append -Encoding utf8
$pingOutput | Write-Host

Write-Host "`nExecuting traceroute to $HostIp..."
"`n--- TRACEROUTE ---" | Out-File -FilePath $rawFile -Append -Encoding utf8
$tracertOutput = tracert -d -h 20 $HostIp
$tracertOutput | Out-File -FilePath $rawFile -Append -Encoding utf8
$tracertOutput | Write-Host

Write-Host "`nT041 raw log saved to: $rawFile"
