import numpy as np 
import astronomy as stk
from astronomy import gravitational_force, center_of_mass
import matplotlib.pyplot as plt


'''
Opdracht 1: Kepplerbanen
'''

'''1.2'''
a_maan = 3.844e8  # Semi-major-axis of the Moon [m]
com_aarde_maan = center_of_mass(stk.earth_mass, stk.earth_mass, 0, a_maan)

'''1.3'''
# Calculating center of masses for given ranges
masses = np.linspace(0.1*stk.earth_mass, 5*stk.jupiter_mass, 100)
coms = center_of_mass(stk.solar_mass, masses, 0, stk.au) # [m]

# Plotting with relevant units
coms = coms / stk.au # [au]
masses_plot = masses / stk.earth_mass # [Earth Masses]
fig1, ax = plt.subplots()
ax.plot(masses_plot, coms, label='Center of Mass')
ax.set_xlabel('Mass of the planet (Earth masses)')
ax.set_ylabel('Center of Mass [au]')
ax.set_title('Center of Mass of a planet-sun system with a SMA of 1 au')
ax.legend()
ax.grid()
fig1.savefig('center_of_mass_plot.png')

'''1.4'''

# Planetary information, relative to center of mass
p_perihelion = 0.2 * stk.au  # Perihelion distance  [m]
p_aphelion = 6 * stk.au  # Aphelion distance

# "De zon doorloopt een een ellips geschaald met m_p/(m_sun+m_p)" - BS lecture 1 slide 47 (moet verslag in)
scale_factor =  masses/(stk.solar_mass+masses)
zon_perihelion = p_perihelion * scale_factor # [m]
zon_aphelion = p_aphelion * scale_factor # [m]

# Plotting with relevant units
zon_perihelion = zon_perihelion / stk.au # [au]
zon_aphelion = zon_aphelion / stk.au # [au]
fig2, ax = plt.subplots()
ax.plot(masses_plot, zon_perihelion, label='Zon Perihelion')
ax.plot(masses_plot, zon_aphelion, label='Zon Aphelion')
ax.set_xlabel('Mass of the planet (Earth masses)')
ax.set_ylabel('Distance from the Sun [au]')
ax.set_title('Distance of the Sun from the center of mass at perihelion and aphelion')
ax.legend()
ax.grid()
fig2.savefig('zon_distance_plot.png')


''' 
Opdracht 2: Atmosferen
'''

'''2.1'''

def MaxBolzd(m: float, T: float, vmin: float) -> tuple[np.ndarray, np.ndarray]:
    '''
    Calculate the Maxwell-Boltzmann distribution for a given mass, temperature between a  minimum velocity and 30000 m/s.
    
    @param m (float): Mass of the particle [kg]
    @param T (float): Temperature of the system [K]
    @param vmin (float): Minimum velocity to consider [m/s]
    
    @return (tuple): Tuple containing the given velocities and their corresponding Maxwell-Boltzmann distribution values.
    '''


    
    v = np.arange(vmin,30000,1)
    f = (m/(2*np.pi*stk.k*T))**(3/2)* 4*np.pi*v**2*np.exp(-m*v**2/(2*stk.k*T))
    return v,f

'''2.2'''

expected_speed = 422
nitrogen_temp = 300
nitrogen_mass = 28 * stk.atomic_mass # vo voor Rino

fig2,ax = plt.subplots()
ax.plot(MaxBolzd(nitrogen_mass, nitrogen_temp, 0)[0], MaxBolzd(nitrogen_mass, nitrogen_temp, 0)[1], label='N2 at 300K')
ax.axvline(expected_speed, color='r', linestyle='--', label='Expected Speed (422 m/s)')
ax.set_xlabel('Velocity [m/s]')
ax.set_ylabel('Maxwell-Boltzmann Distribution')
ax.set_xscale('log')
ax.set_title('Maxwell-Boltzmann Distribution for Nitrogen at 300K')
ax.legend()
ax.grid()
fig2.savefig('maxwell_boltzmann_nitrogen.png')
plt.show()
