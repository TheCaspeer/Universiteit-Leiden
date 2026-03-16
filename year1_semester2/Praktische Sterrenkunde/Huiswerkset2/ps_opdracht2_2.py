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
last_day = ap_time.Time('2026-12-31 23:59:59') # End date
days = np.arange((last_day - first_day).to(u.day).value) * u.day + first_day # Array of days in the year
spring = days[:len(days)//2] 
autumn = days[len(days)//2:]



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
    times = day + np.arange(0, 60*24, 5) * u.minute # Array of times during the day, every 5 minutes
    raise NotImplementedError("use nomimal noon instead!")
    # use nominaal noon instead of different times, based on longitude

    angles = get_angle(times) # Get the angles for each time
    return angles.max() # Return the maximum angle

def find_crossing(arr,season):
    def get_bool(day):
        return max_angle(day) >= theta_critical

    match season:
        case 'spring': 
            def is_crossing(day):
                return (get_bool(day) != get_bool(day - 1*u.day))
        case 'autumn':
            def is_crossing(day):
                return (get_bool(day) != get_bool(day + 1*u.day))
    
    low = 0
    high = len(arr) - 1
    while (low < high):
        mid = (low + high) // 2
        if is_crossing(arr[mid]):
            high = mid
        else:
            low = mid + 1
    return arr[low]



def main():
    spring_crossing = find_crossing(spring, 'spring')
    autumn_crossing = find_crossing(autumn, 'autumn')
    plot_angles()

    print(f"Spring crossing: {spring_crossing.strftime('%Y-%m-%d')}")
    print(f"Autumn crossing: {autumn_crossing.strftime('%Y-%m-%d')}")
            
if __name__ == "__main__":
    main()






    
