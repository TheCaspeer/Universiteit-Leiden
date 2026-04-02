# Authors:
# Bloom Berns (s4393724)
# Casper Juffermans (s4270118)
# Date: 15/03/2026

import numpy as np
import scipy.optimize as opt 
import sys


def read_file(file_loc,delimiter,file_type):
    """
    @param file_loc: location of the file to be read
    @param delimiter: delimiter used in the file
    @param file_type: type of the file to be read, supported types are: .txt, .csv, .xlsx
     
     @return: x and y data read from the file
     """
    if file_type not in ['.txt', '.csv', '.xlsx']:
        raise ValueError("Unsupported file type. Supported types are: .txt, .csv, .xlsx")
        sys.exit(1)
    try:
        if file_type == '.txt':
            data = np.loadtxt(file_loc, delimiter=delimiter, unpack=True)
        elif file_type == '.csv':
            data = np.genfromtxt(file_loc, delimiter=delimiter, skip_header=1, unpack=True)
        elif file_type == '.xlsx':
            import pandas as pd
            data = pd.read_excel(file_loc).values
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    return data


# Gaussian function for fitting
def gaussian(x, mu, sigma, A):
    '''
    @param x: array of x values
    @param mu: mean of the Gaussian
    @param sigma: standard deviation of the Gaussian
    @param A: amplitude of the Gaussian

    @return: array of Gaussian values corresponding to x
    '''
    
    return  A*(1/(sigma * (2*np.pi)**0.5)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

def guass_fit(xdata, ydata, initial_mu, initial_sigma, init_amplitude):
    """
    @param xdata: array of x values
    @param ydata: array of y values
    @param initial_mu: initial guess for the mean of the Gaussian
    @param initial_sigma: initial guess for the standard deviation of the Gaussian
    @param init_amplitude: initial guess for the amplitude of the Gaussian
    
    @return: dictionary containing the optimal parameters for the Gaussian fit
    """
    try: 
        popt, pcov = opt.curve_fit(gaussian, xdata, ydata, p0=[initial_mu, initial_sigma, init_amplitude])
        optimal_values = {
            'mu': popt[0],
            'sigma': popt[1],
            'amplitude': popt[2]
        }

        error_info = {
            'mu_error': np.sqrt(pcov[0][0]),
            'sigma_error': np.sqrt(pcov[1][1]),
            'amplitude_error': np.sqrt(pcov[2][2])
        }
        return optimal_values, error_info
    
    except RuntimeError as e:
        print(f"Error during curve fitting: {e}")
        sys.exit(1)
    