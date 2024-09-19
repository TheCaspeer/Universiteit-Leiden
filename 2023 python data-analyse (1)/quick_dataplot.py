import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

"""
Code for EN1
This code plots a data file of choice for quick inspection

For EN1: you do not need to understand this code. Only adjust the following parameters:
(>>1) The file you would like to fit, and which columns you want to use.
(>>2) The axis sizes and names

These adjustment points are also denoted in the code with (>>x)
"""


"""
(>>1) Load the file you want to process by changing the string between the quotes.
Change which (two) columns to use by adjusting the 'usecols' argument. Column '0' is the first column!
"""

target_file = "data/gaussian_data.csv"
print(f'Read the file: {target_file}')
for column in np.loadtxt(target_file, delimiter=",", unpack=True):
    # prints all the columns np.loadtxt found
    print(f"found column with shape: {np.shape(column)}")


x_data, y_data = np.loadtxt(target_file, delimiter=",", usecols=(0, 1), unpack=True)


plt.figure(dpi=300, figsize=(8, 5))
plt.scatter(x_data, y_data, s=2, label="data name here")  # Plots the data as a scatter


"""
(>>2) Axis labels and axis limits.
"""
# add a title to our graph
plt.title("quick data inspection plot of example data")
plt.xlabel("x-axis (unit)")
plt.ylabel("y-axis (unit) ")

# Uncomment below to change the maximum and minimum axis values for x and y.
# plt.xlim(0, 0.012)  # The range of the x axis
# plt.ylim(0, 5)  # The range of the y axis

plt.grid()  # show a grid
plt.minorticks_on()  # show minor ticks
plt.legend()  # make a legend using the labels from
plt.show()  # Shows the figure
