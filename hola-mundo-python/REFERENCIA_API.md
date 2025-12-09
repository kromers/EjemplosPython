# 📚 Referencia de Módulos y Funciones

## 📦 Módulo: `gmail_downloader.auth`

### Clase: `GmailAuthenticator`

Maneja la autenticación con Gmail API usando OAuth 2.0.

#### Atributos de clase:
- `SCOPES`: Lista de permisos requeridos (lectura de Gmail)
- `TOKEN_FILE`: Ruta del archivo de token (`config/token.pickle`)
- `CREDENTIALS_FILE`: Ruta del archivo de credenciales

#### Métodos:

**`__init__(credentials_file: str = CREDENTIALS_FILE)`**
- Inicializa el autenticador
- Args:
  - `credentials_file`: Ruta al archivo credentials.json
- Ejemplo:
  ```python
  auth = GmailAuthenticator()
  ```

**`authenticate() -> Credentials`**
- Realiza la autenticación con Gmail
- Retorna: Objeto de credenciales autenticado
- Comportamiento:
  - Si existe token válido: lo reutiliza
  - Si está expirado: lo renueva automáticamente
  - Si no existe: abre navegador para autenticar
- Ejemplo:
  ```python
  creds = auth.authenticate()
  ```

**`_authorize_new() -> None`** (privado)
- Realiza una nueva autorización interactiva
- Abre el navegador para que autorices manualmente
- Lanza excepción si credentials.json no existe

---

## 📦 Módulo: `gmail_downloader.downloader`

### Clase: `GmailAttachmentDownloader`

Descarga adjuntos de Gmail API.

#### Atributos:
- `service`: Cliente de Gmail API
- `download_folder`: Ruta de la carpeta de descargas
- `stats`: Diccionario con estadísticas

#### Métodos:

**`__init__(credentials: Credentials, download_folder: str = "downloads")`**
- Inicializa el descargador
- Args:
  - `credentials`: Credenciales de Gmail API
  - `download_folder`: Carpeta raíz donde guardar archivos (defecto: "downloads")
- Los archivos se organizan en: `downloads/<Año>/<Trimestre>/<Remitente>/`
- Ejemplo:
  ```python
  downloader = GmailAttachmentDownloader(creds, "documentos")
  ```
- Estructura de carpetas resultante:
  ```
  documentos/
  ├── 2025/
  │   ├── T1/
  │   │   └── usuario1@gmail.com/
  │   │       ├── factura_001.pdf
  │   │       └── invoice_002.pdf
  │   └── T2/
  │       └── usuario2@gmail.com/
  │           └── factura_cliente.pdf
  └── 2024/
      └── T4/
          └── usuario1@gmail.com/
              └── factura_anual.pdf
  ```

**`download_all_attachments() -> dict`**
- Descarga todos los adjuntos de todos los correos
- Retorna: Diccionario con estadísticas
- Estructura del retorno:
  ```python
  {
      'total_emails': 245,
      'emails_with_attachments': 87,
      'files_downloaded': 156
  }
  ```
- Ejemplo:
  ```python
  stats = downloader.download_all_attachments()
  print(f"Descargados: {stats['files_downloaded']} archivos")
  ```

**`_get_all_messages() -> List[str]`** (privado)
- Obtiene IDs de todos los mensajes
- Retorna: Lista de IDs de mensajes
- Maneja paginación automáticamente

**`_download_message_attachments(msg_id: str) -> None`** (privado)
- Descarga adjuntos de un mensaje específico
- Extrae: asunto, remitente, fecha del correo
- Filtra PDFs con palabras clave
- Args:
  - `msg_id`: ID del mensaje

**`_download_attachment(part, msg_id, subject, sender, email_date) -> None`** (privado)
- Descarga un adjunto específico
- Filtra: solo PDF con "factura" o "invoice" (sin "proforma")
- Crea estructura: `<Año>/<Trimestre>/<Remitente>/`
- Sanitiza nombres de archivo
- Args:
  - `part`: Parte del mensaje con adjunto
  - `msg_id`: ID del mensaje
  - `subject`: Asunto del correo
  - `sender`: Remitente del correo
  - `email_date`: Fecha del correo (datetime)

**`_get_trimester(month: int) -> str`** (estático) ✨ NUEVO
- Calcula el trimestre basado en el mes
- Args:
  - `month`: Número del mes (1-12)
- Retorna: Trimestre (T1, T2, T3, T4)
- Mapping:
  - T1: Enero, Febrero, Marzo (meses 1-3)
  - T2: Abril, Mayo, Junio (meses 4-6)
  - T3: Julio, Agosto, Septiembre (meses 7-9)
  - T4: Octubre, Noviembre, Diciembre (meses 10-12)
- Ejemplo:
  ```python
  trimester = GmailAttachmentDownloader._get_trimester(3)  # T1
  trimester = GmailAttachmentDownloader._get_trimester(6)  # T2
  ```

**`_parse_email_date(date_str: str) -> datetime`** (estático) ✨ NUEVO
- Parsea la fecha del correo en formato RFC 2822
- Args:
  - `date_str`: Fecha en formato RFC 2822 (ej: "Mon, 15 Dec 2024 10:30:45 +0000")
- Retorna: Objeto datetime con la fecha
- Ejemplo:
  ```python
  date = GmailAttachmentDownloader._parse_email_date("Mon, 15 Dec 2024 10:30:45 +0000")
  # Resultado: datetime(2024, 12, 15, 10, 30, 45)
  ```

