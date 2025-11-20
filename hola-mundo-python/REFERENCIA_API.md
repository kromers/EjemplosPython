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
  - `download_folder`: Carpeta donde guardar archivos
- Ejemplo:
  ```python
  downloader = GmailAttachmentDownloader(creds, "mis_descargas")
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
- Args:
  - `msg_id`: ID del mensaje

**`_download_attachment(part, msg_id, subject, sender) -> None`** (privado)
- Descarga un adjunto específico
- Crea carpeta por remitente
- Sanitiza nombres de archivo

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

## 🔄 Flujo de Ejecución

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
    └─ Crear carpeta de descargas
    ↓
3. downloader.download_all_attachments()
    ↓
    ├─ _get_all_messages()
    │   └─ Obtener IDs de todos los correos
    │
    ├─ Por cada mensaje:
    │   └─ _download_message_attachments()
    │       └─ Por cada adjunto:
    │           └─ _download_attachment()
    │               ├─ _sanitize_filename()
    │               └─ Guardar archivo
    │
    └─ Retornar stats
    ↓
4. Mostrar resultados
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
