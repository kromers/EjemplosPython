# 📋 Guía de Configuración - AttachDownloader

## 📂 Ubicación del archivo

```
AttachDownloader/
└── config/
    └── config.cfg  ← Archivo de configuración
```

## 🔧 Secciones de Configuración

### 1. **[GENERAL]** - Información del Proyecto

| Opción | Valor | Descripción |
|--------|-------|-------------|
| `project_name` | AttachDownloader | Nombre del proyecto |
| `version` | 1.0.0 | Versión actual |
| `description` | ... | Descripción breve |
| `mode` | production | Modo: production, debug |

### 2. **[DOWNLOADS]** - Configuración de Descargas

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `download_folder` | ./downloads | Ruta donde guardar adjuntos |
| `folder_structure` | year/trimester/sender | Estructura: `<Año>/<Trimestre>/<Remitente>/` |
| `create_folders_if_not_exist` | True | Crear carpetas automáticamente |
| `max_folders_to_create` | 0 | Límite de carpetas (0 = sin límite) |

**Ejemplos de `download_folder`:**
```
Relativa:   ./downloads
Absoluta macOS: /Users/javitrapero/Downloads/AttachDownloader
Absoluta Windows: C:\Users\usuario\Downloads\AttachDownloader
Entorno: %HOME%/Downloads/facturas
```

### 3. **[GMAIL_API]** - Configuración de Gmail

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `credentials_file` | credentials.json | Nombre del archivo OAuth 2.0 |
| `token_file` | token.pickle | Archivo de token de sesión |
| `gmail_scopes` | gmail.readonly | Permisos: solo lectura recomendado |
| `max_emails_to_process` | 0 | Límite de correos (0 = todos) |
| `max_attachments_to_download` | 0 | Límite de archivos (0 = todos) |

**Ubicaciones esperadas:**
- Credenciales: `config/credentials.json`
- Token: `config/token.pickle`

### 4. **[FILTERS]** - Filtrado de Archivos

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `allowed_extensions` | pdf | Extensiones permitidas (pdf, docx, xlsx, jpg, etc.) |
| `white_list` | factura, invoice, receipt | Palabras clave para INCLUIR |
| `black_list` | proforma, draft, borrador | Palabras clave para EXCLUIR |
| `case_sensitive_filters` | False | Distinguir mayúsculas/minúsculas |

**Ejemplos:**

```
# Solo descargar PDFs con "factura" en el nombre
allowed_extensions = pdf
white_list = factura

# Descargar todo excepto PDFs con "proforma"
allowed_extensions = 
black_list = proforma

# Descargar PDFs que tengan "invoice" pero NO "draft"
allowed_extensions = pdf
white_list = invoice
black_list = draft
```

### 5. **[SENDERS]** - Filtrado por Remitente

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `whitelist_senders` | (vacío) | Solo procesar estos remitentes |
| `blacklist_senders` | noreply@, notification@ | Excluir estos remitentes |
| `use_domain_only` | False | Usar solo dominio en carpeta |

**Ejemplos:**

```
# Solo procesar facturas de empresa1.com
whitelist_senders = facturas@empresa1.com, contabilidad@empresa1.com

# Excluir correos automáticos
blacklist_senders = noreply@, notification@, alert@, no-reply@

# Usar dominio como carpeta
use_domain_only = True
# Resultado: usuario@empresa.com → carpeta "empresa.com"
```

### 6. **[DATES]** - Procesamiento de Fechas

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `date_format` | YYYY-MM-DD | Formato de fecha |
| `use_email_date` | True | Usar fecha del correo para carpeta |
| `date_from` | (vacío) | Descargar desde fecha |
| `date_to` | (vacío) | Descargar hasta fecha |

**Ejemplos:**

```
# Procesar solo correos de 2025
date_from = 2025-01-01
date_to = 2025-12-31

# Procesar solo Q1 de 2025
date_from = 2025-01-01
date_to = 2025-03-31
```

### 7. **[SANITIZATION]** - Limpieza de Nombres

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `invalid_chars` | <, >, :, ", /, \ | Caracteres a reemplazar |
| `max_filename_length` | 255 | Longitud máxima de nombre |
| `replace_spaces_with_underscores` | False | Reemplazar espacios |
| `add_timestamp_on_duplicate` | True | Agregar timestamp si existe |

**Ejemplos:**

```
# Archivo original: "factura<2025>.pdf"
# Después: "factura_2025_.pdf"

# Con timestamp duplicado
# Archivo 1: factura.pdf
# Archivo 2: factura_20251209_101530.pdf
```

