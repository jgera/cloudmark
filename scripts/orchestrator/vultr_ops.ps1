<#
.SYNOPSIS
    CloudMark Vultr Orchestration Helper Script
.DESCRIPTION
    Wraps vultr-cli to automate listing, provisioning, SSH key management, benchmark execution, and teardown.
#>

param (
    [Parameter(Mandatory=$false)]
    [ValidateSet("list-regions", "list-plans", "list-os", "list-ssh-keys", "create-ssh-key", "create-instance", "get-instance", "delete-instance", "exec-test")]
    [string]$Action = "list-plans",

    [string]$Region = "del", # Delhi NCR
    [string]$Plan = "vhp-4c-8gb-amd",
    [string]$OsId = "1743", # Ubuntu 24.04 x64
    [string]$Label = "cloudmark-vultr-del-run01",
    [string]$InstanceId = "",
    [string]$SshKeyId = "",
    [string]$SshKeyName = "cloudmark-key",
    [string]$SshPubKeyPath = "$HOME\.ssh\id_ed25519.pub",
    [string]$SshKeyPath = "$HOME\.ssh\id_ed25519",
    [string]$HostIp = "",
    [string]$ScriptPath = "",
    [string]$RunId = "",
    [string]$TestId = ""
)

$VultrCli = "d:\Projects\CloudMark\bin\vultr\vultr-cli.exe"

function Check-VultrCli {
    if (-not (Test-Path $VultrCli)) {
        Write-Error "vultr-cli not found at $VultrCli"
        exit 1
    }
}

Check-VultrCli

switch ($Action) {
    "list-regions" {
        & $VultrCli regions list
    }

    "list-plans" {
        Write-Host "Fetching available plans..."
        & $VultrCli plans list
    }

    "list-os" {
        Write-Host "Fetching operating systems..."
        & $VultrCli os list
    }

    "list-ssh-keys" {
        & $VultrCli ssh-key list
    }

    "create-ssh-key" {
        if (-not (Test-Path $SshPubKeyPath)) {
            Write-Error "Public key not found at $SshPubKeyPath. Generate one with: ssh-keygen -t ed25519"
            exit 1
        }
        $pubKey = (Get-Content $SshPubKeyPath -Raw).Trim()
        Write-Host "Registering SSH key '$SshKeyName' with Vultr..."
        & $VultrCli ssh-key create --name $SshKeyName --key "$pubKey"
    }

    "create-instance" {
        Write-Host "Provisioning instance: $Label (Plan: $Plan, Region: $Region)..."
        $argsList = @("instance", "create", "--region", $Region, "--plan", $Plan, "--os", $OsId, "--label", $Label)
        if ($SshKeyId) {
            $argsList += @("--ssh-keys", $SshKeyId)
        }
        & $VultrCli @argsList
    }

    "get-instance" {
        if (-not $InstanceId) {
            & $VultrCli instance list
        } else {
            & $VultrCli instance get $InstanceId
        }
    }

    "delete-instance" {
        if (-not $InstanceId) {
            Write-Error "Please specify -InstanceId to delete."
            exit 1
        }
        Write-Host "Terminating instance $InstanceId..."
        & $VultrCli instance delete $InstanceId
    }

    "exec-test" {
        if (-not $HostIp -or -not $ScriptPath -or -not $RunId -or -not $TestId) {
            Write-Error "Required for exec-test: -HostIp, -ScriptPath, -RunId, -TestId"
            exit 1
        }

        $rawDir = "d:\Projects\CloudMark\runs\$RunId\raw"
        if (-not (Test-Path $rawDir)) {
            New-Item -ItemType Directory -Force -Path $rawDir | Out-Null
        }

        $rawOutputFile = "$rawDir\${TestId}_raw.log"
        Write-Host "Executing $ScriptPath on $HostIp for Test $TestId..."
        Write-Host "Raw output will be logged to: $rawOutputFile"

        $sshArgs = @(
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", "ConnectTimeout=15",
            "root@$HostIp",
            "bash -s"
        )
        if (Test-Path $SshKeyPath) {
            $sshArgs = @("-i", $SshKeyPath) + $sshArgs
        }

        $script = (Get-Content $ScriptPath -Raw) -replace "\r\n", "`n"
        $script | & ssh.exe @sshArgs 2>&1 | Tee-Object -FilePath $rawOutputFile
        Write-Host "`nTest $TestId execution finished. Log preserved at $rawOutputFile."
    }
}
