import numpy as np 
import astronomy  as stk 
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
ax.set_xlabel('Mass of the planet [M⊕]')
ax.set_ylabel('Center of Mass [R☉]')
ax.set_title('Center of Mass of a planet-sun system with a SMA of 1 au')
ax.legend()
ax.grid()

'''1.4'''
a_zon = masses / stk.solar_mass * stk.au # [m]
P_zon =( (4 * np.pi*82 * stk.au**3) / (stk.G * (stk.solar_mass+masses)) )**0.5 # [s]
v_zon = 2 * np.pi * a_zon / P_zon # [m/s]
fig2, ax = plt.subplots()
ax.plot(masses_plot, v_zon, label='Orbital Velocity of the Sun')
ax.set_xlabel('Mass of the planet [M⊕]')
ax.set_ylabel('Orbital Velocity of the Sun [m/s]')
ax.set_title('Orbital Velocity of the Sun as a function of Planet Mass at 1 AU')
ax.legend()
ax.grid()

'''1.5'''
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
fig3, ax = plt.subplots()
ax.plot(masses_plot, zon_perihelion, label='Zon Perihelion')
ax.plot(masses_plot, zon_aphelion, label='Zon Aphelion')
ax.set_xlabel('Mass of the planet (Earth masses)')
ax.set_ylabel('Distance from the Sun [au]')
ax.set_title('Distance of the Sun from the center of mass at perihelion and aphelion')
ax.legend()
ax.grid()


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

# For cleanliness, the functions from other exercises are also placed here
def T_planet(distance: float, albedo: float = 0, T_sun: float = 5778) -> float:
    '''
    Calculate the temperature of a planet based on its distance from the sun and its albedo. 
    
    @param distance (float): Distance from the sun [m]
    @param albedo (float): Albedo of the planet (between 0 and 1) (in this exercise only 0 is considered)
    @param T_sun (float): Temperature of the sun [K] (base value is 5778 K)
    
    @return (float): Temperature of the planet [K]
    '''
    T_planet = T_sun * (stk.solar_radius/(2*distance))**(1/2)*(1-albedo)**(1/4)
    return T_planet

def escape_velocity(mass: float, radius: float = stk.earth_radius) -> float:
    '''
    Calculate the escape velocity for a given mass and radius.
    
    @param mass (float): Mass of the planet [kg]
    @param radius (float): Radius of the planet [m] (base value is Earth's radius)
    
    @return (float): Escape velocity [m/s]
    '''
    return np.sqrt(2*stk.G*mass/radius)

def halfwaarde_tijd(N: float) -> float:
    """
    Calculate the half-life of a gas in the atmosphere based on the fraction of particles that escape.
    (derivation included in the raport)

    @param N (float): Fraction of particles that escape (between 0 and 1) per second
    
    @return (float): Half-life of the gas in years
    """
    return -np.log(2) / np.log1p(-N) * 1/(365.25*24*3600) # [s]-> [jaar], log1p is used to avoid small N resulting in log(1).


'''2.2'''

expected_speed = 422 # [m/s]
nitrogen_temp = 300 # [K]
nitrogen_mass = 28 * stk.atomic_mass #[kg]  vo voor Rino

# Plotting the Boltzmann distrubtion for N2 at 300K, with the expected value included.
fig4,ax = plt.subplots()
distrubtion = MaxBolzd(nitrogen_mass, nitrogen_temp, 0)
ax.plot(distrubtion[0], distrubtion[1]*1000, label='N2 at 300K')
ax.axvline(expected_speed, color='r', linestyle='--', label='Expected Speed (422 m/s)')
ax.set_xlabel('Velocity [m/s]')
ax.set_ylabel('Relative abundance (x1000)')
ax.set_xscale('log')
ax.set_title('Maxwell-Boltzmann Distribution for Nitrogen at 300K')
ax.legend()
ax.grid()

"''2.3'''"

gasses = { 
    # N2 and H2 included based on composition, H2O,  CO2  and CH4 are included due to their relative "fame"
    'O2' : 32*stk.atomic_mass,
    'CO2' : 44*stk.atomic_mass,
    'H2O' : 18*stk.atomic_mass,
    'CH4': 16*stk.atomic_mass,
    'H2' : 2*stk.atomic_mass
}

T_sun = 5778 # Temperature of the Sun [K]
T_earth = T_planet(stk.au) # Temperature of the Earth [K]

# Plotting the probability distrubtion for each gas
fig5, ax = plt.subplots()
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
ax.set_yscale('log')

'''2.4'''
# Determing amount of hydrogen molecules in the atmosphere
M_aarde_atmosfeer = 3e18 # [kg]
M_n = gasses['H2'] 
N_waterstof = M_aarde_atmosfeer / M_n  * 0.5 * 1e-6 


