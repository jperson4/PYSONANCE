import subprocess
import sys
import time
from pathlib import Path
import os

def run_in_kitty(script_path: Path):
    # "--hold"
    subprocess.Popen([
        "kitty", "-e",
        sys.executable,
        str(script_path)
    ])
    
ENV = {**os.environ,
       "LANG": "es_ES.UTF-8",
       "LC_ALL": "es_ES.UTF-8",
       "XCOMPOSEFILE": "/usr/share/X11/locale/en_US.UTF-8/Compose"}

if __name__ == "__main__":
    modules_folder = Path(__file__).parent / "modules"

    if not modules_folder.exists():
        print(f"Carpeta {modules_folder} no existe")

    executed_modules = set()

    while True:
        py_files = set(modules_folder.glob("*.py"))
        py_files = {f for f in py_files if f.name != "__init__.py"}

        new_modules = py_files - executed_modules

        for module_file in new_modules:
            try:
                print(f"Lanzando {module_file.name} en kitty...")
                
                # subprocess.Popen(["kitty", "python", "sines.py"], env=ENV)
                
                run_in_kitty(module_file)
                executed_modules.add(module_file)
                print(f"{module_file.name} lanzado")
            except Exception as e:
                print(f"Error al lanzar {module_file.name}: {e}")

        time.sleep(.3) 
