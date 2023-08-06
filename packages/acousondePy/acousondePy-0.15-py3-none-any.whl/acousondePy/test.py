# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:52:27 2020

@author: sven
"""


from MTRead import *
import glob

#pattern for the MT files
path = "./data/"
pattern = '*.MT'
#get list of all auxilliary MT files
fns = glob.glob(path+pattern)

print(fns)
'''
fn='C:\\Users\\sven\\Documents\\Acousonde\\test LJ2\\SBS00000.MT'
p,head,inf = MTread(fn,slMode='s',leng=0,start=0, wav_out=path +'test.wav')
spec_plot(p,head,inf)
# get the auxilliary data
aux = get_aux_MT(fns)
plt.plot(aux.Pressure)

aux.plot(subplots=True)

plt.tight_layout()
plt.show()
'''