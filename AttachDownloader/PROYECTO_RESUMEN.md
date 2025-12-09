# 📋 Resumen del Proyecto: AttachDownloader

## ¿Qué se creó?

Una herramienta profesional completa en Python que **se conecta a tu cuenta de Gmail mediante OAuth 2.0** y **descarga automáticamente adjuntos** de tus correos, organizándolos inteligentemente en estructura: `<Año>/<Trimestre>/<Remitente>/`

## 📂 Estructura del Proyecto

```
hola-mundo-python/
│
├── 📄 src/main.py                    # Script principal a ejecutar
│
├── 📁 src/gmail_downloader/          # Librería principal
│   ├── __init__.py
│   ├── auth.py                       # Autenticación con Google
│   └── downloader.py                 # Lógica de descarga
│
├── 📁 config/                        # Configuración y credenciales
│   ├── credentials.json.example      # Plantilla de credenciales
│   └── credentials.json              # ⚠️ AGREGAR MANUALMENTE
│
├── 📁 downloads/                     # Carpeta de descargas (se crea automáticamente)
│
├── 📁 tests/                         # Tests unitarios
│   └── test_gmail_downloader.py
│
├── 📄 requirements.txt               # Dependencias Python
├── 📄 setup.sh                       # Script de configuración automática
├── 📄 ejemplos.py                    # Ejemplos de uso avanzado
├── 📄 README_GMAIL.md                # Documentación completa
├── 📄 GUIA_RAPIDA.md                 # Guía rápida (5 min)
├── 📄 PROYECTO_RESUMEN.md            # Este archivo
└── 📄 .gitignore                     # Archivos ignorados por Git
```

## 🎯 Características

✅ **Autenticación OAuth 2.0**: Segura y estándar de Google
✅ **Descarga completa**: Todos los adjuntos de todos los correos
✅ **Organización**: Archivos organizados por remitente
✅ **Sanitización**: Nombres de archivo seguros y válidos
✅ **Estadísticas**: Resumen de lo descargado
✅ **Caché automático**: Reutiliza tokens sin reautenticación
✅ **Manejo de errores**: Robusto y detallado
✅ **Documentación**: Completa y con ejemplos

## ⚙️ Dependencias Instaladas

```
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.100.0
python-dotenv>=1.0.0
```

## 🚀 Pasos para Empezar

### 1️⃣ Configuración Inicial (5 minutos)

```bash
cd hola-mundo-python
chmod +x setup.sh
./setup.sh
```

### 2️⃣ Configurar Credenciales de Google (Obligatorio)

1. Ve a: https://console.cloud.google.com/
2. Crea nuevo proyecto
3. Habilita **Gmail API**
4. Crea credenciales: **OAuth 2.0** → **Aplicación de escritorio**
5. Descarga el JSON y guarda como: `config/credentials.json`

### 3️⃣ Primera Ejecución

```bash
source venv/bin/activate
python src/main.py
```

- Se abrirá el navegador automáticamente
- Inicia sesión con tu cuenta de Google
- Autoriza el acceso
- ¡Los adjuntos se descargarán automáticamente!

### 4️⃣ Próximas Ejecuciones

Solo ejecuta:
```bash
python src/main.py
```

El programa reutilizará las credenciales guardadas automáticamente.

## 📥 Cómo se Descargan los Archivos

Los archivos se organizan automáticamente en una **estructura cronológica y jerárquica** (Año/Trimestre/Remitente):

