
from pysonance.pactl import In_Pactl, Out_Pactl
from pysonance.signal import C, Signal
import sounddevice as sd

class Register_IO():
    '''
    Clase en la que registrar los modulos IO y que crea los dispositivos necesarios
    '''
    def __init__(self, tool='pactl'):
        self.io_modules = []
        self.tool = tool
    
    def add(self, module):
        self.io_modules.append(module)
    
    def start(self):
        for mod in self.io_modules:
            mod.create_dev()
            print(f'{mod.name()} creado')
            
        sd._terminate()
        sd._initialize()
        
        for mod in self.io_modules:
            mod.connect()
            print(f'{mod.name()} conectado')

    def stop(self):
        for mod in reversed(self.io_modules):
            mod.delete_dev()
            print(f'{mod.name()} eliminado')

class Line_In(Signal):
    '''
    Sustituye a uns a señal por una entrada line in
    '''
    def __init__(self, nombre, default=C(0), tool='pactl'):
        super().__init__()
        # self.nombre = nombre
        # self.start = False
        # self.default = C(default)
        if tool == 'pactl':
            self.mod = In_Pactl(nombre, default)
        else:
            raise ValueError('Tool no soportada')
        
    def fun(self, tiempo):
        # mientras que no se concecte, devuelve la señal por defecto
        # if not self.start:
        #     return self.default.next(tiempo) 
        return self.mod.next(tiempo)
    
    def create_dev(self):
        self.mod.create_dev()
    
    def delete_dev(self):
        self.mod.delete_dev()
        
    def connect(self):
        self.mod.connect()
        self.start = True
    
    def name(self):
        return self.mod.sink_name
    
class I(Line_In):
    def __init__(self, nombre, default=C(0), tool='pactl'):
        super().__init__(nombre, default=default, tool=tool)
    
class Line_Out():
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
    def create_dev(self):
        self.mod.create_dev()
    
    def delete_dev(self):
        self.mod.delete_dev()
        
    def connect(self):
        self.mod.connect()
        
    def play(self):
        self.mod.play()
        
    def name(self):
        return self.mod.sink_name
        
class O(Line_Out):
    def __init__(self, device, signal:Signal, tool='pactl'):
        super().__init__(device, signal, tool)