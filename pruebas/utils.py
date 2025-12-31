from copy import deepcopy
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import plotly.express as px
import scipy.io.wavfile as wav

from pysonance.signal import Signal
from pysonance.const import SRATE, CHUNK

'''REPRODUCTOR'''
input = None

def callback(outdata, frames, time, status):
    global input
    # print('entro')
    if input is not None:
        bloque = input.next()
        # convertimos formato (CHUNK,) a (CHUNK,1) para que adecuarlo a sounddevice
        outdata[:] = bloque.reshape(-1, 1)
    else:
        # si no hay datos, reproducimos silencio
        outdata[:] = np.zeros((CHUNK, 1))
        
def start_audio():
    ''' Inicia el stream de audio de salida'''
    # stream de salida con callBack
    stream = sd.OutputStream(samplerate=SRATE, channels=2, callback=callback, blocksize=CHUNK)
    stream.start()

def showOsc(osc:Signal, time, chunks=False):
    ''' Muestra una señal'''
    _osc = deepcopy(osc)
    _sig = np.zeros(0)
    _chunks = int(time*(SRATE+CHUNK)/CHUNK)
    if chunks:
        _chunks = time
    for i in range(_chunks):
        _sig = np.concatenate((_sig, _osc.next()))
    plt.plot(_sig)
    
def play(osc:Signal, add=False):
    global input 
    if add is False or input is None:
        input = osc # sustituye lo que estaba sonando antes
    else:
        input += osc # añade a lo que estaba sonando antes
        
def stop():
    global input 
    input = None
    
def playFor(osc:Signal, secs=5, add=False):
    ''' Reproduce una señal durante unos segundos'''
    play(osc)
    time.sleep(secs)
    stop()   
    
def live(osc:Signal, secs=2):
    ''' Devuelve los chunks concatenados como si se hubieran sacado live'''
    wave = np.array([])
    for i in range(int(secs*SRATE/CHUNK)):
        chunk = osc.next(CHUNK)
        wave = np.concatenate((wave, chunk))
    return wave 
    
def show(osc:Signal, secs=.5):
    ''' Muestra la señal '''
    plt.plot(osc.next(SRATE*secs))
    
def show_px(osc:Signal, secs=.5):
    ''' Ploty express'''
    df = pd.DataFrame({"amp": osc.next(SRATE*secs)})
    df["secs"] = df.index / SRATE
    wave = px.line(df, y="amp", title="Waveform")
    wave.show()
    
def show_live(osc:Signal, secs=.5):
    '''Emula live'''
    wave = live(osc, secs)
    plt.plot(wave)
    
def show_px_live(osc:Signal, secs=.5):
    ''' Ploty express + emula live'''
    wave = live(osc, secs)
    df = pd.DataFrame({"amp": wave})
    df["secs"] = df.index / SRATE
    wave = px.line(df, y="amp", title="Waveform")
    wave.show()

def toWav(osc:Signal, filename="output.wav", secs=5):
    wave = osc.next(SRATE*secs)
    wave = (wave * 32767).astype(np.int16)  # Convertir a formato PCM 16 bits
    wav.write(filename, SRATE, wave)
    
def toWav_live(osc:Signal, filename="output.wav", secs=5):
    wave = np.array([])
    for i in range(int(secs*SRATE/CHUNK)):
        chunk = osc.next(CHUNK)
        wave = np.concatenate((wave, chunk))
    wave = (wave * 32767).astype(np.int16)  # Convertir a formato PCM 16 bits
    wav.write(filename, SRATE, wave)
        
    