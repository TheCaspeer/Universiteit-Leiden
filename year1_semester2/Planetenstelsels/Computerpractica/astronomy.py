# sources for all constants and converion factors are from: Brightspace: 2526-S2 Planetenstelsels: Werkecollegse en practica: werkcollege1: Nuttige grootheden
# Constants
G = 6.668e-11  # m^3 kg^-1 s^-2 (Universal gravitational constant)
h = 6.625e-34  # J s (Planck's constant)
c = 2.998e8  # m/s (Speed of light in vacuum)
k = 1.3806e-23  # J/K (Boltzmann's constant)

# Conversion factors
au = 1.496e11  # m (Astronomical unit)
solar_mass = 1.989e30  # kg (Mass of the Sun)
solar_radius = 6.96e8  # m (Radius of the Sun)
earth_mass = 5.9736e24  # kg (Mass of the Earth)
earth_radius = 6.371e6  # m (Radius of the Earth)
jupiter_mass = 1.8986e27  # kg (Mass of Jupiter)
moon_mass = 7.3477e22  # kg (Mass of the Moon)
parsec = 3.086e16  # m (Parsec)
atomic_mass = 1.6605e-27  # kg (Atomic mass unit)

# Functions
def gravitational_force(m1: float, m2: float, r: float) -> float:
    """
    Calculate the gravitational force between two masses.
    
    @param m1: Mass of the first object in kg
    @param m2: Mass of the second object in kg
    @param r: Distance between the centers of the two masses in meters
    @return: Gravitational force in Newtons
    """
    force = G * m1 * m2 / r**2
    return force

def center_of_mass(m1: float, m2: float, r1: float, r2: float) -> float:
    """
    Calculate the center of mass of a two-body system.
    
    @param m1: Mass of the first object [kg]
    @param m2: Mass of the second object [kg]
    @param r1: Position of the first mass [m]
    @param r2: Position of the second mass [m]

    @return: Position of the center of mass [m]
    """
    com = (m1 * r1 + m2 * r2) / (m1 + m2)
    return com
