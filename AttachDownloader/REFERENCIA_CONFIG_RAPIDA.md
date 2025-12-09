# ⚡ Referencia Rápida - Configuración de AttachDownloader

## 🎯 Lo Más Importante

**Archivo de configuración**: `config/config.cfg`

Todos los cambios en el comportamiento de AttachDownloader se hacen editando este archivo, **sin tocar el código**.

---

## 📋 Cambios de Configuración Comunes

### 1️⃣ Cambiar Carpeta de Descargas
```ini
[DOWNLOADS]
download_folder = /Users/usuario/Mis Documentos/Facturas
```

### 2️⃣ Permitir Solo PDFs con "factura"
```ini
[FILTERS]
allowed_extensions = pdf
white_list = factura
black_list = proforma
```

### 3️⃣ Procesar Solo Ciertos Remitentes
```ini
[SENDERS]
whitelist_senders = facturas@empresa.com, contabilidad@empresa.com
```

### 4️⃣ Excluir Correos Automáticos
```ini
[SENDERS]
blacklist_senders = noreply@, notification@, alert@, bot@
```

### 5️⃣ Permitir Múltiples Extensiones
```ini
[FILTERS]
allowed_extensions = pdf, xlsx, docx, jpg
white_list = factura, invoice, recibo
```

### 6️⃣ Descargas Históricas (Solo 2024)
```ini
[DATES]
date_from = 2024-01-01
date_to = 2024-12-31
```

### 7️⃣ Usar Dominio Como Carpeta
```ini
[SENDERS]
use_domain_only = True
```
**Resultado**: `usuario@empresa.com` → carpeta `empresa.com`

### 8️⃣ Cambiar Estructura de Carpetas
```ini
[DOWNLOADS]
folder_structure = year/trimester/sender
# Otras opciones: year/sender, trimester/sender, etc.
```

### 9️⃣ Limitar Cantidad de Correos
```ini
[GMAIL_API]
max_emails_to_process = 100
# 0 = procesar todos
```

### 🔟 Filtros Case-Sensitive
```ini
[FILTERS]
case_sensitive_filters = True
# True = "Factura" ≠ "factura"
# False = "Factura" = "factura"
```

---

## 🔧 Configuración por Defecto

```ini
[DOWNLOADS]
download_folder = ./downloads
folder_structure = year/trimester/sender

[FILTERS]
allowed_extensions = pdf
white_list = factura, invoice, receipt
black_list = proforma, draft, borrador, temporal

[SENDERS]
whitelist_senders = (vacío = todos)
blacklist_senders = noreply@, notification@

[GMAIL_API]
max_emails_to_process = 0 (todos)
```

---

## ✅ Verificar Configuración

Ejecuta esto para ver la configuración actual:

```bash
python src/main.py
```

Al iniciar, verás un resumen como este:

```
======================================================================
⚙️  CONFIGURACIÓN ACTUAL
======================================================================
Proyecto: AttachDownloader v1.0.0
Modo: production
Carpeta de descargas: /Users/.../downloads
Estructura: year/trimester/sender
Extensiones permitidas: ['pdf']
Lista blanca: ['factura', 'invoice', 'receipt']
Lista negra: ['proforma', 'draft', 'borrador', 'temporal']
======================================================================
```

---

## 📂 Estructura de Carpetas Generada

Por defecto: `downloads/<Año>/<Trimestre>/<Remitente>/archivo.pdf`

Ejemplo:
```
downloads/
├── 2025/
│   ├── T1/
│   │   ├── empresa1.com/
│   │   │   ├── factura_001.pdf
│   │   │   └── factura_002.pdf
│   │   └── empresa2.com/
│   │       └── invoice_march.pdf
│   ├── T2/
│   └── T3/
└── 2024/
    ├── T1/
    ├── T2/
    └── T3/
```

---

## 🔍 Lógica de Filtros

```
Para DESCARGAR un archivo, DEBE cumplir TODO esto:

1. ✅ Extensión permitida (allowed_extensions)
   └─ Si está vacía: todas las extensiones

2. ✅ Si white_list no está vacía:
   └─ El nombre DEBE contener ALGUNA palabra de la lista

3. ✅ Si black_list no está vacía:
   └─ El nombre NO DEBE contener NINGUNA palabra de la lista

4. ✅ Remitente no en blacklist_senders

5. ✅ Si whitelist_senders no está vacía:
   └─ Remitente DEBE estar en la lista
```

### Ejemplos

**Escenario 1**: white_list = "factura", black_list = "proforma"
- ✅ `factura_2025.pdf` → SE DESCARGA
- ❌ `proforma_2025.pdf` → NO SE DESCARGA
- ❌ `documento.pdf` → NO SE DESCARGA

**Escenario 2**: allowed_extensions = "pdf", white_list vacía, black_list = "borrador"
- ✅ `documento.pdf` → SE DESCARGA
- ✅ `factura.pdf` → SE DESCARGA
- ❌ `borrador.pdf` → NO SE DESCARGA
- ❌ `documento.xlsx` → NO SE DESCARGA

---

## 🎓 Trimestres

```
T1 = Enero, Febrero, Marzo (Q1)
T2 = Abril, Mayo, Junio (Q2)
T3 = Julio, Agosto, Septiembre (Q3)
T4 = Octubre, Noviembre, Diciembre (Q4)
```

Las carpetas se crean automáticamente basadas en la fecha del correo.

---

## 📖 Documentación Completa

Para más detalles, lee:
- `CONFIG_GUIDE.md` - Guía completa con todas las opciones
- `IMPLEMENTACION_CONFIG.md` - Resumen técnico de los cambios
- `README.md` - Descripción general del proyecto

---

## 🚀 Ejemplos Prácticos

### Caso 1: Solo Facturas 2025
```ini
[FILTERS]
allowed_extensions = pdf
white_list = factura, invoice
black_list = proforma, draft

[DATES]
date_from = 2025-01-01
date_to = 2025-12-31
```

### Caso 2: Múltiples Empresas
```ini
[SENDERS]
whitelist_senders = facturas@empresa1.com, facturas@empresa2.com, facturas@empresa3.com
use_domain_only = True
```

### Caso 3: Archivos Diversos
```ini
[FILTERS]
allowed_extensions = pdf, xlsx, docx, jpg, png
white_list = factura, invoice, recibo, comprobante
black_list = proforma, draft, borrador, temporal, cancelado
```

### Caso 4: Descargas Histórica + Nueva
```ini
[GMAIL_API]
max_emails_to_process = 500

[ADVANCED]
execution_mode = incremental
save_download_history = True
```

---

## ⚠️ Errores Comunes

| Error | Solución |
|-------|----------|
| `FileNotFoundError: config.cfg` | Verifica que `config/config.cfg` existe |
| `Invalid credentials file` | Descarga `credentials.json` de Google Cloud Console |
| No se descargan archivos | Verifica `white_list` y `black_list` |
| Estructura de carpetas incorrecta | Verifica `folder_structure` en [DOWNLOADS] |
| Descarga demasiados archivos | Aumenta restricciones en `black_list` |

---

**Última actualización**: 9 de diciembre de 2025  
**Versión**: 1.0.0
