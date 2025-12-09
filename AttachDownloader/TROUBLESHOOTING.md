# 🔧 Guía Avanzada de Troubleshooting - AttachDownloader

## ❌ Errores Comunes y Soluciones

### 1. `ModuleNotFoundError: No module named 'google'`

**Causa**: Las dependencias no están instaladas

**Solución**:
```bash
# Asegúrate que el entorno virtual está activado
source venv/bin/activate  # macOS/Linux
# o
.\\venv\\Scripts\\activate  # Windows

# Reinstala las dependencias
pip install -r requirements.txt

# Verifica la instalación
python -c "import google; print('✅ OK')"
```

---

### 2. `FileNotFoundError: credentials.json not found`

**Causa**: El archivo de credenciales no existe o está en lugar incorrecto

**Solución**:
```bash
# 1. Descarga el archivo desde Google Cloud Console
# 2. Verifica que esté en la ubicación correcta:
ls -la config/credentials.json  # macOS/Linux
dir config\credentials.json     # Windows

# 3. Verifica el contenido (debe empezar con {"installed":)
head -c 50 config/credentials.json

# 4. Si no existe, cópialo desde otra ubicación:
cp /ruta/descarga/credentials.json config/
```

**Referencia de Google Cloud**:
1. https://console.cloud.google.com/
2. Proyecto → Credenciales
3. "Crear credenciales" → "OAuth 2.0" → "Aplicación de escritorio"
4. Descargar JSON

---

### 3. `RefreshError: ('invalid_grant', {'error_desc': 'The refresh token is invalid'})`

**Causa**: El token ha expirado y no se puede renovar

**Solución**:
```bash
# Elimina el token guardado para forzar reautenticación
rm config/token.pickle

# Ejecuta de nuevo
python src/main.py

# Se abrirá el navegador automáticamente para autenticar
```

---

### 4. `PermissionError: [Errno 13] Permission denied`

**Causa**: No hay permisos para escribir en la carpeta de descargas

**Solución**:
```bash
# Verifica permisos de la carpeta
ls -la downloads/

# Cambiar permisos
chmod 755 downloads/

# O especifica otra carpeta con permisos
python -c "
from src.gmail_downloader.downloader import GmailAttachmentDownloader
# Cambiar download_folder en el código
"
```

---

### 5. `ConnectionError: Connection refused`

**Causa**: Sin conexión a Internet o problemas con Google API

**Solución**:
```bash
# Verifica conexión a Internet
ping google.com

# Verifica que Gmail API esté habilitada:
# https://console.cloud.google.com/apis/library/gmail.googleapis.com

# Si el error persiste, espera unos minutos
# (A veces los servidores de Google tienen issues)
```

---

### 6. `No adjuntos descargados (0 archivos)`

**Causa**: Posibles razones:
- Tus correos no tienen realmente adjuntos
- Gmail API no está habilitada
- El alcance de permisos es insuficiente

**Solución**:
```bash
# 1. Verifica que tienes correos con adjuntos
# (Puedes comprobarlo manualmente en Gmail)

# 2. Verifica que Gmail API esté habilitada
# https://console.cloud.google.com/apis/library/gmail.googleapis.com

# 3. Revisa los permisos en el código (auth.py, línea 16):
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# 4. Si no funciona, elimina token y reautentica:
rm config/token.pickle
python src/main.py
```

---

### 7. `TypeError: 'NoneType' object is not subscriptable`

**Causa**: Estructura inesperada de mensaje en Gmail API

**Solución**:
```bash
# Este error es raro. Intenta lo siguiente:

# 1. Verifica que no hay caracteres especiales en nombres
# 2. Comprueba la versión de la API:
pip show google-api-python-client

# 3. Actualiza a la última versión:
pip install --upgrade google-api-python-client

# 4. Si persiste, añade más validaciones al código
```

---

## ⚠️ Problemas Avanzados

### A. El programa es muy lento

**Causa**: Demasiados correos/adjuntos

**Solución**:
```python
# 1. Implementar paginación limitada en _get_all_messages()
# 2. Usar threading para descargas paralelas
# 3. Agregar barra de progreso

# Ejemplo: Limitar a últimos 100 correos
results = self.service.users().messages().list(
    userId="me",
    maxResults=100  # 👈 Agregar límite
).execute()
```

---

### B. Faltan adjuntos de algunos correos

**Causa**: Estructura de mensaje multipart compleja

**Solución**:
```python
# En downloader.py, mejorar la búsqueda de adjuntos:

def _has_attachments(self, payload):
    """Mejora la detección de adjuntos"""
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("filename"):
                return True
            # Buscar recursivamente en partes anidadas
            if "parts" in part:
                if self._has_attachments(part):
                    return True
    return False
```

---

### C. Nombres de archivo corrupted

**Causa**: Caracteres especiales no sanitizados correctamente

**Solución**:
```python
# Mejorar _sanitize_filename() en downloader.py:

@staticmethod
def _sanitize_filename(filename: str) -> str:
    # Extender lista de caracteres inválidos
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    
    # Limitar longitud
    max_length = 255
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1)
        filename = name[:max_length-len(ext)-1] + '.' + ext
    
    return filename
```

---

## 🧪 Debugging

### Activar modo verbose

```python
# En src/main.py, agregar logging:

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.debug("Iniciando descarga...")
```

### Verificar credenciales

```bash
# Verificar que el archivo es válido JSON
python -c "import json; json.load(open('config/credentials.json'))"

# Mostrar contenido (ocultar datos sensibles)
python -c "
import json
with open('config/credentials.json') as f:
    creds = json.load(f)
    print('Keys:', list(creds.get('installed', {}).keys()))
"
```

### Listar correos sin descargar

```python
# En ejemplos.py, agregar:

def listar_correos():
    auth = GmailAuthenticator()
    creds = auth.authenticate()
    
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    
    for msg in results.get('messages', []):
        full_msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = full_msg['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'N/A')
        print(f"- {subject}")
```

---

## 🔍 Verificaciones Previas a Ejecutar

```bash
# Lista de verificación antes de ejecutar:

# 1. ✅ Entorno virtual activado
echo $VIRTUAL_ENV

# 2. ✅ Dependencias instaladas
pip list | grep google

# 3. ✅ Archivo de credenciales existe
test -f config/credentials.json && echo "✅ OK" || echo "❌ FALTA"

# 4. ✅ Carpeta de descargas existe
mkdir -p downloads

# 5. ✅ Python 3.8 o superior
python --version

# 6. ✅ Conexión a Internet
ping -c 1 google.com

# 7. ✅ Gmail API habilitada
echo "✅ Verifica en: https://console.cloud.google.com/apis/library/gmail.googleapis.com"
```

---

## 📞 Si Nada Funciona

1. **Limpiar completamente**:
   ```bash
   rm -rf venv config/token.pickle
   python instalar.py
   ```

2. **Verificar permisos**:
   ```bash
   rm config/token.pickle
   python src/main.py
   # Autenticar de nuevo
   ```

3. **Contactar soporte Google**:
   - https://support.google.com/accounts/

4. **Revisar documentación oficial**:
   - https://developers.google.com/gmail/api/guides

---

## 💾 Guardar Logs para Debug

```python
# En src/main.py, agregar al inicio:

import logging
from datetime import datetime

# Crear archivo de log
log_file = f"logs/debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Programa iniciado")
```

---

**Última actualización**: 2025-11-20
**Para más ayuda**: Lee README_GMAIL.md o GUIA_RAPIDA.md
