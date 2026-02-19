from astronomy import *
from scipy.interpolate import interp1d
import numpy as np

data_67p = {
    "afstand (AU)": [1.3,2.5,3.3,4.3,5.4],
    "snelheid (km/s)": [33.3,21.3,16.8,12.5,8.5]
}

# Interpolating the data both linearly and quadratically. 
v_func1 = interp1d(data_67p["afstand (AU)"], data_67p["snelheid (km/s)"], kind='linear')
v_func2 = interp1d(data_67p["afstand (AU)"], data_67p["snelheid (km/s)"], kind='quadratic')
distances = np.linspace(1.3,5.4,100) # distances to evaluate functions on (AU)
v_values1 = v_func1(distances) 
v_values2 = v_func2(distances) 

# Calculating the speed according to the Visa-Visa formula
def vis_visa_speed(M: float, r: float, a: float) -> float:
    """
    Calculate the speed of an object in a elliptical orbit around a heavier body using the Visa-Visa formula.
    
    @param M: Mass of the heavier body (kg)
    @param r: Distance from the heavier body in meters (m)
    @param a: Semi-major axis of the body's orbit in meters (m)
    @return: Speed of the body in m/s
    """
    v = np.sqrt(G * M * (2/r - 1/a))
    return v

a_67p = 3.47 * au # semi-major axis of 67P's orbit in meters
visa_speeds = vis_visa_speed(solar_mass, distances * au, a_67p) * 1e-3 # converting m/s to km/s for comparison with data

# Determining error of interpolatations
error_linear = np.abs(v_values1 - visa_speeds)
error_quadratic = np.abs(v_values2 - visa_speeds)

import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plotting the result of the evaluated functions and the Visa-Visa formula, along with the original data points
ax1.plot(distances, v_values1, label='Linear Interpolation (fit)', color='blue', linestyle='--')
ax1.plot(distances, v_values2, label='Quadratic Interpolation (fit)', color='orange', linestyle='--')
ax1.plot(distances, visa_speeds, label='Visa-Visa Formula', color='green', linestyle='-')
ax1.scatter(data_67p["afstand (AU)"], data_67p["snelheid (km/s)"], color='red', label='Data points')
ax1.set_title('Interpolaties & Visa-Visa vergelijking')
ax1.set_xlabel('Afstand tot de zon (AU)')
ax1.set_ylabel('Snelheid (km/s)')
ax1.legend()
ax1.grid()

# Plotting the errors of the interpolations
ax2.plot(distances, error_linear, label='Error Linear interpolation', color='blue', linestyle='--')
ax2.plot(distances, error_quadratic, label='Error Quadratic interpolation', color='orange', linestyle='--')
ax2.set_title('Fout van interpolaties')
ax2.set_xlabel('Afstand tot de zon (AU)')
ax2.set_ylabel('Absolute fout (km/s)')
ax2.legend()
ax2.grid()

fig.suptitle('Analyse van de snelheid van komeet 67P als functie van afstand tot de zon')

plt.show()