import subprocess
import sys

def test_main_output():
    result = subprocess.run([sys.executable, '../src/main.py'], capture_output=True, text=True)
    assert result.stdout.strip() == "Hola Mundo"

if __name__ == "__main__":
    test_main_output()