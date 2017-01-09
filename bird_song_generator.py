import numpy as np
from scipy.integrate import odeint
from scipy.io import wavfile
import os
import os.path

"""
This is a bird song generator by ilknuricke

https://github.com/ilknuricke/birdsong_generator_CPG

but in python!

To see how it works, see the original, especially this wonderfull blog:
http://mindwriting.org/blog/?p=229

Changes compared to the original:
-Brain and syrinx models are merged into a single set of ODE to avoid the interpolation
-Duration of a syllable is 0.3 s, not 0.24 s as stated in the original source

Variables meaning (see the original):
y = [ xp , y , xk,  x , y  ]
 ...|    brain   |  syrinx  |

Some changes would have to be done to remove the pops between the syllables
"""

#brain global variables
rho1=0.
rho3=6.
A=10.
B=10.
C=10.
D=-2.
E=4.
alpha=2.
beta=20.

#syrinx global variables
b=1000.
d=10.**8

#syllable creation variables

Fs = 22050    #sampling frequency
t_lim=0.3     #duration of a syllable in seconds
    
def bird_model(y,t_now,rho2):
    dydt=np.zeros(5)
    
    #brain part

    dydt[0] = 30.*(-y[0]+(1/(1+np.exp(-1*(rho1+A*y[0]-B*y[1])))))
    dydt[1] = 30.*(-y[1]+(1/(1+np.exp(-1*(rho2+C*y[0]-D*y[1]+alpha*y[2])))))
    dydt[2] = 120.*(-y[2]+(1/(1+np.exp(-1*(rho3+E*y[2]-beta*y[1])))))

    #syrinx part

    p=7000.*y[0]-2200.
    k=1.4*10**9*y[2]+4.8*10.**8
    
    dydt[3]=y[4]
    dydt[4]=-k*y[3]-(b-p)*y[4]-d*y[4]*y[3]**2
    
    return dydt

def sing_syllable(rho2):
    t = np.arange(0,t_lim,1./Fs)
    
    result=odeint(bird_model,0.01*np.ones(5), t, (rho2,))

    sound=result.T[4].astype('float32')
    sound/=np.max(sound)
    return sound

print 'creating syllables'

syllables={}
syllables['a']=sing_syllable(-11.)
syllables['b']=sing_syllable(-11.8)
syllables['c']=sing_syllable(-7.1)

#uncomment to save the syllables as wav files
'''
if not os.path.isdir('syllables'):

    os.mkdir('syllables')
for i in syllables.keys():
    print i
    wavfile.write('syllables/'+i+'.wav',Fs,syllables[i])
'''

print 'creating songs'
if not os.path.isdir('songs'):
    os.mkdir('songs')

songs=['abcc','bbc','cccc','bba']

for song in songs:
    song_sound=np.array([])
    print song
    for i in song:
        song_sound=np.concatenate((song_sound,syllables[i]))

    wavfile.write(os.path.join('songs',song+'.wav'),Fs, song_sound)

