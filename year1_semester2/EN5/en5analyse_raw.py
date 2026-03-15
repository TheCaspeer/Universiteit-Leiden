# Authors:
# Bloom Berns (s4393724)
# Casper Juffermans (s4270118)
# Date: 15/03/2026

import numpy as np
import scipy.optimize as opt 
import sys


def read_file(file_loc,delimiter,file_type):
    if file_type not in ['.txt', '.csv', '.xlsx']:
        raise ValueError("Unsupported file type. Supported types are: .txt, .csv, .xlsx")
        sys.exit(1)
    try:
        if file_type == '.txt':
            data = np.loadtxt(file_loc, delimiter=delimiter)
        elif file_type == '.csv':
            data = np.genfromtxt(file_loc, delimiter=delimiter, skip_header=1)
        elif file_type == '.xlsx':
            import pandas as pd
            data = pd.read_excel(file_loc).values
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    return data


# Gaussian function for fitting
def gaussian(x, mu, sigma):
    '''
    @param x: array of x values
    @param mu: mean of the Gaussian
    @param sigma: standard deviation of the Gaussian

    @return: array of Gaussian values corresponding to x
    '''
    
    return (1/(sigma * np.pi**0.5)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

def guass_fit(xdata, ydata, y_err, initial_mu, initial_sigma):
    try: 
        popt = opt.curve_fit(gaussian, xdata, ydata, sigma=y_err, p0=[initial_mu, initial_sigma])

        optimal_values = {
            'mu': popt[0],
            'sigma': popt[1]
        }
        return optimal_values
    
    except RuntimeError as e:
        print(f"Error during curve fitting: {e}")
        sys.exit(1)
    