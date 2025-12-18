<#
PowerShell helper to build AttachDownloader executable with PyInstaller.
- Produces a single-file exe in the `dist` folder: dist\AttachDownloader\AttachDownloader.exe
- Does NOT bundle any files under `config/` or any help/docs files.

Usage (from repository root):
    .\scripts\build_exe.ps1

If PyInstaller not present, the script will offer to install it in the active Python environment.
#>

Write-Host "🚧 Building AttachDownloader executable..."

# Ensure we run from project root
Push-Location (Split-Path -Path $PSCommandPath -Parent) | Out-Null
Set-Location ..

# Optionally install pyinstaller if missing
try {
    pyinstaller --version > $null 2>&1
} catch {
    Write-Host "PyInstaller not found. Installing with pip..."
    python -m pip install --upgrade pyinstaller
}

# Clean previous builds
Remove-Item -Recurse -Force build,dist -ErrorAction SilentlyContinue

# Use spec if available, otherwise call pyinstaller directly
if (Test-Path .\AttachDownloader.spec) {
    Write-Host "Using AttachDownloader.spec to build (onefile will be produced)."
    pyinstaller .\AttachDownloader.spec --clean
} else {
    # Fallback: run direct command including common hidden imports (single-line for PowerShell)
    pyinstaller --clean --onefile --name AttachDownloader --hidden-import=googleapiclient.discovery --hidden-import=google.auth.transport.requests --hidden-import=google.oauth2.credentials --hidden-import=httplib2 src\main.py
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed. Revisa la salida por errores." -ForegroundColor Red
    Pop-Location
    exit $LASTEXITCODE
}

Write-Host "✅ Build finished. Ejecutable en: dist\AttachDownloader\" -ForegroundColor Green
Write-Host "⚠️ Recuerda: la carpeta config/ NO está incluida en el exe. Debes mantener archivos como config/config.cfg y config/credentials.json junto al ejecutable o en la ruta esperada." -ForegroundColor Yellow

Pop-Location
