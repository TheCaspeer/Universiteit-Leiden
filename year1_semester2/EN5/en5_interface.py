# Authors:
# Bloom Berns (s4393724)
# Casper Juffermans (s4270118)
# Date: 15/03/2026


import en5analyse_raw as en5
import matplotlib.pyplot as plt
import numpy as np

def main():
    # File importing parameters
    file_loc = rf'year1_semester2\EN5\m_-1_spectro.csv' # CHANGE BEFORE USING
    file_type = '.csv'
    delimiter = ','

    # Data acquisition and handling
    x,y = get_data(file_loc, file_type, delimiter)
    y = clean_data(y)

    # Fit initial guess values 
    initial_mu = x[np.argmax(y)] # rough value, if need be can be manually ammended
    initial_sigma = 5   # manually change this value if you can not get a proper fit
    initial_amplitude = max(y) # rough value, if need be can be manually ammended

    # Fitting
    fit_info, error_info = get_fit(x,y, initial_mu, initial_sigma, initial_amplitude)
    print(f"Optimal parameters: mu = {fit_info['mu']}, sigma = {fit_info['sigma']}, amplitude = {fit_info['amplitude']}")
    mu = fit_info['mu']
    sigma = fit_info['sigma']
    amplitude = fit_info['amplitude']
    sigma_error = error_info['sigma_error']

    analysis(sigma, sigma_error)

    # Plotting (not necessary for data analysis)
    plot_fit(x,y,mu,sigma, amplitude)

def get_data(file_loc, file_type, delimiter):
    """
    @param file_loc: location of the file to be read
    @param file_type: type of the file to be read, supported types are: .txt, .csv, .xlsx
    @param delimiter: delimiter used in the file
    
     @return: x and y data read from the file
     """
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

def clean_data(y):
    """
    Normalizes and roughly removes noise from data

    @param y: array of y values to be cleaned
     
     @return: array of cleaned y values
     """
    y_normalized = y / np.sum(y) # normalizes the data
    y_denoised = y_normalized - np.min(y_normalized) # very roughly removing noise, this does not impact the parameters we look for but makes the fit easier
    return y_denoised

def get_fit(x,y, initial_mu, initial_sigma, initial_amplitude):
    """
    Fits data to a Gaussian function and returns the optimal parameters for the fit

    @param x: array of x values
    @param y: array of y values
    @param initial_mu: initial guess for the mean of the Gaussian
    @param initial_sigma: initial guess for the standard deviation of the Gaussian
    @param initial_amplitude: initial guess for the amplitude of the Gaussian
    
    @return: dictionary containing the optimal parameters for the Gaussian fit
     """
    if initial_mu == None or initial_sigma == None or initial_amplitude == None: 
        raise ValueError("Initial parameters for fitting have not been specified, please specify the initial parameters before running the code.")
        sys.exit(1)
    return en5.guass_fit(x, y, initial_mu, initial_sigma, initial_amplitude)

def plot_fit(x,y,mu,sigma, amplitude):
    """
    Plots the original data and the Gaussian fit

    @param x: array of x values
    @param y: array of y values
    @param mu: mean of the Gaussian fit
    @param sigma: standard deviation of the Gaussian fit
    @param amplitude: amplitude of the Gaussian fit
     
     @return: None
     """
    x_fit = np.linspace(min(x), max(x), 1000)
    y_fit = en5.gaussian(x_fit, mu, sigma,amplitude)
    
    plt.scatter(x, y, label='Data',s=0.5, color='red')
    plt.plot(x_fit, y_fit, label='Gaussian Fit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Gaussian Fit to Data')
    plt.legend()
    plt.grid()
    plt.show()


def analysis(sigma, sigma_error):
    '''
    @param sigma: standard deviation of the Gaussian fit, this is the parameter we are interested in for data analysis
    
    '''
    FWHM = 2 * (2 * np.log(2))**0.5 * sigma
    FWHM_error = 2 * (2 * np.log(2))**0.5 * sigma_error
    pixel_width = 3.75e-6 # [M]
    wavelength_width = FWHM * pixel_width # [M]
    wavelength_width_error = FWHM_error * pixel_width # [M]

    print(f"FWHM: {FWHM} ± {FWHM_error} pixels")
    print(f"Wavelength width: {wavelength_width} ± {wavelength_width_error} meters")

if __name__ == "__main__":
    main()