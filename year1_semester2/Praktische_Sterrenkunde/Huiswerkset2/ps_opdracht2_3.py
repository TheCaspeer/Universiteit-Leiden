import astropy as ap
from astropy import units as u
from astropy import constants as const
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
import astropy.coordinates as coord
from astropy import time as ap_time
from matplotlib.axes import Axes
import numpy as np
import matplotlib.pyplot as plt

# Starting parameters
location = EarthLocation(lat=52.160*u.deg, lon=4.497*u.deg, height=0*u.m) # Leiden
start_time = ap_time.Time('2023-02-01 19:00:00', scale='utc') # Time of observation
time_array = start_time + np.arange(0,14*1) * u.day # Array at 1 day intervals over 14 days (observation period)

fig, ax = plt.subplots(figsize=(10, 6)) # Create a figure and axis for plotting

planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'] # Planets in the solar system, excluding earth

def get_planet_position(planet_name, time):
    '''
    @param planet_name: string, name of the planet
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
        ax.plot(azimuths, altitudes, label=planet, lw=2) # Plot the planet's position with a label

    ax.set_xlabel('Azimuth (degrees)')
    ax.set_ylabel('Altitude (degrees)')
    ax.set_title(rf"Planet Positions from {start_time.strftime('%Y-%m-%d')} to {time_array[-1].strftime('%Y-%m-%d')} at {location.lat.deg:.2f}°N, {location.lon.deg:.2f}°E")
    ax.legend(loc='upper right')
    ranges = (ax.get_xlim(), ax.get_ylim()) # Get the ranges of the x and y axes for later use in filtering constellations
    return ranges 

def read_constellations(filename, ranges):
    '''
    Reads the constellation data from a file and returns a dictionary of constellation names and their corresponding coordinates.

    @param filename: string, name of the file containing the constellation data
    @param ranges: tuple, the range of azimuth and altitude values

    @return: dictionary of constellation names and their corresponding coordinates
    '''
    constellation_abbreviation, azimuth, altitude, pen_down = np.loadtxt(filename,
                                                                                usecols=(1,2,3,4),
                                                                                dtype=[('abbr','U5'), ('az',float), ('alt',float), ('pen',int)],
                                                                                unpack=True) # Load the constellation data from the file
    # location is never used, thusly not loaded 
    class Constellation:
        def __init__(self, abbreviation, azimuth, altitude, pen_down):
            self.abbreviation = abbreviation 
            self.azimuth = azimuth
            self.altitude = altitude
            self.pen_down = pen_down
    
    constellations = []
    for const in np.unique(constellation_abbreviation):
        const_data = np.where(constellation_abbreviation == const)
        alt = altitude[const_data]
        az = azimuth[const_data]
        # Saves all constellations who have at least one point within the range.
        if (np.max(az) >= ranges[0][0] 
            and np.min(az) <= ranges[0][1] 
            and np.max(alt) >= ranges[1][0]  
            and np.min(alt) <= ranges[1][1]): 
            constellations.append(Constellation(const, azimuth[const_data], altitude[const_data], pen_down[const_data])) # Create a Constellation object and add it to the list of constellations

    return constellations


def plot_constellations(constellations):
    '''
    Plots the constellations on the same plot as the planets.

    @param constellations: list of Constellation objects, containing the data for the constellations to be plotted
    '''
    for constellation in constellations:
        for i in range(len(constellation.azimuth)-1): # Loop through the points of the constellation, except for the last point``
            if (constellation.pen_down[i] == 1 and constellation.pen_down[i+1] == 1): # Checks if you need to draw a line between the points
                point1 = {'x': constellation.azimuth[i], 'y':constellation.altitude[i]}
                point2 = {'x': constellation.azimuth[i+1], 'y':constellation.altitude[i+1]}
                if (abs(point1['x'] - point2['x']) < 180): # Check if the line does not cross the 0/360 degree boundary
                    ax.plot([point1['x'], point2['x']], [point1['y'], point2['y']], color='lightblue', linewidth=0.5, zorder=-2) # Plot a line between the current point and the next point
                    # it could be coded that the line goes from (a->360) and (0->b), however this would not be in the domain of the plot, thusly not necessary to implement.

        for i in range(len(constellation.azimuth)): #  Draws the individual stars 
            ax.scatter(constellation.azimuth[i], constellation.altitude[i], color='lightblue', s=10, zorder=-1) # Plot the current point as a scatter point
def main():
    ranges = plot_planet_positions() # Plotting planet positions and getting the ranges of the planets positions
    # Ranges can also be set manually, use format ranges = ((min_az, max_az), (min_alt, max_alt)) if you want to include more constellations or exclude some of the planets.

    parent_dic = rf'year1_semester2\Praktische_Sterrenkunde\Huiswerkset2'
    file_name = rf'HuibConstel_Rukl.txt'
    constellation_data = read_constellations(rf'{parent_dic}\{file_name}',ranges)
    plot_constellations(constellation_data)

    # Set the x/y-axis limits to the ranges of azimuth/altitude values (preventing constellations from stretching out the view)
    plt.xlim(ranges[0]) 
    plt.ylim(ranges[1]) 
    
    plt.savefig(rf'{parent_dic}\planet_constellations_plot.pdf') # Save the plot as a PDF file
    plt.show()

if __name__ == "__main__":
    main()
