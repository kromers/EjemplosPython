# Instrucciones para construir el ejecutable (PyInstaller)

Este proyecto incluye un helper para generar un ejecutable independiente con PyInstaller.

Pasos rápidos (PowerShell, desde la raíz del repo):

1. Abrir PowerShell y situarse en la raíz del repositorio
2. Ejecutar:

   ```powershell
   .\scripts\build_exe.ps1
   ```

Notas importantes:

- El ejecutable se generará en `dist\AttachDownloader\AttachDownloader.exe`.
- **Los archivos de configuración y ayuda NO se incluyen** en el ejecutable (ej: `config/config.cfg`, `config/credentials.json`). Debes distribuirlos junto al exe o usar rutas externas.
- Si faltan dependencias, el script intentará instalar `pyinstaller` en el entorno activo.
- Si tu aplicación depende de módulos dinámicos adicionales, añade `--hidden-import=` en el script `build_exe.ps1` o actualiza `AttachDownloader.spec`.

Depuración:

- Ejecuta `pyinstaller` directamente con más opciones para depurar la inclusión de dependencias dinámicas.
- Revisa `build\` para logs detallados si la compilación falla.

Si quieres, puedo ejecutar una compilación de prueba en tu entorno (si me das permiso para instalar `pyinstaller`).