**`_sanitize_filename(filename: str) -> str`** (estático)
- Elimina caracteres inválidos de nombres
- Reemplaza: `< > : " / \ | ? *`
- Retorna: Nombre sanitizado
- Ejemplo:
  ```python
  safe_name = GmailAttachmentDownloader._sanitize_filename('documento"mal".pdf')
  # Resultado: 'documento_mal_.pdf'
  ```

---

## 🎯 Script Principal: `src/main.py`

### Función: `main()`

Orquesta el flujo completo de la aplicación.

**Pasos:**
1. Autentica con Gmail API
2. Crea instancia del descargador
3. Descarga todos los adjuntos
4. Muestra estadísticas
5. Maneja errores

**Errores que captura:**
- `FileNotFoundError`: Si falta credentials.json
- Excepciones generales: Cualquier otro error

**Ejemplo de uso:**
```bash
python src/main.py
```

---

## 📊 Estructura de Estadísticas

El diccionario `stats` retornado contiene:

```python
{
    'total_emails': int,              # Total de correos procesados
    'emails_with_attachments': int,   # Correos que tienen adjuntos
    'files_downloaded': int           # Cantidad de archivos descargados
}
```

---

## 🔄 Flujo de Ejecución (Con Estructura Año/Trimestre/Remitente)

```
main.py
    ↓
1. GmailAuthenticator.authenticate()
    ↓
    ├─ Verificar token.pickle
    ├─ Si existe y válido: usar
    ├─ Si expirado: renovar
    └─ Si no existe: autorizar nuevo
    ↓
2. GmailAttachmentDownloader.__init__()
    ↓
    └─ Crear carpeta raíz: downloads/
    ↓
3. downloader.download_all_attachments()
    ↓
    ├─ _get_all_messages()
    │   └─ Obtener IDs de todos los correos
    │
    ├─ Por cada mensaje:
    │   └─ _download_message_attachments()
    │       ├─ Obtener: asunto, remitente, fecha
    │       ├─ _parse_email_date() → Extraer fecha
    │       └─ Por cada adjunto (si es PDF):
    │           └─ _download_attachment()
    │               ├─ Filtrar: "factura" o "invoice" (sin "proforma")
    │               ├─ _get_trimester() → T1/T2/T3/T4 según mes
    │               ├─ Crear ruta: downloads/<Año>/<Trimestre>/<Remitente>/
    │               ├─ _sanitize_filename() → nombres seguros
    │               └─ Guardar: downloads/2025/T1/usuario1@gmail.com/factura.pdf
    │
    └─ Retornar stats

Estructura final de carpetas:
    downloads/
    ├── 2025/
    │   ├── T1/
    │   │   ├── usuario1@gmail.com/
    │   │   │   ├── factura_001.pdf
    │   │   │   └── invoice_002.pdf
    │   │   └── usuario2@gmail.com/
    │   │       └── factura_cliente.pdf
    │   ├── T2/
    │   │   └── usuario1@gmail.com/
    │   │       ├── factura_q2_001.pdf
    │   │       └── invoice_q2_002.pdf
    │   ├── T3/
    │   │   └── usuario1@gmail.com/
    │   │       └── factura_q3_001.pdf
    │   └── T4/
    │       └── usuario2@gmail.com/
    │           └── factura_final.pdf
    └── 2024/
        └── T4/
            └── usuario1@gmail.com/
                └── factura_2024.pdf
    ↓
4. Mostrar resultados con estadísticas
```

---

## 🛡️ Manejo de Errores

| Error | Ubicación | Acción |
|-------|-----------|--------|
| `FileNotFoundError` | `GmailAuthenticator` | Mensaje con instrucciones de Google Cloud |
| `RefreshError` | `GmailAuthenticator` | Reautenticar |
| `Exception` general | Todos los métodos | Registrar y continuar |

---

## 🔑 Constantes Importantes

| Constante | Valor | Propósito |
|-----------|-------|----------|
| `SCOPES` | `["...gmail.readonly"]` | Permisos de API |
| `TOKEN_FILE` | `"config/token.pickle"` | Almacenamiento de token |
| `CREDENTIALS_FILE` | `"config/credentials.json"` | Credenciales OAuth |

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Uso básico
```python
from gmail_downloader.auth import GmailAuthenticator
from gmail_downloader.downloader import GmailAttachmentDownloader

# Autenticar
auth = GmailAuthenticator()
creds = auth.authenticate()

# Descargar
downloader = GmailAttachmentDownloader(creds)
stats = downloader.download_all_attachments()

print(f"✅ {stats['files_downloaded']} archivos descargados")
```

### Ejemplo 2: Carpeta personalizada
```python
downloader = GmailAttachmentDownloader(
    creds, 
    download_folder="mis_documentos"
)
stats = downloader.download_all_attachments()
```

### Ejemplo 3: Análisis de resultados
```python
stats = downloader.download_all_attachments()

if stats['files_downloaded'] > 0:
    avg = stats['files_downloaded'] / stats['emails_with_attachments']
    print(f"Promedio: {avg:.1f} archivos por correo")
```

---

## 🧪 Testing

Ver `tests/test_gmail_downloader.py` para:
- Tests de sanitización de nombres
- Tests de creación de carpetas
- Tests de autenticación

```bash
python -m pytest tests/
```

---

## 📖 Documentación Relacionada

- **GUIA_RAPIDA.md**: Guía de instalación rápida
- **README_GMAIL.md**: Documentación completa
- **PROYECTO_RESUMEN.md**: Overview del proyecto
- **ejemplos.py**: Ejemplos de uso avanzado

---

**Última actualización**: 2025-11-20
**Versión**: 1.0.0
