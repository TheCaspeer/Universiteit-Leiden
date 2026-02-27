from astronomy import *
import matplotlib.pyplot as plt
import numpy as np


parent_dic = r'year2_semester2\Planetenstelsels\Computerpractica'
file_loc1 = rf"{parent_dic}\WASP-203_lightcurve.dat"
data1 = np.loadtxt (rf"{file_loc1}")
phase =data1 [: ,0] # phase
flux  =data1 [: ,1] # flux

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
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
fig1.name = "Lightcurve of WASP-203"
# plt.tight_layout()
# plt.show()

# the transit happens in flux (0.94,0.96)
y_transit = flux_bin[(flux_bin > 0.94) & (flux_bin < 0.96)]
transit_flux = np.mean(y_transit) # average flux during transit 
print(f"Transit flux: {transit_flux:.4f}% van de totale flux")


# Radial velocity data and plot
file_loc2 = rf"{parent_dic}\WASP-203_RV.dat"
data2 = np.loadtxt (rf"{file_loc2}")
time = data2 [: ,0] # time [s]
radial_velocity = data2 [: ,1] # radial velocity [km/s]

fig2, (ax3,ax4) =  plt.subplots(1, 2, figsize=(14, 6))
ax3.scatter(time, radial_velocity, s=10)
ax3.set_title('Radial Velocity of WASP-203')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Radial Velocity (km/s)')
ax3.grid()
fig2.name = "Radial Velocity of WASP-203"


# plt.tight_layout()
# plt.show()

# quit() # remove

# Fitting radial velocity 
from scipy.optimize import minimize

gemeten_tijd = time/(3600.*24) # [s] -> [dagen]
gemeten_radial_velocity = radial_velocity # [km/s]
def fit_functie (variabelen , tijd , v_gemeten ):
    # De variabelen die we gaan fitten.
    K = variabelen [0]
    phi = variabelen [1]
    P = variabelen [2]

    K_0 = variabelen [3]

    # Uitrekenen wat de huidige fit zou doen.
    v_fit = K * np.sin (2 * np.pi * (tijd + phi) / P) + K_0
    # We minimaliseren de som van de least squares .
    return np.sum (( v_gemeten - v_fit) ** 2)

#De initiele gok waarmee minimize mee gaat beginnen .
K_gok = 0.25
phi_gok = 0.5
P_gok = 0.2e6/(3600.*24) # 0.2 miljoen seconden -> dagen # Eigenlijk moet de plot ook in dagen maar fuck dat voor nu
K_0_gok = 9.35
x0 = np.array ([ K_gok , phi_gok , P_gok , K_0_gok ])

#Hier wordt de functie gefit aan de data.
x = minimize (fit_functie , x0 , args =( gemeten_tijd , gemeten_radial_velocity ),method = 'Powell').x

#De resulterende parameters .
K = x[0]
phi = x[1]
P = x[2]
K_0 = x[3]


# Plotting fitted curve
tijd_sample = np.linspace (gemeten_tijd.min(), gemeten_tijd.max(), 1000)

def v_fitted(tijd):
   return K * np.sin (2 * np.pi * (tijd + phi) / P) + K_0

ax4.plot(tijd_sample, v_fitted(tijd_sample), color='red', label='Fitted Curve')
ax4.set_title('Fitted Radial Velocity Curve of WASP-203')
ax4.set_xlabel('Time [days]')
ax4.set_ylabel('Radial Velocity [km/s]')
ax4.grid()

plt.tight_layout()
plt.show()