import astropy as ap
from astropy import units as u
from astropy import constants as const
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
import astropy.coordinates as coord
from astropy import time as ap_time
from matplotlib.axes import Axes
import numpy as np
import matplotlib.pyplot as plt


location = EarthLocation(lat=52.160*u.deg, lon=4.497*u.deg, height=0*u.m) # Leiden
start_time = ap_time.Time('2023-02-01 19:00:00', scale='utc') # Time of observation
time_array = start_time + np.arange(0,14*24) * u.hour # Array of times at 1 hour intervals over 14 days

fig, ax = plt.subplots(figsize=(10, 6)) # Create a figure and axis for plotting

planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

def get_planet_position(planet_name, time):
    '''
    @param planet_name: string, name of the planet (e.g. 'Mars')
    @param time: astropy Time object

    @return: the position of the planet in the sky at the given time and location (location is defined globally)
    '''
    planet = coord.get_body(planet_name, time, location) # Get the position of the planet at the given time and location
    planet_coords = planet.transform_to(AltAz(obstime=time, location=location)) # Transform the planet's position to the AltAz frame for the given time and location
    return planet_coords.az.deg, planet_coords.alt.deg # Return the altitude and azimuth of the planet

def plot_planet_positions():
    '''
    Plots the positions of the planets in the sky over the given timespan at the given location (location and timespan are defined globally)
    '''
    for planet in planets:
        azimuths, altitudes = [], []
        planet_coords = coord.get_body(planet, time_array, location) # Get the position of the planet at the given times and location
        altaz = planet_coords.transform_to(AltAz(obstime=time_array, location=location)) # Transform the planet's position to the AltAz frame for the given times and location
        azimuths = altaz.az.deg # Get the azimuths of the planet
        altitudes = altaz.alt.deg # Get the altitudes of the planet
        ax.scatter(azimuths, altitudes, label=planet, s=2) # Plot the planet's position with a label

    ax.set_xlabel('Azimuth (degrees)')
    ax.set_ylabel('Altitude (degrees)')
    ax.set_title('Planet Positions Over Time')
    plt.legend()
    plt.show()

 

def main():
    plot_planet_positions()

if __name__ == "__main__":
    main()
