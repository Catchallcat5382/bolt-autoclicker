$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$BuildRoot = Join-Path $Root "build_out"
$Dist = Join-Path $BuildRoot "dist"
$Work = Join-Path $BuildRoot "build"
$Icon = Join-Path $Root "assets\bolt_autoclicker.ico"
$Assets = Join-Path $Root "assets"
$BundledPython = "C:\Users\ilans\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$PythonExe = "python"

try {
    & $PythonExe --version | Out-Null
} catch {
    if (Test-Path $BundledPython) {
        $PythonExe = $BundledPython
    } else {
        throw "Python was not found on PATH."
    }
}

if (Test-Path $BuildRoot) {
    Remove-Item -LiteralPath $BuildRoot -Recurse -Force
}

& $PythonExe (Join-Path $Root "make_icon.py")

& $PythonExe -m PyInstaller `
    --noconfirm `
    --clean `
    --noupx `
    --onefile `
    --windowed `
    --name BoltAutoClicker `
    --icon $Icon `
    --add-data "$Assets;assets" `
    --distpath $Dist `
    --workpath $Work `
    --specpath $BuildRoot `
    (Join-Path $Root "bolt_autoclicker.py")

Write-Host "One-file build complete: $(Join-Path $Dist 'BoltAutoClicker.exe')"
