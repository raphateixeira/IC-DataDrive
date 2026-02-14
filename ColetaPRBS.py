# Bibliotecas
from scipy import signal as sg
import matplotlib.pyplot as plt
import numpy as np
import serial
import time as tempo


Ts = 20e-3

setpoint = 8.0

# PRBS:
u = 2.0*(sg.max_len_seq(8)[0]-0.5)[0:200]
u = np.repeat(u,4) + setpoint
NA = len(u)
y = np.zeros(NA).astype(float)
toc = np.zeros(NA)
u = u[:NA]

tempo_medido = np.zeros(len(y)).astype(float)

# Coleta
print('\n Conexão')
conexao = serial.Serial(port='COM8',
                        baudrate=115200, 
                        timeout=0.005)

tempo.sleep(1)
print('\n Coleta')

for n in range(NA):
    tic = tempo.time()
    sinal_pwm = (u[n]*255)/15
    conexao.write(str(round(sinal_pwm)).encode())

    if (conexao.inWaiting()>0):
        y[n] = conexao.readline().decode()

    tempo.sleep(Ts)
    tempo_medido[n] = tempo.time()-tic
    

conexao.write('0'.encode())
print('\nFim da coleta.')
conexao.close()

# Gráficos
t = Ts*np.arange(0,len(u))
plt.figure(figsize=(10,10))
plt.subplot(211)
plt.step(t,u,'-b',linewidth=1.2)
plt.xlabel('Tempo(s)')
plt.ylabel('Sinal de Entrada')
plt.grid()
plt.legend(loc='lower right')

plt.subplot(212)
plt.plot(t,y,'-r',linewidth=1.2)
plt.xlabel('Tempo(s)')
plt.ylabel('sinal de saida')
plt.grid()
plt.legend(loc='lower right', labels=('Tempo','Sinal de saida'))
plt.savefig('coleta_dados_2.png', bbox_inches='tight')
plt.show()

# Salva Dados:
Dados = np.stack((tempo_medido,u,y), axis=-1)
np.save(r"DadosMG.npy",Dados)