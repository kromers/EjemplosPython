# 🚀 Gmail Attachment Downloader

**Un programa en Python que descarga automáticamente todos los adjuntos de tus correos de Gmail.**

> Este proyecto es mucho más ambicioso que un "Hola Mundo" - es una aplicación completa que se conecta a Gmail mediante OAuth 2.0 y descarga de forma inteligente todos tus archivos adjuntos.

## ✨ Características

- ✅ **Autenticación OAuth 2.0** segura con Google
- ✅ **Descarga automática** de TODOS los adjuntos
- ✅ **Organización inteligente** de archivos por remitente
- ✅ **Sanitización** de nombres de archivo
- ✅ **Estadísticas detalladas** de descarga
- ✅ **Caché automático** de credenciales
- ✅ **Manejo robusto** de errores
- ✅ **Documentación exhaustiva** (6 archivos)

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

Los archivos se organizan automáticamente por remitente:

```
downloads/
├── usuario1@gmail.com/
│   ├── documento.pdf
│   ├── imagen.jpg
│   └── reporte.xlsx
├── usuario2@gmail.com/
│   ├── presentacion.pptx
│   └── datos.csv
└── usuario3@gmail.com/
    └── archivo.zip
```

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