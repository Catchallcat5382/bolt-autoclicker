$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Dist = $Root
$Work = Join-Path $Root "build"
$AssetIcon = Join-Path $Root "assets\bolt_autoclicker.ico"
$Extra = Join-Path $Root "extra"
$ExtraIcon = Join-Path $Extra "bolt_autoclicker.ico"
$Icon = if (Test-Path $ExtraIcon) { $ExtraIcon } else { $AssetIcon }
$Assets = Join-Path $Root "assets"
$Source = Join-Path $Root "bolt_autoclicker.py"
$NewExe = Join-Path $Root "BoltAutoClicker_new.exe"

Write-Host "Using icon: $Icon"

if (Test-Path $Work) {
    Remove-Item -LiteralPath $Work -Recurse -Force
}

if (Test-Path $NewExe) {
    Remove-Item -LiteralPath $NewExe -Force
}

$PythonExe = "python"
try {
    & $PythonExe --version | Out-Null
} catch {
    $BundledPython = "C:\Users\ilans\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    if (Test-Path $BundledPython) {
        $PythonExe = $BundledPython
    } else {
        throw "Python was not found on PATH."
    }
}

& $PythonExe (Join-Path $Root "prepare_assets.py")
$Icon = if (Test-Path $ExtraIcon) { $ExtraIcon } else { $AssetIcon }

$AddDataArgs = @("--add-data", "$Assets;assets")
if (Test-Path $Extra) {
    $AddDataArgs += @("--add-data", "$Extra;extra")
}

& $PythonExe -m PyInstaller `
    --noconfirm `
    --clean `
    --noupx `
    --onefile `
    --windowed `
    --name BoltAutoClicker_new `
    --icon $Icon `
    @AddDataArgs `
    --distpath $Dist `
    --workpath $Work `
    --specpath $Root `
    $Source

if (!(Test-Path $NewExe)) {
    throw "Build failed. Missing output: $NewExe"
}

Write-Host "One-file build complete: $NewExe"
