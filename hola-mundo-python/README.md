# Proyecto Hola Mundo en Python

Este proyecto es una simple aplicación en Python que imprime "Hola Mundo" en la consola.

## Instalación y Configuración

### 1. Crear un Entorno Virtual

```powershell
python -m venv venv
```

### 2. Activar el Entorno Virtual

**En PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**En CMD:**
```cmd
venv\Scripts\activate.bat
```

### 3. Instalar Dependencias

```powershell
python -m pip install -r requirements.txt
```

## Instrucciones para Ejecutar

### Ejecutar la aplicación:

```powershell
python src\main.py
```

### Ejecutar los tests:

```powershell
python tests\test_main.py
```

O con unittest discover:

```powershell
python -m unittest discover -s tests -v
```

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