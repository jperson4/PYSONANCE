from pysonance.const import *
from pysonance.signal import Signal

import pulsectl as pactl
import sounddevice as sd
import numpy as np
import threading
class In_Pactl(Signal):
    '''Line in mediante PACTL'''
    def __init__(self, name):
        super().__init__()
        self.sink_name = name
        self.cli_name = 'pysonance'
        self.cli = pactl.Pulse(self.cli_name)

        self.mod_id = self.create_dev()
        self.buffer = np.array([])
        
        # Threading
        self.cond = threading.Condition()
        self.buff_lock = threading.Lock()
        
        self.in_stream = sd.InputStream(samplerate=SRATE, channels=1,blocksize=CHUNK, device=f'{self.sink_name}', callback=self.callback)
        self.in_stream.start()
        
    def fun(self, tiempo):
        with self.cond:
            self.cond.wait()
            with self.buff_lock:
                _buff = self.buffer.copy()
        
            # Rellenar con ceros si no tiene el tamaño necesario ( no deberia pasar )
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
        _args=[
            'media.class=Audio/Source/Virtual',
            f'sink_name={self.sink_name}',
            # 'channel_map',
            # f'client_name={self.cli_name}',
            f'rate={SRATE}',
            'channels=1',
            'channel_map=mono',
            f'sink_properties=device.description={self.sink_name}',
        ]
        ret = self.cli.module_load('module-null-sink', args=_args)
        # Es necesario reiniciar sounddevice para que reconozca el nuevo dispositivo
        sd._terminate()
        sd._initialize()
        return ret
    
    def delete_dev(self):
        self.cli.module_unload(self.mod_id)
    
class Out_Pactl():
    '''Line out mediante PACTL'''
    def __init__(self, device, signal:Signal):
        self.sink_name = device
        self.signal = signal
        self.cli_name = 'pysonance_out'
        self.cli = pactl.Pulse(self.cli_name)
        
        _mod_id = self.create_dev()
        self.out_stream = sd.OutputStream(samplerate=SRATE, channels=1, blocksize=CHUNK, device=f'{self.sink_name}', callback=self.callback)
        self.out_stream.start()
        
    def callback(self, outdata, frames, time, status):
        _sig = self.signal.next(frames)
        outdata[:, 0] = _sig
        
    def delete_dev(self):
        self.cli.module_unload(self.mod_id)
        
    def play(self):
        ''' Conecta el device a la salida por defecto'''
        self.cli.sink_input_move(self.out_stream._stream._ptr, self.cli.get_sink_by_name('default').index)
        
    def create_dev(self):
        _args=[
            'media.class=Audio/Source/Virtual',
            f'sink_name={self.sink_name}',
            # 'channel_map',
            # f'client_name={self.cli_name}',
            f'rate={SRATE}',
            'channels=1',
            'channel_map=mono',
            f'sink_properties=device.description={self.sink_name}',
        ]
        ret = self.cli.module_load('module-null-sink', args=_args)
        # Es necesario reiniciar sounddevice para que reconozca el nuevo dispositivo
        sd._terminate()
        sd._initialize()
        return ret
    
    
    

        
    