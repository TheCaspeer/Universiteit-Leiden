# Authors:
# Bloom Berns (s4393724)
# Casper Juffermans (s4270118)
# Date: 12/03/2026

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt 
import sys

# Reading file:
parent_dic = r'year1_semester2\EN5'
file_loc = rf"{parent_dic}\temp.temp" # change file loc before running
if (file_loc.endswith('.temp')):
    raise ValueError("File has not been changed from temporary value, please change the file location before running the code.")
    sys.exit(1)

# Gaussian function for fitting
def gaussian(x, mu, sigma):
    '''
    @param x: array of x values
    @param mu: mean of the Gaussian
    @param sigma: standard deviation of the Gaussian

    @return: array of Gaussian values corresponding to x
    '''
    
    return (1/(sigma * np.pi**0.5)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

# Fitting the function
initial_mu = 0.0 # Initial guess for mean
initial_sigma = 1.0 # Initial guess for standard deviation

try:
    popt, pcov = opt.curve_fit(gaussian, xdata, ydata,sigma=y_err, p0=[initial_mu, initial_sigma])

    optimal_values = {
        'mu': popt[0],
        'sigma': popt[1]
    }

    deviation = np.sqrt(np.diag(pcov))

except:
    raise ValueError("Curve fitting failed, trying again but excluding error data. Have you checked error data?")

try:
    popt, pcov = opt.curve_fit(gaussian, xdata, ydata, p0=[initial_mu, initial_sigma])

    optimal_values = {
        'mu': popt[0],
        'sigma': popt[1]
    }

    deviation = np.sqrt(np.diag(pcov))

except RuntimeError as e:
    print(f"Error during curve fitting: {e}")
    optimal_values = None
    deviation = None


# Calculating the lineair dispersion and its error
def lineair_dispersion(delta_lambda,delta_x):
    return delta_lambda/delta_x

def error_lineair(delta_lambda, delta_x, err_delta_lambda, err_delta_x):
    return np.sqrt((err_delta_lambda/delta_lambda)**2 + (err_delta_x/delta_x)**2)