$ErrorActionPreference = 'Stop'

$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$installerPath = Join-Path $toolsDir 'multigit-install.exe'

$packageArgs = @{
	packageName    = $env:ChocolateyPackageName
	fileType       = 'exe'
	file           = $installerPath
	softwareName   = 'Multigit OpenSource*'
	silentArgs     = '/VERYSILENT /NORESTART /SUPPRESSMSGBOXES /CLOSEAPPLICATIONS'
	validExitCodes = @(0, 3010, 1641)
}

Install-ChocolateyInstallPackage @packageArgs

