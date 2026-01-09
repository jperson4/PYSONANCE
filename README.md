# Librería para trastear con audio en Python

### Setup:
Primero, deberíamos crear un venv para importar las librerías.
``` 
python3.12 -m venv ~/.venvs/AUDIO 
```

Una vez tenemos el venv creado, lo activamos e instalamos las librerías
```
source ~/.venvs/AUDIO/bin/activate
```
Proccedemos a instalar las librerías:
```
pip install numpy
pip install sounddevice
pip install matplotlib
pip install pandas
pip install plotly
```

Para mayor comodidad, podemos emplear requirements.txt:
```
pip install -r requirements.txt
```

instalamos la libreria que hemos creado:
```
pip install -e ../libreria
```

### Also check:
- [osc_gen](https://github.com/harveyormston/osc_gen)
- [AudioNoise](https://github.com/torvalds/AudioNoise)
