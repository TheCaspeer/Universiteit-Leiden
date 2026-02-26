from astronomy import *
import matplotlib.pyplot as plt
import numpy as np


parent_dic = r'year2_semester2\Planetenstelsels\Computerpractica'
file_loc = rf"{parent_dic}\WASP-203_lightcurve.dat"
data=np. loadtxt (rf"{file_loc}")
phase =data [: ,0] # phase
flux  =data [: ,1] # flux

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
ax1.plot(phase, flux, 'o', markersize=1)
ax1.set_title('Lightcurve of WASP-203 (raw)')
ax1.set_xlabel('Phase')
ax1.set_ylabel('Flux')
ax1.grid()


import codecp2

binsize = 1/(len(phase)/100) # 75 bins, iets te weinig atm lulw
binned = codecp2.bincurve(phase ,flux , binsize)
phase_bin = binned [0]
flux_bin = binned [1]

ax2.plot(phase_bin, flux_bin, 'o', markersize=1)
ax2.set_title('Lightcurve of WASP-203 (binned)')
ax2.set_xlabel('Phase')
ax2.set_ylabel('Flux')
ax2.grid()
plt.tight_layout()
# plt.show()


# the transit happens in flux (0.94,0.96)
y_transit = flux_bin[(flux_bin > 0.94) & (flux_bin < 0.96)]
transit_flux = np.mean(y_transit) # average flux during transit 
print("Transit flux: {}% van de totale flux".format(transit_flux))

