# 🚀 AttachDownloader

**Un programa profesional en Python que descarga y organiza automáticamente adjuntos de Gmail con estructura inteligente por año, trimestre y remitente.**

> AttachDownloader es una herramienta empresarial que se conecta a Gmail mediante OAuth 2.0 y gestiona de forma inteligente todos tus archivos adjuntos, especialmente facturas y documentos comerciales.

## ✨ Características

- ✅ **Autenticación OAuth 2.0** segura con Google
- ✅ **Descarga automática** de todos los adjuntos
- ✅ **Organización inteligente** por año, trimestre y remitente
- ✅ **Filtrado de documentos** (facturas, invoices, etc.)
- ✅ **Sanitización** de nombres de archivo
- ✅ **Estadísticas detalladas** de descarga
- ✅ **Caché automático** de credenciales
- ✅ **Manejo robusto** de errores
- ✅ **Documentación exhaustiva**

## 📚 Documentación

| Documento | Contenido | Tiempo |
|-----------|----------|--------|
| **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** ⭐ | Empeza aquí - Instalación rápida | 5 min |
| **[README_GMAIL.md](README_GMAIL.md)** | Documentación completa del proyecto | 15 min |
| **[PROYECTO_RESUMEN.md](PROYECTO_RESUMEN.md)** | Overview y características | 10 min |
| **[REFERENCIA_API.md](REFERENCIA_API.md)** | Referencia de módulos y funciones | - |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Solución de problemas | - |

## 🚀 Inicio Rápido (3 pasos)

### 1️⃣ Obtén credenciales de Google

1. Ve a https://console.cloud.google.com/
2. Crea un nuevo proyecto
3. Habilita **Gmail API**
4. Crea credenciales: **OAuth 2.0 → Aplicación de escritorio**
5. Descarga el JSON y guarda como `config/credentials.json`

### 2️⃣ Instala dependencias

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar librerías
pip install -r requirements.txt
```

### 3️⃣ Ejecuta el programa

```bash
python src/main.py
```

La primera vez se abrirá automáticamente el navegador para autorizar. ¡Luego descargará todos tus adjuntos!

## 📂 Estructura del Proyecto

```
hola-mundo-python/
├── src/
│   ├── main.py                           # Script principal
│   └── gmail_downloader/
│       ├── auth.py                       # Autenticación OAuth 2.0
│       └── downloader.py                 # Lógica de descarga
├── config/
│   ├── credentials.json                  # ⚠️ AGREGAR (NO COMPARTIR)
│   └── credentials.json.example          # Plantilla
├── downloads/                            # Archivos descargados aquí
├── tests/                                # Tests unitarios
├── GUIA_RAPIDA.md                        # ⭐ Empeza aquí
├── README_GMAIL.md                       # Documentación completa
├── requirements.txt                      # Dependencias
└── .gitignore                            # Archivos ignorados
```

## 💻 Requisitos

- Python 3.8+
- Cuenta de Google
- Acceso a Google Cloud Console

## 🔧 Herramientas Disponibles

```bash
# Ver guía interactiva
python INICIO_RAPIDO.py

# Instalar automáticamente
python instalar.py

# Ver ejemplos de uso
python ejemplos.py

# Ejecutar tests
python -m pytest tests/
```

## 📊 Output del Programa

```
==================================================
🚀 Gmail Attachment Downloader
==================================================

📝 Autenticando con Gmail API...
✅ Autenticación exitosa

📥 Iniciando descarga de adjuntos...
📧 Total de correos encontrados: 245
✅ Descargado: documento.pdf
✅ Descargado: imagen.jpg
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

- 🛡️ Usa OAuth 2.0 estándar de Google
- 🔒 Credenciales guardadas localmente
- ✅ Solo lectura (no modifica correos)
- 🚫 Protegido con .gitignore
- 🔄 Renovación automática de tokens

## 📥 Resultado de la Descarga

Los archivos se organizan automáticamente en una estructura **cronológica y jerárquica** (Año/Trimestre/Remitente), ideal para auditoría y gestión documental:

### Estructura Avanzada: Año/Trimestre/Remitente

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

### ¿Por Qué Esta Estructura?

- **Cronológica**: Documentos organizados por año y trimestre
- **Identifica fácilmente el origen**: Sabe quién envió cada archivo
- **Búsqueda rápida**: Encuentra documentos por período + remitente
- **Auditoría**: Seguimiento de documentación por período
- **Gestión sencilla**: Backup o eliminación por trimestre
- **Escalabilidad**: Funciona bien con histórico de años

### Filtrado Automático

Solo se descargan archivos PDF que cumplen:
- ✅ Extensión: `.pdf`
- ✅ Contienen: "factura" o "invoice"
- ✅ No contienen: "proforma"

## ❓ Preguntas Frecuentes

**P: ¿Es seguro?**
R: Sí, usa OAuth 2.0 estándar. Las credenciales se guardan localmente.

**P: ¿Modifica mis correos?**
R: No, solo tiene permisos de lectura. No puede eliminar ni cambiar nada.

**P: ¿Cuánto tarda?**
R: Depende de la cantidad de correos. La primera vez puede tardar minutos.

**P: ¿Puedo ejecutarlo varias veces?**
R: Sí, es completamente seguro. Las credenciales se cargan automáticamente.

## 📚 Aprenderás

Este proyecto enseña:
- ✅ Autenticación OAuth 2.0 con Google
- ✅ Uso de APIs de terceros
- ✅ Manejo de excepciones
- ✅ Organización modular de código
- ✅ Sanitización de datos
- ✅ Estadísticas y análisis

## 🎯 Dependencias

```
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.100.0
python-dotenv>=1.0.0
```

## 🛠️ Instalación Paso a Paso

Para instalación automática:
```bash
python instalar.py
```

Para instalación manual, lee [GUIA_RAPIDA.md](GUIA_RAPIDA.md)

## 📞 Soporte

- 📖 **Documentación**: Lee los archivos `.md` en el proyecto
- 🔧 **Problemas**: Consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 💡 **Ejemplos**: Ver `ejemplos.py`
- 🔗 **API Oficial**: https://developers.google.com/gmail/api/guides

## 📝 Licencia

MIT License - Puedes usar este código libremente

---

**Versión**: 1.0.0  
**Creado**: Noviembre 2025  
**Autor**: GitHub Copilot

### ⭐ ¿Te gustó? Dale una estrella al repositorio!

## Configuración de GIT

```powershell
git config --global user.email tu_email@ejemplo.com
git config --global user.name tu_nombre
```

## Estructura del Proyecto

```
hola-mundo-python
├── src
│   ├── main.py
│   └── __init__.py
├── tests
│   └── test_main.py
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Instrucciones para Ejecutar

1. Asegúrate de tener Python instalado en tu sistema.
2. Clona el repositorio o descarga los archivos del proyecto.
3. Navega al directorio del proyecto.
4. Ejecuta el siguiente comando para correr la aplicación:

   ```
   python src/main.py
   ```

## Pruebas

Para ejecutar las pruebas unitarias, asegúrate de tener `pytest` instalado y ejecuta:

```
pytest tests/test_main.py
```

## Dependencias

Este proyecto no tiene dependencias externas, pero puedes agregar cualquier librería necesaria en el archivo `requirements.txt`.