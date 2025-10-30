"""
Práctica 3: Sistema musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Alejandro Ramirez Zepeda
Número de control: 22211765
Correo institucional: 22211765@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Instalar librerias en consola
#!pip install control
#!pip install slycot

import control as ctrl
import math as m
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

x0,t0,tF,dt,w,h = 0,0,10,1E-3,10,5
N = round((tF-t0)/dt) + 1
t = np.linspace(t0,tF,N)
u = np.zeros(N); u [round(1/dt):round(2/dt)] = 1

def musculo(Cs,Cp,R,Alfa):
    num = [Cs*R,1-Alfa]
    den = [R*(Cp + Cs),1]
    sys = ctrl.tf(num,den)
    return sys

#Funcion de trnasferencia: Control
Cs,Cp,R,Alfa = 10E-6,100E-6,100,0.25
syscontrol = musculo(Cs,Cp,R,Alfa)
print(f'Funcion de transferencia del control: {syscontrol}')

#Funcion de trnasferencia: Caso
Cs,Cp,R,Alfa = 10E-6,100E-6,10000,0.25
syscaso = musculo(Cs,Cp,R,Alfa)
print(f'Funcion de transferencia del casso: {syscaso}')

#Respuestas en lazo abierto (Sin tratamiento)
_,Fs1 = ctrl.forced_response(syscontrol,t,u,x0) #Control
_,Fs2 = ctrl.forced_response(syscaso,t,u,x0) #Caso

fg1 = plt.figure()
plt.plot(t,u,'-',linewidth=1, color= np.array([127,76,165])/255, label = 'F(t)')
plt.plot(t,Fs1,'-',linewidth=1, color= np.array([5,127,109])/255, label = 'Fs(t): Control')
plt.plot(t,Fs2,'-',linewidth=1, color=np.array([223,57,105])/255, label = 'Fs(t): Caso')

plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.05,1.03); plt.yticks(np.arange(0,1.2, 0.2))
plt.xlabel('Fs(t) [V]')
plt.ylabel('t [s]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('Sistema musculoesquelético python.png', dpi=600, bbox_inches='tight')
fg1.savefig('Sistema musculoesquelético python.pdf')

def tratamiento(kP,kI,sys):
    Cr = 1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    numPI = [Rr*Cr,1]
    denPI = [Re*Cr,0]
    PI = ctrl.tf(numPI,denPI)
    X = ctrl.series(PI,sys)
    sysPI = ctrl.feedback(X,1,sign= -1)
    return sysPI

CasoPI = tratamiento(0.020982,43250.2057,syscaso)

#Respuestas en lazo cerrado
_, Fs3 = ctrl.forced_response(CasoPI,t,Fs1,x0) #Tratamiento

fg2 = plt.figure()
plt.plot(t,u,'-',linewidth=1, color= np.array([127,76,165])/255, label = 'F(t)')
plt.plot(t,Fs1,'-',linewidth=1, color= np.array([5,127,109])/255, label = 'Fs(t): Control')
plt.plot(t,Fs2,'-',linewidth=1, color=np.array([223,57,105])/255, label = 'Fs(t): Caso')
plt.plot(t,Fs3,':',linewidth=1, color=np.array([51,199,216])/255, label = 'Fs(t): Tratamiento')

plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.05,1.03); plt.yticks(np.arange(0,1.2, 0.2))
plt.xlabel('Fs(t) [V]')
plt.ylabel('t [s]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3)
plt.show()
fg2.set_size_inches(w,h)
fg2.tight_layout()
fg2.savefig('Sistema musculoesquelético PI python.png', dpi=600, bbox_inches='tight')
fg2.savefig('Sistema musculoesquelético PI python.pdf')
    