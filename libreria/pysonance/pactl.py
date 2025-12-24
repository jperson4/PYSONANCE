from pysonance.const import *
from pysonance.signal import Signal

import pulsectl as pactl
import sounddevice as sd
import numpy as np

command = 'pactl load-module  module-null-sink'

class Line_In(Signal):
    '''
    Envuelve una señal para que actúe como un line-in virtual
    '''
    def __init__(self, nombre):
        # self.nombre = nombre
        self.mod = Pactl(nombre)
        
    def next(self, tiempo):
        return self.mod.next(tiempo)
    
class I(Line_In):
    def __init__(self, nombre):
        super().__init__(nombre)
    
    
class Pactl(Signal):
    '''Line in mediante PACTL'''
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.cli_name = 'pysonance'
        self.cli = pactl.Pulse(self.cli_name)
        _mod_id = self.create_dev()
        self.buffer = np.array([])
        self.instr = sd.InputStream(samplerate=SRATE, channels=1, callback=self.callback,blocksize=CHUNK, device=f'{self.nombre}')
        self.instr.start()

    
    def fun(self, tiempo):
        _buff = self.buffer[:len(tiempo)]
        self.buffer = self.buffer[len(tiempo):]
        
        # Rellenar con ceros si no tiene el tamaño necesario
        if len(_buff) < len(tiempo):
            _buff = np.concatenate((_buff, np.zeros(len(tiempo) - len(_buff))))
        
        return _buff
        
        
    def create_dev(self):
        _args=[
            'media.class=Audio/Source/Virtual',
            f'sink_name={self.nombre}',
            # 'channel_map',
            # f'client_name={self.cli_name}',
            'channels=1'
        ]
        return self.cli.module_load('module-null-sink', args=_args)
        

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        bloque = indata[:, 0].copy()
        self.buffer = np.concatenate((self.buffer, bloque))