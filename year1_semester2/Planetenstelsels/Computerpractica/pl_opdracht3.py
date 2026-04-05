import numpy as np 
import astronomy as stk
from astronomy import gravitational_force, center_of_mass
import matplotlib.pyplot as plt
from scipy import integrate


'''
Opdracht 1: Kepplerbanen
'''

'''1.2'''
a_maan = 3.844e8  # Semi-major-axis of the Moon [m]
com_aarde_maan = center_of_mass(stk.earth_mass, stk.moon_mass, 0, a_maan)
print(f"Center of mass of the Earth-Moon system: {com_aarde_maan:.2e} m from the center of the Earth")

'''1.3'''
# Calculating center of masses for given ranges
masses = np.linspace(0.1*stk.earth_mass, 5*stk.jupiter_mass, 100)
coms = center_of_mass(stk.solar_mass, masses, 0, stk.au) # [m]

# Plotting with relevant units
coms = coms / stk.solar_radius # [solar radii]
masses_plot = masses / stk.earth_mass # [Earth Masses]
fig1, ax = plt.subplots()
ax.plot(masses_plot, coms, label='Center of Mass')
ax.set_xlabel('Mass of the planet (M⊕)')
ax.set_ylabel('Center of Mass [R☉]')
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

fig3,ax = plt.subplots()
distrubtion = MaxBolzd(nitrogen_mass, nitrogen_temp, 0)
ax.plot(distrubtion[0], distrubtion[1]*1000, label='N2 at 300K')
ax.axvline(expected_speed, color='r', linestyle='--', label='Expected Speed (422 m/s)')
ax.set_xlabel('Velocity [m/s]')
ax.set_ylabel('Relative abundance (x1000)')
ax.set_xscale('log')
ax.set_title('Maxwell-Boltzmann Distribution for Nitrogen at 300K')
ax.legend()
ax.grid()
fig3.savefig('maxwell_boltzmann_nitrogen.png')

"''2.3'''"

gasses = { 
    # N2 and H2 included based on composition, H2O,  CO2  and CH4 are included due to their relative "fame"
    'O2' : 32*stk.atomic_mass,
    'CO2' : 44*stk.atomic_mass,
    'H2O' : 18*stk.atomic_mass,
    'CH4': 16*stk.atomic_mass,
    'H2' : 2*stk.atomic_mass
}

A = 0 # an albedo of 0, followed from the thermal equilibrium.
T_sun = 5778 # Temperature of the Sun [K]
T_earth = T_sun * (stk.solar_radius/(2*stk.au))**(1/2)*(1-A)**(1/4) # Temperature of the Earth [K]
print(T_earth)

fig4, ax = plt.subplots()

for gas, mass in gasses.items():
    distrubtion = MaxBolzd(mass, T_earth, 0)
    ax.plot(distrubtion[0], distrubtion[1], label=gas)
    maximum = np.argmax(distrubtion[1])
ax.set_xlabel('Velocity [m/s]')
ax.set_ylabel('Maxwell-Boltzmann Distribution')
ax.set_title('Maxwell-Boltzmann Distribution for Various Gases at Earth\'s Temperature')
ax.legend()
ax.grid()
ax.set_xscale('log')
# ax.set_yscale('log') # choose to include
fig4.savefig('maxwell_boltzmann_gases.png')

'''2.4'''
M_aarde_atmosfeer = 3e18 # [kg]
M_n = gasses['H2'] 
N_waterstof = M_aarde_atmosfeer / M_n  * 0.5 * 1e-6 


v_esc = np.sqrt(2*stk.G*stk.earth_mass/stk.earth_radius) # Escape velocity of Earth [m/s]

x,y = MaxBolzd(gasses['H2'], T_earth, 0.8*v_esc,)
y_int = integrate.trapezoid(y,x) 
N_waterstof_snel = N_waterstof * y_int
print(f"Het aantal deeltjes dat sneller gaan dan 80% van de ontsnappingssnelheid is: {N_waterstof_snel:.2e}, dit is {(y_int*100):.5e}% van het totale aantal waterstofdeeltjes in de atmosfeer.")
print(y_int)

'''2.5'''

afstanden = np.linspace(0.5*stk.au,2*stk.au,100)
temperaturen = T_sun * (stk.solar_radius/(2*afstanden))**(1/2)*(1-A)**(1/4) # Temperatuur van de aarde [K]

fig5 , (ax1,ax2) = plt.subplots(1,2, figsize=(12,6))
ax1.plot(afstanden/stk.au, temperaturen, label='Temperatuur')
ax1.set_xlabel('Afstand tot de zon [au]')
ax1.set_ylabel('Temperatuur [K]')
ax1.set_title('Temperatuur van een planeet als functie van de afstand tot de zon')
ax1.legend()
ax1.grid()

xs,ys = [], []
for temp in temperaturen:
    v,f  = MaxBolzd(gasses['H2'], temp, 0.8*v_esc,)
    xs.append(v)
    ys.append(f)

Ns = integrate.trapezoid(ys, x=xs, axis=1)
def halfwaarde_tijd(N):
    return -np.log(2) / np.log1p(-N) * 1/(365.25*24*3600) # [s]-> [jaar], log1p is used to avoid small N resulting in log(1).


halfwaardes = halfwaarde_tijd(Ns)

ax2.plot(afstanden/stk.au, halfwaardes, label='Halveringstijd')
ax2.set_xlabel('Afstand tot de zon [au]')
ax2.set_ylabel('Halveringstijd [jaar]')
ax2.set_yscale('log')
ax2.set_title('Halveringstijd van waterstof in de atmosfeer als functie van de afstand tot de zon')
ax2.legend()
ax2.grid()
fig5.savefig('temperature_half_life.png')

plt.show()

