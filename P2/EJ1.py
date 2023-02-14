

# reproductor con Chunks

import numpy as np         # arrays
import sounddevice as sd   # modulo de conexión con portAudio
import math as m
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE= 44100

# corregido
last = 0 # ultimo frame generado
def oscChuck(frec,vol):
    global last # var global
    data = np.float32(vol*np.sin(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE))
    last += CHUNK # actualizamos ultimo generado
    return data



# leemos wav en array numpy (data)
# por defecto lee float64 (no soportado por portAudio)
# podemos hacer directamente la conversion a float32
#data, SRATE = sf.read('ex1.wav',dtype="float32")




# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

# arrancamos stream
stream.start()



kb = kbhit.KBHit()
c= ' '

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
numBloque = 0 # contador de bloques/chunks

vol = 0.5
frec=440
print('\n\nProcessing chunks: ',end='')

# termina con 'q' o cuando no queden samples
end = False # será true cuando el chunk esté vacio

while c!= 'q' and not(end)>0:
    # nuevo bloque. Si tiene menos de CHUNK samples coge los que quedan
    bloque = oscChuck(frec,vol)
    stream.write(bloque) # escribimos al stream
    # modificación de volumen
    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): vol= max(0,vol-0.05)
        elif (c=='V'): vol= min(1,vol+0.05)
        elif(c=='F'): frec= min(frec*( 2**(1/12)),20000)
        elif(c=='f'): frec= max(20,frec/( 2**(1/12)))
        print("Vol: ",vol)
        print("Frec: ",frec)

    print('.',end='')

print('end')

stream.stop()
stream.close()
kb.set_normal_term()

#%%
