# 📝 Cambios en el Proyecto - downloader.py

**Fecha**: 9 de diciembre de 2025  
**Archivo modificado**: `src/gmail_downloader/downloader.py`  
**Impacto**: ALTO - Cambios en estructura de descargas y filtrado

---

## 🔄 Cambios Principales

### 1. ✨ Nueva Estructura de Carpetas

**Antes:**
```
downloads/
├── usuario1@gmail.com/
│   ├── documento.pdf
│   └── imagen.jpg
└── usuario2@gmail.com/
    └── factura.pdf
```

**Ahora:**
```
downloads/
├── 2025/
│   ├── T1/  (Enero - Marzo)
│   │   └── usuario1@gmail.com/
│   │       ├── factura_001.pdf
│   │       └── invoice_002.pdf
│   ├── T2/  (Abril - Junio)
│   │   └── usuario2@gmail.com/
│   │       └── factura_cliente.pdf
│   └── T3/  (Julio - Septiembre)
│       └── usuario1@gmail.com/
│           └── factura_q3_001.pdf
└── 2024/
    └── T4/
        └── usuario1@gmail.com/
            └── factura_2024.pdf
```

**Ventajas:**
- 📅 Organización cronológica por año y trimestre
- 🔍 Búsqueda más precisa por período
- 📊 Ideal para auditoría y cumplimiento normativo

---

### 2. 🔍 Nuevo Sistema de Filtrado

**Características nuevas:**

#### a) Filtrado por Tipo de Archivo
- ✅ Solo archivos **PDF** se descargan
- ❌ Se ignoran: DOCX, XLS, JPG, etc.

#### b) Whitelist (Palabras Clave)
Solo se descargan archivos que contengan:
- `factura`
- `invoice`

#### c) Blacklist (Palabras Excluidas)
Se rechazan archivos que contengan:
- `proforma`

**Ejemplos:**
```
✅ factura_2025_001.pdf          → Se descarga
✅ invoice_Q1_cliente.pdf         → Se descarga
✅ FACTURA_EMPRESA.pdf            → Se descarga (insensible a mayúsculas)
❌ proforma_cotizacion.pdf        → NO se descarga
❌ factura_proforma.pdf           → NO se descarga (contiene "proforma")
❌ documento_importante.docx      → NO se descarga (no es PDF)
❌ imagen_factura.jpg             → NO se descarga (no es PDF)
```

---

### 3. 🕐 Extracción de Fecha del Correo

**Nuevo método:** `_parse_email_date(date_str: str) -> datetime`

- Parsea fecha en formato RFC 2822
- Ejemplo: `"Mon, 15 Dec 2024 10:30:45 +0000"` → `datetime(2024, 12, 15)`
- Permite organización por año y trimestre

---

### 4. 📆 Cálculo de Trimestre

**Nuevo método:** `_get_trimester(month: int) -> str`

- Convierte número de mes a trimestre
- Mapping:
  - Enero-Marzo (1-3) → T1
  - Abril-Junio (4-6) → T2
  - Julio-Septiembre (7-9) → T3
  - Octubre-Diciembre (10-12) → T4

---

### 5. 📂 Estructura de Carpetas Jerárquica

**Ruta de descarga:**
```
<download_folder>/<Año>/<Trimestre>/<Remitente>/
```

**Ejemplo real:**
```
downloads/2025/T1/usuario1@gmail.com/factura_001.pdf
downloads/2025/T2/usuario2@gmail.com/factura_cliente.pdf
downloads/2024/T4/usuario1@gmail.com/factura_2024.pdf
```

---

## 📊 Cambios en Métodos

### Método: `_download_message_attachments()`

**Cambios:**
- ✨ Nuevo: Extrae fecha del correo con `_parse_email_date()`
- ✨ Nuevo: Pasa `email_date` a `_download_attachment()`
- Sin cambios en la lógica de procesamiento

**Firma anterior:**
```python
def _download_message_attachments(self, msg_id: str) -> None
```

**Firma actual:**
```python
def _download_message_attachments(self, msg_id: str) -> None
```

---

### Método: `_download_attachment()` 

**Cambios SIGNIFICATIVOS:**

