$ErrorActionPreference = 'Stop'

function Split-UninstallCommand([string] $command) {
    if ($command -match '^"(?<file>[^"]+)"\s*(?<arguments>.*)$') {
        return @{
            File = $matches.file
            Arguments = $matches.arguments.Trim()
        }
    }

    if ($command -match '^(?<file>\S+)\s*(?<arguments>.*)$') {
        return @{
            File = $matches.file
            Arguments = $matches.arguments.Trim()
        }
    }

    throw "Unable to parse uninstall command: $command"
}

$registryKeys = Get-UninstallRegistryKey -SoftwareName 'Multigit OpenSource*'

if ($registryKeys.Count -eq 0) {
    Write-Warning 'Multigit OpenSource is not installed or has already been removed.'
    return
}

if ($registryKeys.Count -gt 1) {
    $registryKeys | ForEach-Object {
        Write-Warning "Skipping uninstall because multiple matching entries were found: $($_.DisplayName)"
    }
    return
}

$commandParts = Split-UninstallCommand $registryKeys[0].UninstallString
$silentArgs = '/VERYSILENT /NORESTART /SUPPRESSMSGBOXES'

if ($commandParts.Arguments) {
    $silentArgs = ($commandParts.Arguments + ' ' + $silentArgs).Trim()
}

$packageArgs = @{
    packageName    = $env:ChocolateyPackageName
    fileType       = 'exe'
    file           = $commandParts.File
    silentArgs     = $silentArgs
    validExitCodes = @(0, 3010, 1605, 1614, 1641)
}

Uninstall-ChocolateyPackage @packageArgs

