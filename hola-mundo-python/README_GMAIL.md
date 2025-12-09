# Gmail Attachment Downloader

Programa en Python que descarga automáticamente todos los adjuntos de tus correos de Gmail.

## 🚀 Características

- ✅ Conecta con Gmail API usando OAuth 2.0
- ✅ Descarga todos los adjuntos de todos los correos
- ✅ Organiza archivos por remitente
- ✅ Sanitiza nombres de archivos
- ✅ Estadísticas de descarga
- ✅ Manejo robusto de errores

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cuenta de Google
- Acceso a Google Cloud Console

## 🔧 Instalación

### 1. Clonar/Descargar el proyecto

```bash
cd /Users/javitrapero/WorkSpace/EjemplosPython/hola-mundo-python
```

### 2. Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar credenciales de Google

#### a. Crear proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Habilita Gmail API:
   - En la barra de búsqueda, busca "Gmail API"
   - Haz clic en "Habilitar"

#### b. Crear credenciales OAuth

1. Ve a "Credenciales" en el menú lateral
2. Haz clic en "Crear credenciales" → "ID de cliente OAuth"
3. Selecciona "Aplicación de escritorio"
4. Descarga el archivo JSON
5. Guarda el archivo como `config/credentials.json`

## 🚀 Uso

```bash
python src/main.py
```

### Primera ejecución

La primera vez que ejecutes el script:
1. Se abrirá una ventana del navegador
2. Inicia sesión con tu cuenta de Google
3. Autoriza el acceso a tu cuenta de Gmail
4. Las credenciales se guardarán automáticamente

### Ejecuciones posteriores

Las credenciales se cargarán automáticamente desde `config/token.pickle`

## 📁 Estructura de Descarga

Los archivos se descargarán en la carpeta `downloads/` organizados jerárquicamente por **año**, **trimestre** y **remitente**. Esta estructura avanzada facilita:
- 📅 Organización cronológica por trimestres
- 📧 Identificación del remitente
- 🔍 Búsqueda rápida por período
- 🗂️ Acceso ordenado y coherente

### Estructura Jerárquica (Año/Trimestre/Remitente)

```
downloads/
├── 2025/
│   ├── T1/
│   │   └── usuario1@gmail.com/
│   │       ├── factura_001.pdf
│   │       ├── invoice_002.pdf
│   │       └── factura_003.pdf
│   ├── T2/
│   │   ├── usuario1@gmail.com/
│   │   │   ├── factura_q2_001.pdf
│   │   │   └── invoice_q2_002.pdf
│   │   └── usuario2@gmail.com/
│   │       └── factura_cliente.pdf
│   ├── T3/
│   │   └── usuario1@gmail.com/
│   │       └── factura_q3_001.pdf
│   └── T4/
│       └── usuario2@gmail.com/
│           ├── factura_final.pdf
│           └── invoice_anual.pdf
└── 2024/
    ├── T4/
    │   └── usuario1@gmail.com/
    │       └── factura_2024.pdf
    └── T1/
        └── usuario2@gmail.com/
            └── invoice_inicial.pdf
```

### Filtrado Inteligente

El sistema filtra automáticamente:
- ✅ **Solo PDFs**: Se descargan únicamente archivos PDF
- ✅ **Whitelist**: Contiene palabras clave: "factura", "invoice"
- ✅ **Blacklist**: Excluye archivos con: "proforma"

**Ejemplo de filtrado:**
- ✅ `factura_2025_001.pdf` → Se descarga
- ✅ `invoice_Q1_cliente.pdf` → Se descarga
- ❌ `proforma_cotizacion.pdf` → NO se descarga
- ❌ `documento.docx` → NO se descarga (no es PDF)

### Ventajas de Esta Estructura

| Ventaja | Descripción |
|---------|-------------|
| **Cronológica** | Documentos organizados por año y trimestre |
| **Claridad** | Sabe exactamente de quién es cada archivo |
| **Búsqueda rápida** | Navega por período + remitente |
| **Auditoría** | Fácil seguimiento de documentación por período |
| **Mantenimiento** | Simple hacer backup o limpiar por trimestre |
| **Escalable** | Funciona bien con histórico de años |

## 📊 Estadísticas

El programa muestra:
- Total de correos procesados
- Cantidad de correos con adjuntos
- Total de archivos descargados

## 🔐 Seguridad

- Las credenciales se almacenan localmente en `config/token.pickle`
- El archivo `config/credentials.json` está en `.gitignore`
- Nunca compartas tus credenciales
- Los tokens se actualizan automáticamente

## 🛠️ Solución de Problemas

### Error: "El archivo credentials.json no existe"

Asegúrate de haber descargado el archivo de credenciales desde Google Cloud Console y guardarlo como `config/credentials.json`

### Error: "Acceso denegado"

1. Verifica que Gmail API esté habilitada en Google Cloud Console
2. Elimina `config/token.pickle` y ejecuta de nuevo para reautenticar

### No descarga adjuntos

1. Verifica que tus correos tengan realmente adjuntos
2. Revisa los permisos en Google Cloud Console
3. Comprueba los logs de error en la consola

## 📝 Notas

- El script lee tus correos, pero no los modifica ni elimina
- La primera descarga puede tardar según la cantidad de correos
- Considera ejecutar el script regularmente para mantener los adjuntos descargados

## 📚 Referencias

- [Gmail API Documentation](https://developers.google.com/gmail/api/guides)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [Python Google Client Library](https://github.com/googleapis/google-api-python-client)

## 👤 Autor

Tu Nombre

## 📄 Licencia

MIT License