# The amount of particle that leave the atmosphere is those who go faster than 80%, 
# We can determine the relative amount by integrating the distrubtion from 0.8*escape_velocity to infinity 
# With 30k being approximated as infinity. 
v_esc = escape_velocity(stk.earth_mass) # Escape velocity of Earth [m/s]
x,y = MaxBolzd(gasses['H2'], T_earth, 0.8*v_esc,)
y_int = integrate.trapezoid(y,x) 
N_waterstof_snel = N_waterstof * y_int
print(f"Het aantal deeltjes dat sneller gaan dan 80% van de ontsnappingssnelheid is: {N_waterstof_snel:.2e}, dit is {(y_int*100):.5e}% van het totale aantal waterstofdeeltjes in de atmosfeer.")

'''2.6'''
afstanden = np.linspace(0.5*stk.au,2*stk.au,100)
temperaturen = T_planet(afstanden) # Temperaturen van de aarde op afstanden (0.5AU, 2AU) [K]

# Plotting temperature v semi-major-axis
fig6 , (ax1,ax2) = plt.subplots(1,2, figsize=(12,6))
ax1.plot(afstanden/stk.au, temperaturen, label='Temperature')
ax1.set_xlabel('Distance to the sun [au]')
ax1.set_ylabel('Temperature [K]')
ax1.set_title('Temperature of Earth  as a function of SMA')
ax1.legend()
ax1.grid()

# An approach with Numpy vectorized arrays would be preferable, but it is not known how to implement this without running into broadcasting mismatch issues.
xs,ys = [], []
for temp in temperaturen:
    v,f  = MaxBolzd(gasses['H2'], temp, 0.8*v_esc,)
    xs.append(v)
    ys.append(f)

# Determining fraction lost / s 
Ns = integrate.trapezoid(ys, x=xs, axis=1)
halfwaardes = halfwaarde_tijd(Ns) # [s]

# Plotting half-life v semi-major-axis
afstanden_plot = afstanden / stk.au # [au]
halfwaardes_plot = halfwaardes * 1/(365.25*24*3600) # [s] -> [jaar]

ax2.plot(afstanden_plot, halfwaardes_plot, label='Half-life')
ax2.set_xlabel('Distance to the sun [au]')
ax2.set_ylabel('Half-time [jaar]')
ax2.set_yscale('log')
ax2.set_title('Half-life of hydrogen  as a function of SMA')
ax2.legend()
ax2.grid()

'''2.7'''
masses =  np.linspace(0.1*stk.earth_mass,5*stk.earth_mass,100) # [kg]
density_earth = 5495 # [kg/m^3]
radii = (3*masses/(4*np.pi*density_earth))**(1/3) # [m]
escape_velocities = np.sqrt(2*stk.G*masses/radii) # [m/s]

# Plotting escape velocity v planet mass
fig7, (ax1,ax2) = plt.subplots(1,2, figsize=(12,6))
ax1.plot(masses/stk.earth_mass, escape_velocities, label='Escape Velocity')
ax1.set_xlabel('Mass of the planet [M⊕]')
ax1.set_ylabel('Escape Velocity [m/s]')
ax1.set_title('Escape Velocity as a function of Planet Mass')
ax1.legend()
ax1.grid()

T = T_planet(stk.au) # [K]

# Similiary as before, np vectorized would be preferable but not feasible.
Ns = []
for escape_vel in escape_velocities:
    v,f = MaxBolzd(gasses['H2'], T, 0.8*escape_vel)
    N = integrate.trapezoid(f, x=v)
    Ns.append(N)
halfwaardes = halfwaarde_tijd(np.array(Ns)) # [s]
halfwaardes_plot = halfwaardes * 1/(365.25*24*3600) # [s] -> [jaar]

# Plotting half-life v planet mass
ax2.plot(masses/stk.earth_mass, halfwaardes_plot, label='Half-life of hydrogen in the atmosphere')
ax2.set_xlabel('Mass of the planet [M⊕]')
ax2.set_ylabel('Half-life  [years]')
ax2.set_yscale('log')
ax2.set_title('Half-life of hydrogen in the atmosphere as a function of Planet Mass')
ax2.legend()
ax2.grid()

'''Settings for saving and showing figures'''
# Saving figures
save_fig = True
if(save_fig):
    folder = rf'year1_semester2\Planetenstelsels\Computerpractica\opdracht_3\plots'
    fig1.savefig(f'{folder}/center_of_mass_plot.png') # 1.3 
    fig2.savefig(f'{folder}/maxwell_boltzmann_gases.png') # 1.4
    fig3.savefig(f'{folder}/temperature_distribution.png') # 1.5
    fig4.savefig(f'{folder}/half_life_plot.png') # 2.2
    fig5.savefig(f'{folder}/maxwell_boltzmann_gases.png') # 2.3
    fig6.savefig(f'{folder}/temperature_half_life.png') # 2.6
    fig7.savefig(f'{folder}/escape_velocity_half_life.png') # 2.7

# Show all figures
show_figs = True
if(show_figs):
    plt.show()
