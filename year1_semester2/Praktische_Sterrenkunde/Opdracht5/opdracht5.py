import astropy.units as u
import numpy as np
import astropy as ap
import os


curr_folder = os.path.dirname(os.path.abspath(__file__))


def read_txt(path: String):
    """
    Reads a text file and returns its contents as a dictionary.
    
    @param path (str): The relative path to the text file.
    
    @return dict: A dictionary containing the data from the text file.
    """''
    path = rf"{curr_folder}/data/{path}"
    data = np.genfromtxt(
        path,
        dtype=None,
        encoding="utf-8",
        delimiter=None  # <-- THIS is the key
    )
    data = dict(zip(data.dtype.names, data.T)) # Convert the structured array to a dictionary
    return data

def cepheid_mag(period: u.Quantity, err_period: u.Quantity):
    """
    Calculate the absolute magnitude of a Cepheid variable star based on its period.

    
    @param period (float): The period of the Cepheid variable star in days.
    @param err_period (float): The uncertainty in the period.

    @return tuple: A tuple containing the absolute magnitude and its uncertainty.
    """
    # Using the period-luminosity relation for Cepheid variables
    period = period.to(u.day).value  # Ensure the period is in days
    err_period = err_period.to(u.day).value  # Ensure the error in period is in days
    M = -2.43 * (np.log10(period)-1) - 4.05
    M = M.to(u.mag)  # Convert to magnitudes

    # Calculating the error
    err_M = 2.43/(period * np.log(10)) * err_period
    err_M = err_M.to(u.mag)  # Convert to magnitudes

    return M, err_M

def distance_modulus(m:float, M:float, err_M:float, err_m:float):
    """
    Calculate the distance modulus given the apparent magnitude and absolute magnitude.

    @param m (float): The apparent magnitude of the star.
    @param M (float): The absolute magnitude of the star.
    @param err_M (float): The uncertainty in the absolute magnitude.
    @param err_m (float): The uncertainty in the apparent magnitude.

    @return tuple: A tuple containing the distance and its uncertainty.
    """
    # Using: m-M = 5log10(d)-5
    d = 10**((m-M) / 5 + 1)
    d = d * u.pc  # Convert to parsecs

    # Calculating the error using error propagation
    err_d = (np.ln(10) * 10**(m-M)/ 5+1) * np.sqrt(err_M**2 + err_m**2)
    err_d = err_d.to(u.pc)  # Convert to parsecs
    
    return d,err_d

def hubble_law(distance: u.Quantity, H0=70 * u.km / (u.s * u.Mpc)):
    """
    This function calculates the recessional velocity of a galaxy based on its distance using Hubble's Law.
    
    @param distance (Mpc): The distance to the galaxy in megaparsecs (Mpc).
    @param H0 (km/s/Mpc): The Hubble constant in km/s/Mpc. Default is 70 km/s/Mpc.
    
    @return velocity (km/s): The recessional velocity of the galaxy in km/s.
    """
    H0 = H0.to(u.km / (u.s * u.Mpc))  # Ensure Hubble constant is in km/s/Mpc
    distance = distance.to(u.Mpc)  # Ensure distance is in Mpc
    velocity = H0 * distance
    return velocity

def reverse_hubble_law(velocity: u.Quantity, H0=70 * u.km / (u.s * u.Mpc)):
    """
    This function calculates the distance to a galaxy based on its recessional velocity using the reverse of Hubble's Law.
    
    @param velocity (km/s): The recessional velocity of the galaxy in km/s.
    @param H0 (km/s/Mpc): The Hubble constant in km/s/Mpc. Default is 70 km/s/Mpc.
    
    @return distance (Mpc): The distance to the galaxy in megaparsecs (Mpc).
    """
    velocity = velocity.to(u.km / u.s)  # Ensure velocity is in km/s
    H0 = H0.to(u.km / (u.s * u.Mpc))  # Ensure Hubble constant is in km/s/Mpc
    distance = velocity / H0
    return distance


