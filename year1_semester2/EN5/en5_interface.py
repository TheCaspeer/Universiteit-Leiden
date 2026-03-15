# Authors:
# Bloom Berns (s4393724)
# Casper Juffermans (s4270118)
# Date: 15/03/2026


import en5analyse_raw as en5
import matplotlib.pyplot as plt
import numpy as np


# File importing parameters
file_loc = r'temp' # CHANGE BEFORE USING
file_types = ['.txt', '.csv', '.xlsx']
file_type = None # CHANGE BEFORE USING
delimiters = [',', ';', '\t']
delimiter = None # CHANGE BEFORE USING

# Fitting parameters
initial_mu = None # Initial guess for mean # CHANGE BEFORE USING
initial_sigma = None # Initial guess for standard deviation # CHANGE BEFORE USING


def main():
    x,y,y_err = get_data()
    fit_info = get_fit(x,y,y_err)
    print(f"Optimal parameters: mu = {fit_info['mu']}, sigma = {fit_info['sigma']}")
    mu = fit_info['mu']
    sigma = fit_info['sigma']
    plot_fit(x,y,y_err,mu,sigma)

def get_data():
    if file_loc == r'temp':
        raise ValueError("File location has not been changed from temporary value, please change the file location before running the code.")
        sys.exit(1)
    if file_type == None:
        raise ValueError("File type has not been specified, please specify the file type before running the code.")
        sys.exit(1)
    if delimiter == None:
        raise ValueError("Delimiter has not been specified, please specify the delimiter before running the code.")
        sys.exit(1)
    
    x,y = en5.read_file(file_loc, delimiter, file_type)
    return x,y

def get_fit(x,y,y_err):
    if initial_mu == None or initial_sigma == None:
        raise ValueError("Initial parameters for fitting have not been specified, please specify the initial parameters before running the code.")
        sys.exit(1)
    return en5.guass_fit(x, y, y_err, initial_mu, initial_sigma)

def plot_fit(x,y,y_err,mu,sigma):
    x_fit = np.linspace(min(x), max(x), 1000)
    y_fit = en5.gaussian(x_fit, mu, sigma)
    
    plt.errorbar(x, y, yerr=y_err, fmt='o', label='Data')
    plt.plot(x_fit, y_fit, label='Gaussian Fit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Gaussian Fit to Data')
    plt.legend()
    plt.grid()
    plt.show()
    