Primero, deberíamos crear un venv para importar las librerías.
``` 
python3.12 -m venv ~/.venvs/AUDIO 
```

Una vez tenemos el venv creado, lo activamos e instalamos las librerías
```
source ~/.venvs/AUDIO/bin/activate
```
Proccedemos a importar las librerías:
```
pip install numpy
pip install sounddevice
pip install matplotlib
```
instalamos la libreria que hemos creado:
```
pip install -e ../libreria
```