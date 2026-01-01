
from pysonance.pactl import In_Pactl, Out_Pactl
from pysonance.signal import Signal

class Line_In(Signal):
    '''
    Sustituye a uns a señal por una entrada line in
    '''
    def __init__(self, nombre, tool='pactl'):
        super().__init__()
        # self.nombre = nombre
        if tool == 'pactl':
            self.mod = In_Pactl(nombre)
        else:
            raise ValueError('Tool no soportada')
        
    def fun(self, tiempo):
        return self.mod.next(tiempo)
    
    def delete_dev(self):
        self.mod.delete_dev()
    
class I(Line_In):
    def __init__(self, nombre):
        super().__init__(nombre)
    
class LineOut():
    '''
    Envuelve a una señal para que su salida vaya a la salida de audio
    '''
    def __init__(self, device, signal:Signal, tool='pactl'):
        # super().__init__()
        # self.signal = signal
        if tool == 'pactl':
            self.mod = Out_Pactl(device, signal)
        else:
            raise ValueError('Tool no soportada')
        
    # def fun(self, tiempo):
    #     _sig = self.signal.next(tiempo)
    #     self.mod.send(_sig)
    #     return _sig
    def delete_dev(self):
        self.mod.delete_dev()
        
    def play(self):
        self.mod.play()
        
class O(LineOut):
    def __init__(self, device, signal:Signal):
        super().__init__(device, signal)