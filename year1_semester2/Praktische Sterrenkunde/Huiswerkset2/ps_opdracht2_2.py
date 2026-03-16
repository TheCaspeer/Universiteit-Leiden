import astropy as ap
from astropy import units as u
from astropy import constants as const
from astropy.coordinates import EarthLocation, AltAz, SkyCoord, get_sun
from astropy import time as ap_time
import numpy as np
import matplotlib.pyplot as plt

# Input parameters
fence_distance = 4 * u.meter
fence_height = 2 * u.meter

# Half-garden angle
theta_critical = np.arctan(fence_height/ (fence_distance/2)).to(u.deg)

location = EarthLocation(lat=52.160*u.deg, lon=4.497*u.deg, height=0*u.m) #

first_day = ap_time.Time('2026-01-01 00:00:00') # Start date
last_day = ap_time.Time('2026-12-31 00:00:00') # End date
days = first_day + np.arange(int((last_day - first_day).to_value(u.day)) + 1) * u.day # Inclusive array of days in the year
spring = days[0:len(days)//2] # First half of the year
autumn = days[len(days)//2:] # Second half of the year

# Nominal noon (UTC)
# Local solar noon occurs near 12:00 local solar time.
# Converting to UTC for east-positive longitude gives ~12h - longitude_offset.
longitude_offset = location.lon / (360 * u.deg) * (24 * u.hour)
def get_nominal_noon(day):
    return day + 12 * u.hour - longitude_offset

def get_angle(time):
    '''
    @param time: astropy Time object

    @return: the angle the sun makes with the horizontal plane at the given time and location (location is defined globally)
    '''
    AltAz_frame = AltAz(obstime=time, location=location) # Define the AltAz frame for the given time and location
    sun_altaz = get_sun(time).transform_to(AltAz_frame) # The suns position, relative to the given frame
    return sun_altaz.alt # Return the altitude of the sun, which is the angle it makes with the horizontal plan

def max_angle(day):
    '''
    @param day: astropy Time object representing a single day

    @return: the maximum angle the sun makes with the horizontal plane during that day at the given location (location is defined globally)
    '''
    nominal_noon = get_nominal_noon(day)

    angle = get_angle(nominal_noon) # Get the angles for the nomimal noon
    return angle # Return the maximum angle

def find_crossings(day_array,season):
    '''
    @param day_array: array of astropy Time objects representing days
    @param season: string, either 'spring' or 'autumn', indicating which half of the year to search for crossings

    @return: the days on which the sun angle crosses the critical angle (theta_critical) in spring and autumn
    '''

    match season:
        case 'spring':
            def crosses_critical(day):
                return (max_angle(day) != max_angle(day-1))
        case 'autumn':
            def crosses_critical(day):
                return (max_angle(day) != max_angle(day+1))

    low = 0
    high = len(day_array) - 1
    while low <= high:
        mid = (low + high) // 2
        if (crosses_critical(day_array[mid])):
            return day_array[mid]
        else: 
            if max_angle(day_array[mid]) < theta_critical:
                low = mid + 1
            else:
                high = mid - 1

def plot_angles():
    angles = [max_angle(day) for day in days]
    angle_values = u.Quantity(angles).to_value(u.deg)
    plt.plot(days.to_datetime(), angle_values, label='Max Sun Angle')
    plt.axhline(theta_critical.to_value(u.deg), color='r', linestyle='--', label='Critical Angle')
    plt.xlabel('Date')
    plt.ylabel('Maximum Sun Angle (degrees)')
    plt.title('Maximum Sun Angle Throughout the Year')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('sun_angle_plot.png') # Save the plot as a PNG file
    plt.show()


def main():
    spring_crossing, autumn_crossing = find_crossings(spring, 'spring'), find_crossings(autumn, 'autumn')
    print(f"Spring crossing: {spring_crossing.strftime('%Y-%m-%d')}")
    print(f"Autumn crossing: {autumn_crossing.strftime('%Y-%m-%d')}")

    plot_angles()
            
if __name__ == "__main__":
    main()






    
