import numpy as np
from scipy.stats import binned_statistic

# bin data
# input, fase van de data, genormaliseerde flux en de grootte van de bins
# output, array met in de eerste kolom fase en in tweede kolom genormaliseerde flux
def bincurve(phase, flux, binsize):
    bins = 1.0 / binsize
    #werkt alleen met een array met waarden tussen 0 en 1!
    newphase = []
    newflux = []
    x = np.arange(np.min(phase),np.max(phase), binsize)
    for bin in x:
        count = 0
        f = []
        for p in range(len(phase)):
            if (phase[p] >= bin and phase[p] < bin+binsize):
                count = count + 1
                f.append(flux[p])
 
        newphase.append(bin + binsize/2)
        g = np.array(f)
        newflux.append(np.mean(g))

    return np.array(newphase),np.array(newflux)

def bincurve_fast(phase, flux, binsize):
    nbins = int(np.round((phase.max()-phase.min())/binsize))
    phase_binned, binedges, _ = binned_statistic(phase, flux, statistic='mean', bins=nbins)

    return binedges[0:-1]+0.5*(binedges[1:]-binedges[0:-1]), phase_binned
