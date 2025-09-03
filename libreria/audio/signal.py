from audio.const import *
import numpy as np

class Signal:
    def __init__(self):
        self.frame = 0
        
    ''' Devuelve un chunk de señal '''
    def next(self, tiempo=None):
        _tiempo = tiempo
        if tiempo is None:
            _tiempo = np.arange(self.frame, self.frame + CHUNK)
            self.frame += CHUNK
        return self.funcion(_tiempo)
            
    ''' Función que define la señal '''
    def funcion(self, tiempo):
        return np.zeros(len(tiempo))
    
    def reset(self):
        self.frame = 0
        
    # Operadores
    def __add__(self, other):
        return Add(self, other)
        
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __neg__(self):
        return Neg(self)
    
    def __pow__(self, power):
        return Pow(self, power)
    
class Add(Signal):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
        
    def funcion(self, tiempo):
        return self.a.next(tiempo) + self.b.next(tiempo)
    
class Sub(Signal):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
        
    def funcion(self, tiempo):
        return self.a.next(tiempo) - self.b.next(tiempo)

class Mul(Signal):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
        
    def funcion(self, tiempo):
        return self.a.next(tiempo) * self.b.next(tiempo)
    
class Div(Signal):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
        
    def funcion(self, tiempo):
        return self.a.next(tiempo) / self.b.next(tiempo)
    
class Neg(Signal):
    def __init__(self, a):
        super().__init__()
        self.a = a
        
    def funcion(self, tiempo):
        return -self.a.next(tiempo)
    
class Pow(Signal):
    def __init__(self, a, power):
        super().__init__()
        self.a = a
        self.power = power
        
    def funcion(self, tiempo):
        return self.a.next(tiempo) ** self.power.next(tiempo)
    

    

    