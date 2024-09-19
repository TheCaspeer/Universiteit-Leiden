import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

"""
Code for EN1
This code loads a data file, slices it, performs a fit on the first two columns of the data.

For EN1: you do not need to understand this code. Only adjust the following parameters:
(>>0) The functions (models) that are available to fit.
(>>1) The file you would like to fit
(>>2) Select which data (rows) you want use
(>>3) The formula to calculate the physical quantity you are interested in. In this case: humidity.
      also, the formula for calculating the error for the voltage and corresponding error in humidity.  
(>>4) The type function you would like to fit and the initial (guess) parameters.

These adjustment points are also denoted in the code with (>>x)
"""


"""
Define the functions you want to fit. Code is not set to fit linear_model.
arguments:  'x' independent variable (first!), 'a', 'b', fit-parameters.
"""


def quadratic_model(x, a, b, c):
    return a * x**2 + b * x + c


def exponential_model(x, a, b, c):
    return np.exp(a * x + b) + c


def sine_model(x, a, b, c):
    return a * np.sin(b * (x - c))


def gaussian_model(x, a, b, c):
    return a * np.exp(-b * (x - c) ** 2)


"""
(>>1) Load the file you want to process by changing the string between the quotes.
"""
target_file = "data/sine_data.csv"
print(f"Read the file: {target_file}")
for column in np.loadtxt(target_file, delimiter=",", unpack=True):
    print(f"found column with shape: {np.shape(column)}")  # prints all the columns np.loadtxt found


"""
(>>2) Select the data you want to display and perform a fit on. This process is called 'slicing'.
Change the variables below to select a start and end row of your data. These must be whole numbers!
"""

slice_start = 0
slice_end = 10000  # data with fewer dan 10000 datapoints is always fully included.
time_unsliced, voltage_unsliced = np.loadtxt(target_file, delimiter=",", usecols=(0, 1), unpack=True)
time, voltage = (
    time_unsliced[slice_start:slice_end],
    voltage_unsliced[slice_start:slice_end],
)


"""
(>>3) Calculate the (WRONG!) resistance and error from the voltage using an incorrect formula. Adjust this!
Also, calculate the phyical quantity (grootheid) our transducer measures.
Some examples; division: voltage/1000, exponentiation: voltage**4, addition: voltage + 4
"""
voltage_error = 0.02 * np.abs(voltage) # arbitrary, used abs. because error cannot be negative.
resistance = 1.0 * voltage   # arbitrary
resistance_error = 1.0*voltage_error  # arbitrary

humidity = resistance + 0.0001 * np.exp(resistance)  # wrong
humidity_error = resistance_error  # wrong


"""
(>>4)  The function you want to fit and the initial parameters ('guesses') for fit in the same order 
as the function arguments. Set values for the computers initial values for a, b, c.
These should be somewhat close to the actual data, otherwise the computer won't find a good fit.
"""
model_chosen = sine_model  # make the fitting function *itself* a variable so we don't have to repeat it later.
a_initial_guess = 2
b_initial_guess = 3.14
c_initial_guess = 1.7


"""
Perform the fit using the 'linear_model', and using 'time'-data as the x-axis and 'voltage'-data as the y-axis.
Store the optimal parameters in the 'param' array and co-variances in the pcov array.
documentation for curve_fit: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
"""
initial_fit_parameters = [a_initial_guess, b_initial_guess, c_initial_guess]
param, pcov = curve_fit(
    model_chosen,
    time,
    humidity,
    sigma=humidity_error,
    absolute_sigma=True,
    p0=initial_fit_parameters,
    maxfev=5000,
)

a_fit, b_fit, c_fit = param[0], param[1], param[2]  # extract the fitted parameters
a_std, b_std, c_std = (
    np.sqrt(pcov[0, 0]),
    np.sqrt(pcov[1, 1]),
    np.sqrt(pcov[2, 2]),
)  # calculate the errors from the diagonals


# Print the optimal values to the screen. Note: these are not (correctly) rounded!
print("The unrounded optimal value for parameter 'a' is: ", a_fit, "+/-", a_std)
print("The unrounded optimal value for parameter 'b' is: ", b_fit, "+/-", b_std)
print("The unrounded optimal value for parameter 'c' is: ", c_fit, "+/-", b_std)


"""
Check your result with a plot: make sure that the fit is good!
Make a figure. Plot the data using errorbars. Plot the fitted function on top.
"""
plt.figure(dpi=300, figsize=(8, 5))
plt.errorbar(
    time,
    humidity,
    yerr=humidity_error,
    fmt="o",
    markersize=2,
    capsize=3,
    label="Humidity sensor 1",
)  # Plots the data with errorbars
plt.plot(
    time,
    model_chosen(time, a_fit, b_fit, c_fit),
    linestyle="dashed",
    label="fit: Humidity sensor 1",
)  # Plot the fit as a line
# plt.plot(time, linear_model(time, a_initial_guess, b_initial_guess, c_initial_guess), linestyle='dashed', label="guess Resistor 1")  # plots the fit as a line.

plt.title("Humidity as measured by a humidity sensor over time")  # add a title to our graph
plt.xlabel("time (s)")
plt.ylabel("Humidity (Number of water particles) ")

plt.grid()  # show a grid
plt.minorticks_on()  # show minor ticks
plt.legend()  # make a legend using the labels from the plot command


# Uncomment below to change the maximum and minimum axis values for x and y.
# plt.xlim(0, 0.012)  # The range of the x axis
# plt.ylim(0, 5)  # The range of the y axis

# Uncomment below to scale the y-axis logarithmically
# plt.semilogy()

# Uncomment to save the figure with the name 
# plt.savefig('filename_here.pdf')

plt.show()  # Shows the figure