**Antes:**
```python
def _download_attachment(self, part, msg_id, subject, sender):
    # Crea carpeta: downloads/remitente@email.com/
    # Descarga cualquier archivo
```

**Ahora:**
```python
def _download_attachment(self, part, msg_id, subject, sender, email_date):
    # 1. Filtra solo PDFs
    # 2. Aplica whitelist/blacklist
    # 3. Extrae año y trimestre
    # 4. Crea carpeta: downloads/<Año>/<Trimestre>/<Remitente>/
    # 5. Descarga si pasa filtros
```

**Pasos nuevos:**
1. ✅ Verifica extensión `.pdf`
2. ✅ Aplica whitelist ("factura", "invoice")
3. ✅ Aplica blacklist (no "proforma")
4. ✅ Extrae año de fecha del correo
5. ✅ Calcula trimestre con `_get_trimester()`
6. ✅ Crea estructura de carpetas
7. ✅ Descarga solo si pasa todos los filtros

---

### Métodos NUEVOS

#### `_get_trimester(month: int) -> str`
```python
@staticmethod
def _get_trimester(month: int) -> str:
    """Obtiene el trimestre basado en el mes (T1-T4)"""
```

#### `_parse_email_date(date_str: str) -> datetime`
```python
@staticmethod
def _parse_email_date(date_str: str) -> datetime:
    """Parsea fecha RFC 2822 a datetime"""
```

---

## 📋 Comparativa de Cambios

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Estructura** | `downloads/<Remitente>/` | `downloads/<Año>/<Trimestre>/<Remitente>/` |
| **Filtrado** | Todos los archivos | Solo PDF con palabras clave |
| **Métodos privados** | 4 | 6 (+2 nuevos) |
| **Parámetros** | `_download_attachment(4)` | `_download_attachment(5)` |
| **Uso de fecha** | No | Sí, para organización |
| **Whitelist** | No | Sí: "factura", "invoice" |
| **Blacklist** | No | Sí: "proforma" |

---

## 🔄 Impacto en Documentación

**Archivos actualizados:**
- ✅ `README_GMAIL.md` - Estructura de descargas
- ✅ `README.md` - Resultado de la descarga
- ✅ `PROYECTO_RESUMEN.md` - Cómo se descargan los archivos
- ✅ `GUIA_RAPIDA.md` - Estructura del proyecto
- ✅ `REFERENCIA_API.md` - Documentación completa de métodos

---

## ⚠️ Consideraciones Importantes

### 1. Compatibilidad Hacia Atrás
- ❌ **NO es compatible** con descargas anteriores
- Las carpetas ahora tienen estructura diferente
- Los archivos anteriores NO se reorganizan automáticamente

### 2. Migración de Datos
Si tenías archivos descargados con la estructura anterior:
```bash
# Estructura anterior
downloads/usuario1@gmail.com/factura.pdf

# Necesita reorganizarse manualmente a:
downloads/2025/T1/usuario1@gmail.com/factura.pdf
```

### 3. Configuración
El filtrado está **hardcodeado** en el método:
```python
white_list = ["factura", "invoice"]
black_list = ["proforma"]
```

Para cambiar los filtros, edita estos valores en `downloader.py` línea ~138

---

## 🧪 Testing Recomendado

Después de estos cambios, verifica:

1. ✅ Las carpetas se crean correctamente: `<Año>/<Trimestre>/<Remitente>/`
2. ✅ Solo se descargan PDFs
3. ✅ Se respetan whitelist y blacklist
4. ✅ Las fechas se extraen correctamente
5. ✅ Los trimestres se calculan bien
6. ✅ Los nombres de archivo se sanitizan

---

## 📚 Referencias

- Método `_parse_email_date()`: Usa `email.utils.parsedate_to_datetime`
- Método `_get_trimester()`: Mapeo estático mes→trimestre
- RFC 2822: Formato estándar de fechas de correo

---

## 🔔 Notas Finales

- Estos cambios **mejoran significativamente** la organización de archivos
- Son especialmente útiles para **auditoría y cumplimiento**
- El sistema ahora es más **robusto** y **selectivo**
- La documentación debe estar **completamente actualizada**

---

**Versión**: 1.0.2  
**Estado**: Cambios implementados y documentados  
**Próxima revisión**: Según necesidades de filtrado
