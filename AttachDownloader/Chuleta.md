# GIT
git config --global user.email javitrapero@gmail.com
git config --global user.name javitrapero

# Terminal
Abrir un nuevo terminal: Ctrl + j

# Productivizar
pip install pyinstaller
pyinstaller --onefile src/main.py


# Entornos virtuales
python -m venv <nombreEntorno>
```

**Ejemplo:**
```powershell
python -m venv venv
python -m venv gitHubCop
```

## Activar un Entorno Virtual

### En PowerShell:
```powershell
.\<nombreEntorno>\Scripts\Activate.ps1
```

**Ejemplo:**
```powershell
.\venv\Scripts\Activate.ps1
.\gitHubCop\Scripts\Activate.ps1
```

**Nota:** Si PowerShell no permite ejecutar scripts, ejecuta primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### En CMD (Símbolo del Sistema):
```cmd
<nombreEntorno>\Scripts\activate.bat
```

**Ejemplo:**
```cmd
venv\Scripts\activate.bat
gitHubCop\Scripts\activate.bat
```

## Indicador de Entorno Activo

Cuando un entorno virtual está **activo**, verás el nombre entre paréntesis en la terminal:
```
(venv) PS C:\Users\javit\WorkSpace\EjemplosPython>
(gitHubCop) PS C:\Users\javit\WorkSpace\EjemplosPython>
```

## Desactivar el Entorno Virtual

```powershell
deactivate
```

## Listar Entornos Virtuales Creados

Para ver todos los entornos virtuales que tienes en la carpeta actual:

```powershell
Get-ChildItem -Directory | Where-Object { Test-Path "$($_.FullName)\Scripts\Activate.ps1" }
```

O más simple, lista las carpetas:

```powershell
ls  # Lista todas las carpetas, los entornos virtuales tendrán carpetas Scripts
```

**Carpeta típica de un entorno virtual:**
```
venv/
├── Scripts/
├── Lib/
├── Include/
└── pyvenv.cfg
```

## Cambiar de un Entorno Virtual a Otro

### Paso 1: Desactivar el entorno actual
```powershell
deactivate
```

### Paso 2: Activar el nuevo entorno
```powershell
.\<nombreDelNuevoEntorno>\Scripts\Activate.ps1
```

**Ejemplo completo:**
```powershell
# Verificar entorno actual (está activo si ves el nombre entre paréntesis)
deactivate  # Desactiva el entorno actual

# Activar otro entorno
.\gitHubCop\Scripts\Activate.ps1
```

## Listar Paquetes Instalados

Cuando estés **dentro de un entorno virtual activo**:

```powershell
python -m pip list
pip list
python -m pip install --upgrade pip
```

## Eliminar un Entorno Virtual

Solo elimina la carpeta completa:

```powershell
Remove-Item -Recurse -Force venv
Remove-Item -Recurse -Force gitHubCop
```

O desde el explorador: haz clic derecho → Eliminar.