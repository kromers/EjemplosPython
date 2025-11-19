import subprocess
import sys
from pathlib import Path

def test_main_output():
    # Obtener la ruta absoluta de main.py basada en la ubicación de este test
    test_dir = Path(__file__).resolve().parent
    main_py = test_dir.parent / "src" / "main.py"
    
    print("\n" + "="*60)
    print("EJECUCIÓN DE TESTS")
    print("="*60)
    print(f"Fichero .py testeado: {main_py.name}")
    print(f"Ruta: {main_py}")
    print("-"*60)
    
    try:
        result = subprocess.run([sys.executable, str(main_py)], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        expected = "Hola Mundo"
        
        print(f"Salida obtenida: '{output}'")
        print(f"Salida esperada: '{expected}'")
        print("-"*60)
        
        assert output == expected, f"Salida no coincide: esperado '{expected}', obtenido '{output}'"
        
        print("✓ TEST EXITOSO")
        print("="*60 + "\n")
        
    except AssertionError as e:
        print(f"✗ TEST FALLIDO")
        print(f"Error: {e}")
        print("="*60 + "\n")
        raise
    except subprocess.TimeoutExpired:
        print(f"✗ TEST FALLIDO")
        print(f"Error: El script tardó más de 5 segundos en ejecutarse")
        print("="*60 + "\n")
        raise
    except Exception as e:
        print(f"✗ TEST FALLIDO")
        print(f"Error: {type(e).__name__}: {e}")
        print("="*60 + "\n")
        raise

if __name__ == "__main__":
    test_main_output()