### 8. **[LOGGING]** - Registros y Logs

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `log_level` | INFO | Nivel: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `log_file` | logs/attachdownloader.log | Ubicación del archivo de log |
| `console_output` | True | Mostrar logs en consola |
| `log_successful_downloads` | True | Registrar descargas exitosas |
| `log_filtered_files` | True | Registrar archivos ignorados |
| `log_errors_detailed` | True | Registrar errores detallados |

### 9. **[NOTIFICATIONS]** - Notificaciones

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `send_notification` | False | Enviar notificación al terminar |
| `notification_type` | email | Tipo: email, slack, webhook |
| `notification_recipient` | (vacío) | Destinatario o webhook URL |
| `include_statistics` | True | Incluir estadísticas |

### 10. **[ADVANCED]** - Comportamiento Avanzado

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `execution_mode` | full | full, incremental |
| `save_download_history` | True | Guardar historial |
| `history_file` | logs/download_history.json | Archivo de historial |
| `retry_attempts` | 3 | Reintentos en error |
| `retry_delay` | 5 | Espera entre reintentos (segundos) |
| `use_proxy` | False | Usar servidor proxy |
| `connection_timeout` | 30 | Timeout conexión (segundos) |

### 11. **[BACKUP]** - Backup y Seguridad

| Opción | Valor Defecto | Descripción |
|--------|---------------|-------------|
| `backup_credentials` | False | Hacer backup de credenciales |
| `backup_folder` | ./backups | Carpeta de backup |
| `delete_after_backup` | False | Eliminar originales |
| `compress_downloads` | False | Comprimir en ZIP |

---

## 💡 Ejemplos de Configuración

### Ejemplo 1: Descargar Solo Facturas

```ini
[FILTERS]
allowed_extensions = pdf
white_list = factura, invoice
black_list = proforma, draft

[DOWNLOADS]
download_folder = ./facturas
```

### Ejemplo 2: Estructura por Empresa

```ini
[DOWNLOADS]
download_folder = /Users/usuario/Documents/Empresas/Facturas

[SENDERS]
whitelist_senders = facturas@empresa1.com, contabilidad@empresa2.com
use_domain_only = True
```

### Ejemplo 3: Descargas Históricas

```ini
[DATES]
date_from = 2024-01-01
date_to = 2024-12-31

[FILTERS]
white_list = factura, invoice
black_list = proforma
```

### Ejemplo 4: Con Notificaciones

```ini
[NOTIFICATIONS]
send_notification = True
notification_type = email
notification_recipient = admin@empresa.com
include_statistics = True

[LOGGING]
log_level = INFO
console_output = True
```

---

## 🔍 Lista de Verificación

Antes de ejecutar AttachDownloader:

- [ ] ¿Existe `config/credentials.json`? (descargado de Google Cloud Console)
- [ ] ¿`download_folder` apunta a la carpeta correcta?
- [ ] ¿`white_list` y `black_list` están configurados correctamente?
- [ ] ¿`allowed_extensions` incluye los formatos deseados?
- [ ] ¿`whitelist_senders` está vacío (procesar todos) o tiene valores específicos?
- [ ] ¿`date_from` y `date_to` están correctos (si aplica)?
- [ ] ¿`log_level` es `INFO` para producción?
- [ ] ¿`max_emails_to_process` es 0 (todos) o tiene un límite?

---

## 📝 Notas Importantes

### Variables de Entorno

Puedes usar variables de entorno en rutas:
```
download_folder = %HOME%/Downloads/AttachDownloader
```

### Rutas Relativas vs Absolutas

- **Relativa**: `./downloads` → `AttachDownloader/downloads/`
- **Absoluta**: `/Users/usuario/Downloads/` → Ruta exacta

### Lógica de Filtros

```
Si WHITE_LIST está vacía:
  → Descargar TODOS los archivos (excepto BLACK_LIST)

Si WHITE_LIST tiene valores:
  → Descargar SOLO archivos que cumplan WHITE_LIST (y no estén en BLACK_LIST)

BLACK_LIST siempre excluye (independiente de WHITE_LIST)
```

### Trimestres

```
T1 = Enero, Febrero, Marzo (meses 1-3)
T2 = Abril, Mayo, Junio (meses 4-6)
T3 = Julio, Agosto, Septiembre (meses 7-9)
T4 = Octubre, Noviembre, Diciembre (meses 10-12)
```

---

**Última actualización**: 9 de diciembre de 2025  
**Versión**: 1.0.0  
**Proyecto**: AttachDownloader
