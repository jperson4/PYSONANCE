from audio.const import *
from audio.signal import Signal
import numpy as np


class Const(Signal):
    def __init__(self, valor: float):
        super().__init__()
        self.valor = valor
        
    def fun(self, tiempo):
        return self.valor

class C(Const): # otra forma más corta de definir una constante
    def __init__(self, valor):
        super().__init__(valor)
        
class X(Signal): # (ax + b)^c
    def __init__(self, mul=C(1), add=C(0), pow=C(1)):
        super().__init__()
        self.mul = mul
        self.add = add
        self.pow = pow
        
    def fun(self, tiempo):
        _mul = self.mul.next(tiempo) / SRATE 
        _add = self.add.next(tiempo)
        _exp = self.pow.next(tiempo)
        return (_mul * tiempo + _add) ** _exp
        
''' Función genérica que permite definir muchas funciones matemáticas

    Para definir algo como f(x) = arcsin(sin(x^2) - .1) * 2, haríamos:
        g = Function(np.sin, X(pow=C(2)) - C(.1))
        f = Function(np.arcsin, g) * C(2)
        
    (es necesario que function sea una función que acepte un array de numpy como input y devuelva otro array de numpy) 
        
    Como es un poco complejo, a continuación he desarrollado algunas funciones
    de onda comunes como Sine, Triangle y Sawtooth. 
'''

class Function(Signal):
    def __init__(self, function, inside=C(0)):
        super().__init__()
        self.inside = inside
        self.function = function
        
    def fun(self, tiempo):
        return self.function(self.inside.next(tiempo))
        
''' 
    Podemos ver la frecuencia como el valor dentro del seno por el cual 
    multiplicamos el tiempo y la fase el valor que sumamos al tiempo*freq.
    
    de esta forma, para hacer algo como sin(sin(x)), haríamos:
        Sine(freq=0, phase=Sine())
    
'''
class Sine(Signal):
    def __init__(self, freq=C(1), amp=C(1), phase=C(0)):
        super().__init__()
        self.freq = freq
        self.amp = amp
        self.phase = phase
        
    def fun(self, tiempo):
        _freq = self.freq.next(tiempo) / SRATE
        _amp = self.amp.next(tiempo) 
        _phase = self.phase.next(tiempo)
        return _amp * np.sin(2 * np.pi * _freq * tiempo + _phase)
    
class Triangle(Signal):
    def __init__(self, freq=C(1), amp=C(1), phase=C(0)):
        super().__init__()
        self.freq = freq
        self.amp = amp
        self.phase = phase
        
    def fun(self, tiempo):
        _freq = self.freq.next(tiempo) / SRATE
        _amp = self.amp.next(tiempo) 
        _phase = self.phase.next(tiempo)
        return _amp * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * _freq * tiempo + _phase))
    
class Sawtooth(Signal):
    def __init__(self, freq=C(1), amp=C(1), phase=C(0)):
        super().__init__()
        self.freq = freq
        self.amp = amp
        self.phase = phase
        
    def fun(self, tiempo):
        _freq = self.freq.next(tiempo) / SRATE
        _amp = self.amp.next(tiempo) 
        _phase = self.phase.next(tiempo)
        return _amp * (2 / np.pi) * np.arctan(np.tan(np.pi * _freq * tiempo + _phase))
    
class Square(Signal):
    def __init__(self, freq=C(1), amp=C(1), phase=C(0)):
        super().__init__()
        self.freq = freq
        self.amp = amp
        self.phase = phase
        
    def fun(self, tiempo):
        _freq = self.freq.next(tiempo) / SRATE
        _amp = self.amp.next(tiempo) 
        _phase = self.phase.next(tiempo)
        return _amp * np.sign(np.sin(2 * np.pi * _freq * tiempo + _phase))
        # return _amp * sg.square(2*np.pi * tiempo * _freq+ _phase)