```
downloads/
├── 2025/
│   ├── T1/  (Enero - Marzo)
│   │   └── usuario1@gmail.com/
│   │       ├── factura_001.pdf
│   │       ├── invoice_002.pdf
│   │       └── factura_003.pdf
│   ├── T2/  (Abril - Junio)
│   │   ├── usuario1@gmail.com/
│   │   │   ├── factura_q2_001.pdf
│   │   │   └── invoice_q2_002.pdf
│   │   └── usuario2@gmail.com/
│   │       └── factura_cliente.pdf
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

### Ventajas de Esta Estructura

✅ **Cronológica**: Documentos por año y trimestre  
✅ **Identificación**: Sabe quién envió cada archivo  
✅ **Búsqueda rápida**: Por período + remitente  
✅ **Auditoría**: Seguimiento de documentación  
✅ **Gestión**: Backup o limpieza por trimestre  
✅ **Escalable**: Histórico de múltiples años

### Filtrado Automático

Solo descarga PDFs con:
- ✅ Contienen: "factura" o "invoice"
- ❌ No contienen: "proforma"

## 📊 Output del Programa

```
==================================================
🚀 Gmail Attachment Downloader
==================================================

📝 Autenticando con Gmail API...
✅ Autenticación exitosa

📥 Iniciando descarga de adjuntos...
📧 Total de correos encontrados: 245
✅ Descargado: documento.pdf -> /ruta/al/archivo
✅ Descargado: imagen.jpg -> /ruta/al/archivo
...

==================================================
📊 Estadísticas de descarga:
==================================================
Total de correos: 245
Correos con adjuntos: 87
Archivos descargados: 156
==================================================
✅ ¡Descarga completada!
```

## 🔐 Seguridad

🛡️ **OAuth 2.0**: Protocolo estándar de Google
🔒 **Tokens locales**: Se guardan en `config/token.pickle`
✅ **Solo lectura**: No puede modificar ni eliminar correos
🚫 **Archivo .gitignore**: Protege credenciales de subirse a Git
🔄 **Renovación automática**: Los tokens se actualizan automáticamente

## 📚 Archivos Importantes para Entender

1. **src/main.py**: Punto de entrada, flujo principal
2. **src/gmail_downloader/auth.py**: Cómo autenticar con Google
3. **src/gmail_downloader/downloader.py**: Lógica de descarga
4. **README_GMAIL.md**: Documentación completa (Recomendado leer)
5. **GUIA_RAPIDA.md**: Solución de problemas

## ❓ Preguntas Frecuentes

**P: ¿Es seguro?**
R: Sí. Usa OAuth 2.0 estándar. Las credenciales se guardan localmente.

**P: ¿Modifica mis correos?**
R: No. Solo tiene permisos de lectura.

**P: ¿Cuánto tarda?**
R: Depende de tus correos. Primera vez puede tardar minutos.

**P: ¿Puedo ejecutarlo varias veces?**
R: Sí, es completamente seguro.

**P: ¿Qué pasa si se interrumpe?**
R: Solo ejecuta de nuevo. No descargará duplicados.

## 🛠️ Personalización

### Cambiar carpeta de descargas

En `src/main.py`:
```python
downloader = GmailAttachmentDownloader(
    credentials, 
    download_folder="mi_carpeta"  # 👈 Cambiar aquí
)
```

### Ver solo estadísticas

```python
stats = downloader.download_all_attachments()
print(stats)
# {'total_emails': 245, 'emails_with_attachments': 87, 'files_downloaded': 156}
```

## 📞 Soporte

1. Consulta **GUIA_RAPIDA.md** para problemas comunes
2. Lee **README_GMAIL.md** para documentación detallada
3. Revisa los **ejemplos.py** para casos de uso

## 🎓 Conceptos Aprendidos

- ✅ Autenticación OAuth 2.0 con Google
- ✅ Uso de APIs de terceros
- ✅ Manejo de excepciones
- ✅ Organización modular de código
- ✅ Interacción con APIs REST
- ✅ Trabajo con credenciales y tokens
- ✅ Sanitización de nombres de archivo
- ✅ Estadísticas y análisis

## 📝 Licencia

MIT License - Puedes usar este código libremente

---

**Creado**: 20 de noviembre de 2025
**Versión**: 1.0.0
**Autor**: GitHub Copilot

**¡Listo para usar! 🚀**
