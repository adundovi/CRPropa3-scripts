import numpy as np

lEbins = np.arange(15, 20.51, 0.1)
lEcens = (lEbins[1:] + lEbins[:-1]) / 2

datadir='data/'
filename='out-nucleons.txt' #'out-photons.txt'

hist = np.zeros(len(lEbins)-1, dtype='int32')

with open(datadir+filename) as rawdata:
    for line in rawdata:
        if line[0] == '#':
            continue
        data = line.split()
        E = data[2]
        if float(E) == 0:
            continue
        htemp = np.histogram(np.log10(float(E))+18, lEbins)[0]
        hist += htemp

for p in hist:
    print p, " ",
