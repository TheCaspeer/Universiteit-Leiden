# sources for all constants and converion factors are from: Brightspace: 2526-S2 Planetenstelsels: Werkecollegse en practica: werkcollege1: Nuttige grootheden
# Constants
G = 6.668e-11  # m^3 kg^-1 s^-2 (Universal gravitational constant)
h = 6.625e-34  # J s (Planck's constant)
c = 2.998e8  # m/s (Speed of light in vacuum)

# Conversion factors
au = 1.496e11  # m (Astronomical unit)
solar_mass = 1.989e30  # kg (Mass of the Sun)
solar_radius = 6.96e8  # m (Radius of the Sun)
earth_mass = 5.9736e24  # kg (Mass of the Earth)
earth_radius = 6.371e6  # m (Radius of the Earth)
jupiter_mass = 1.8986e27  # kg (Mass of Jupiter)
parsec = 3.086e16  # m (Parsec)

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


