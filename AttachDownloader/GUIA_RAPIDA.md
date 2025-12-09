# 🚀 Guía Rápida - AttachDownloader

## Instalación Rápida (5 minutos)

```bash
# 1. Navega al directorio
cd hola-mundo-python

# 2. Ejecuta el script de configuración
chmod +x setup.sh
./setup.sh

# 3. Configura credenciales (ver paso 4 abajo)

# 4. Ejecuta el programa
python src/main.py
```

## Configuración de Google Cloud (Paso Importante)

### 1. Crear Proyecto en Google Cloud Console

```
https://console.cloud.google.com/ → Nuevo Proyecto
```

### 2. Habilitar Gmail API

1. En la barra de búsqueda: "Gmail API"
2. Haz clic en "Habilitar"

### 3. Crear Credenciales OAuth

1. Menú lateral → "Credenciales"
2. "Crear credenciales" → "ID de cliente OAuth"
3. Tipo: "Aplicación de escritorio"
4. Descarga el JSON
5. **Guarda como**: `config/credentials.json`

### 4. Primera ejecución

```bash
source venv/bin/activate
python src/main.py
```

- Se abrirá el navegador automáticamente
- Inicia sesión con tu cuenta de Google
- Autoriza el acceso
- ¡Listo! Los adjuntos se descargarán

## Estructura del Proyecto

```
hola-mundo-python/
├── src/
│   ├── main.py                    # 🎯 Script principal
│   └── gmail_downloader/
│       ├── __init__.py
│       ├── auth.py                # Autenticación
│       └── downloader.py           # Descarga con filtrado
├── config/
│   ├── credentials.json.example    # Plantilla
│   └── credentials.json            # ⚠️ NO compartir
├── downloads/                      # 📥 Archivos descargados
│   ├── 2025/                       # Organizados por año
│   │   ├── T1/                     # T1, T2, T3, T4
│   │   │   └── usuario@gmail.com/  # Por remitente
│   │   ├── T2/
│   │   ├── T3/
│   │   └── T4/
│   └── 2024/
│       └── T4/
├── tests/                          # ✓ Tests unitarios
├── requirements.txt                # Dependencias
├── setup.sh                        # Script de configuración
└── README_GMAIL.md                 # Documentación completa
```

### Estructura de Descargas (Año/Trimestre/Remitente)

Los archivos se descargan automáticamente organizados cronológicamente:

```
downloads/
├── 2025/
│   ├── T1/  (Enero - Marzo)
│   │   └── usuario1@gmail.com/
│   │       ├── factura_001.pdf
│   │       ├── invoice_002.pdf
│   │       └── factura_003.pdf
│   ├── T2/  (Abril - Junio)
│   │   └── usuario1@gmail.com/
│   │       ├── factura_q2_001.pdf
│   │       └── invoice_q2_002.pdf
│   ├── T3/  (Julio - Septiembre)
│   │   └── usuario1@gmail.com/
│   │       └── factura_q3_001.pdf
│   └── T4/  (Octubre - Diciembre)
│       └── usuario2@gmail.com/
│           ├── factura_final.pdf
│           └── invoice_anual.pdf
└── 2024/
    └── T4/
        └── usuario1@gmail.com/
            └── factura_2024.pdf
```

**Ventajas:**
- ✅ Organización cronológica (año/trimestre)
- ✅ Identificación del remitente
- ✅ Búsqueda rápida por período
- ✅ Ideal para auditoría y cumplimiento

## Características Principales

✅ **OAuth 2.0**: Autenticación segura con Google
✅ **Descarga Completa**: Todos los adjuntos de todos los correos
✅ **Organización**: Archivos organizados por remitente
✅ **Sanitización**: Nombres de archivo seguros
✅ **Estadísticas**: Resumen de descargas
✅ **Caché de Credenciales**: Reutiliza tokens automáticamente

## Solución de Problemas

### ❌ "Archivo credentials.json no existe"

```bash
# Descárgalo desde Google Cloud Console y guarda como:
config/credentials.json
```

### ❌ "Acceso denegado"

```bash
# Elimina el token anterior y reautentica
rm config/token.pickle
python src/main.py
```

### ❌ No descarga nada

1. Verifica que tus correos tengan adjuntos
2. Revisa que Gmail API esté habilitada en Google Cloud
3. Comprueba los logs de error en la consola

## Uso Avanzado

### Modificar carpeta de descargas

En `src/main.py`, línea con `GmailAttachmentDownloader`:

```python
downloader = GmailAttachmentDownloader(
    credentials, 
    download_folder="mi_carpeta_personalizada"  # 👈 Cambiar aquí
)
```

### Ver estadísticas detalladas

```python
stats = downloader.download_all_attachments()
print(stats)
# {'total_emails': 123, 'emails_with_attachments': 45, 'files_downloaded': 87}
```

## Seguridad y Privacidad

🔐 **Credenciales locales**: Se guardan en `config/token.pickle`
🔒 **Protección**: El archivo está en `.gitignore`, nunca se sube a Git
🛡️ **Permisos**: Solo acceso de lectura a Gmail (no se modifica nada)
✅ **Actualización automática**: Los tokens se renuevan automáticamente

## Preguntas Frecuentes

**P: ¿Es seguro?**
R: Sí, usa OAuth 2.0 estándar de Google. Las credenciales se guardan localmente.

**P: ¿Modifica mis correos?**
R: No, solo tiene permiso de lectura. No puede eliminar ni modificar correos.

**P: ¿Cuánto tarda la descarga?**
R: Depende de la cantidad de correos. La primera vez puede tardar más.

**P: ¿Puedo ejecutarlo regularmente?**
R: Sí, es perfectamente seguro ejecutarlo múltiples veces.

**P: ¿Qué pasa si se interrumpe?**
R: Puedes ejecutarlo de nuevo. No descargará los mismos archivos dos veces.

## Contacto y Soporte

Para problemas o sugerencias, consulta la documentación completa en `README_GMAIL.md`

---

**Última actualización**: 2025-11-20
**Versión**: 1.0.0
