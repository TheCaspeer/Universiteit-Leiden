from astronomy import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import codecp2
from scipy.optimize import minimize

# Reading lightcurve data
parent_dic = r'year1_semester2\Planetenstelsels\Computerpractica'
file_loc1 = rf"{parent_dic}\WASP-203_lightcurve.dat"
data1 = np.loadtxt (rf"{file_loc1}")
phase =data1 [: ,0] # phase
flux  =data1 [: ,1] # flux

# Plotting lightcurve
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
ax1.plot(phase, flux, 'o', markersize=1)
ax1.set_title('Lightcurve of WASP-203 (raw)')
ax1.set_xlabel('Phase')
ax1.set_ylabel('Flux')
ax1.grid()

# Binning the data
binsize = 1/(len(phase)/100) # 75 bins
binned = codecp2.bincurve(phase ,flux , binsize)
phase_bin = binned [0]
flux_bin = binned [1]

# Plotting binned lightcurve
ax2.plot(phase_bin, flux_bin, 'o', markersize=1)
ax2.set_title('Lightcurve of WASP-203 (binned)')
ax2.set_xlabel('Phase')
ax2.set_ylabel('Flux')
ax2.grid()
fig1.name = "Lightcurve of WASP-203"
fig1.title = "Lightcurve of WASP-203"

# The transit happens in flux (0.94,0.96), manually read from the plot
x_transit = phase_bin [(phase_bin > -0.025) & ( phase_bin < 0.025)]
y_transit = flux_bin [(phase_bin > -0.025) & ( phase_bin < 0.025)]
transit_flux = np.mean(y_transit) # average flux during transit 
print(f"Transit flux: {transit_flux*100:.4f}% van de totale flux")

# Reading radial velocity data 
file_loc2 = rf"{parent_dic}\WASP-203_RV.dat"
data2 = np.loadtxt (rf"{file_loc2}")
time = data2 [: ,0] # time [s]
tijd = time/(3600.*24) # [s] -> [dagen]
radial_velocity = data2 [: ,1] # radial velocity [km/s]

# Plotting radial velocity data
fig2, (ax3,ax4) =  plt.subplots(1, 2, figsize=(14, 6))
ax3.scatter(tijd, radial_velocity, s=10)
ax3.set_title('Radial Velocity of WASP-203')
ax3.set_xlabel('Time [days]')
ax3.set_ylabel('Radial Velocity [km/s]')
ax3.grid()
fig2.name = "Radial Velocity of WASP-203"
fig2.title = "Radial Velocity of WASP-203"

# Fitting radial velocity (largely foreign code)
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
K_gok = 0.20  # Amplitude
phi_gok = 0 # Phase offset
P_gok = 1.5 # Period
K_0_gok = 9.35 # Mean
x0 = np.array ([ K_gok , phi_gok , P_gok , K_0_gok ])

#Hier wordt de functie gefit aan de data.
x = minimize (fit_functie , x0 , args =( tijd , radial_velocity ),method = 'Powell').x

print(f"Fitted parameters: K = {x[0]:.4f} km/s, phi = {x[1]:.4f} days, P = {x[2]:.4f} days, K_0 = {x[3]:.4f} km/s \n"
      f"Giving the sinusoïde: v(t) = {x[0]:.4f} * sin(2 * pi * (t + {x[1]:.4f}) / {x[2]:.4f}) + {x[3]:.4f}")

#De resulterende parameters
K = x[0]
phi = x[1]
P = x[2]
K_0 = x[3]

# Plotting fitted curve
tijd_sample = np.linspace (tijd.min(), tijd.max(), 1000)
def v_fitted(tijd):
   return K * np.sin (2 * np.pi * (tijd + phi) / P) + K_0
ax4.plot(tijd_sample, v_fitted(tijd_sample), color='red', label='Fitted Curve')
ax4.set_title('Fitted Radial Velocity Curve of WASP-203')
ax4.set_xlabel('Time [days]')
ax4.set_ylabel('Radial Velocity [km/s]')
ax4.grid()

# Overlaying fit on data
ax3.plot(tijd, v_fitted(tijd), color='red', label='Fitted Curve', zorder=-1) # z-axis is behind the data so that any deviations are clearly visible
ax3.legend()

# Showing and exporting all plots
plt.tight_layout()
try: 
    fig1.savefig(rf"{parent_dic}\WASP-203_lightcurve.png") 
except Exception as e:
    print(f"Error saving lightcurve figure: {e}")

try:
    fig2.savefig(rf"{parent_dic}\WASP-203_radial_velocity.png") 
except Exception as e:
    print(f"Error saving radial velocity figure: {e}")
plt.show()