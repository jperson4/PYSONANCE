from pysonance.const import *
from pysonance.signal import Signal

import pulsectl as pactl
import sounddevice as sd
import numpy as np
import threading

command = 'pactl load-module  module-null-sink'

class Line_In(Signal):
    '''
    Envuelve una señal para que actúe como un line-in virtual
    '''
    def __init__(self, nombre):
        super().__init__()
        # self.nombre = nombre
        self.mod = Pactl(nombre)
        
    def fun(self, tiempo):
        return self.mod.next(tiempo)
    
class I(Line_In):
    def __init__(self, nombre):
        super().__init__(nombre)
    
    
class Pactl(Signal):
    '''Line in mediante PACTL'''
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.cli_name = 'pysonance'
        self.cli = pactl.Pulse(self.cli_name)
        _mod_id = self.create_dev()
        self.buffer = np.array([])
        
        # Threading
        self.cond = threading.Condition()
        self.buff_lock = threading.Lock()

        
        self.in_stream = sd.InputStream(samplerate=SRATE, channels=1, callback=self.callback,blocksize=CHUNK, device=f'{self.name}')
        self.in_stream.start()
        
    def fun(self, tiempo):
        with self.cond:
            self.cond.wait()
            with self.buff_lock:
                _buff = self.buffer.copy()
                # no son necesarios porque buffer solo guarda un chunk
                # _buff = self.buffer[:len(tiempo)].copy()
                # self.buffer = self.buffer[len(tiempo):]
        
            # Rellenar con ceros si no tiene el tamaño necesario
        if len(_buff) < len(tiempo):
                _buff = np.concatenate((_buff, np.zeros(len(tiempo) - len(_buff))))
        
        return _buff        

    def callback(self, indata, frames, time, status):
        block = indata[:, 0].copy()
        with self.buff_lock:
            # self.buffer = np.concatenate((self.buffer, block))
            self.buffer = block
        with self.cond:
            self.cond.notify()
        
    def create_dev(self):
        # TODO arreglar
        _args=[
            'media.class=Audio/Source/Virtual',
            f'sink_name={self.name}',
            # 'channel_map',
            # f'client_name={self.cli_name}',
            'channels=1'
        ]
        return self.cli.module_load('module-null-sink', args=_args)