# Chocolatey packaging for Multigit

This directory contains the Chocolatey package definition for Multigit.

## Package id

The package id is `multigit`.

## Build prerequisites

1. Build the Windows executable bundle with `packaging\windows\package_exe.bat`.
2. Build the Windows installer with `packaging\windows\package_installer.bat`.

## Build the package

```powershell
python packaging\chocolatey\package_chocolatey.py
```

This command stages the Chocolatey package under `build\chocolatey\package` and, when `choco` is available in `PATH`, creates the package in `dist`.

The staged `tools` directory includes:
- `multigit-install.exe` (embedded installer)
- `LICENSE.txt` (copied from repository root)
- `VERIFICATION.txt` (from `packaging\chocolatey\tools`)

If you only want to prepare the staged content without calling Chocolatey:

```powershell
python packaging\chocolatey\package_chocolatey.py --skip-pack
```

## Local installation test

```powershell
choco install multigit --source dist
choco uninstall multigit
```

The package embeds the official Multigit installer as `tools\multigit-install.exe`, so it can also be used from a local or private Chocolatey feed.

