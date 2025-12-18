AttachDownloader - Paquete de distribución

Contenido del ZIP:
- AttachDownloader/AttachDownloader.exe (ejecutable principal)
- AttachDownloader/_internal/ (archivos necesarios generados por PyInstaller)
- config/config.cfg (archivo de configuración)
- config/credentials.json.example (plantilla de credenciales OAuth, NO la real)
- BUILD.md (instrucciones de construcción)
- GUIA_RAPIDA.md (guía rápida de uso)
- INSTALL.md (instrucciones de instalación y ejecución en otro PC)

Instrucciones de uso:
1. Extrae el ZIP en un equipo Windows.
2. Copia el archivo de credenciales `credentials.json` (descargado desde Google Cloud Console) a la carpeta `config/`.
3. Edita `config/config.cfg` según tus preferencias.
4. Ejecuta `AttachDownloader\AttachDownloader.exe`.

Notas:
- No incluyas `credentials.json` real en repositorios públicos ni al compartir el ZIP de forma insegura.
- Para reducir problemas, ejecuta el exe en un Windows con las librerías C runtime estándar disponibles. Si tu exe falla con librerías faltantes, instala Visual C++ Redistributable para Visual Studio 2015-2022.
