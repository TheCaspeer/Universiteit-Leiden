import astropy.units as u
import numpy as np
import astropy as ap

def cepheid_mag(period, err_period):
    """
    Calculate the absolute magnitude of a Cepheid variable star based on its period.

    Parameters:
    period (float): The period of the Cepheid variable star in days.
    err_period (float): The uncertainty in the period.

    Returns:
    float: The absolute magnitude of the Cepheid variable star.
    float: The uncertainty in the absolute magnitude.
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

def distance_modulus(m, M, err_M, err_m):
    """
    Calculate the distance modulus given the apparent magnitude and absolute magnitude.

    Parameters:
    m (float): The apparent magnitude of the star.
    M (float): The absolute magnitude of the star.
    err_M (float): The uncertainty in the absolute magnitude.
    err_m (float): The uncertainty in the apparent magnitude.


    Returns:
    float: The distance in parsecs.
    """
    # Using: m-M = 5log10(d)-5
    d = 10**((m-M) / 5 + 1)
    d = d * u.pc  # Convert to parsecs

    # Calculating the error using error propagation
    err_d = (np.ln(10) * 10**(m-M)/ 5+1) * np.sqrt(err_M**2 + err_m**2)
    err_d = err_d.to(u.pc)  # Convert to parsecs
    
    return d,err_d
