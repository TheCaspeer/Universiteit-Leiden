import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

"""
Code for EN1
This code loads a data file and calculates its standard deviation on a specified column

For EN1: you do not need to understand this code. Only adjust the following parameters:
(>>1) The file you would like to fit, and which column you want to use.

These adjustment points are also denoted in the code with (>>x)
"""


"""
(>>1) Load the file you want to process by changing the string between the quotes.
Change which (two) columns to use by adjusting the 'usecols' argument. 
Note: Column '0' is the first column and column '1' is the second!
"""


target_file = "data/gaussian_data.csv"
print(f"Read the file: {target_file}")
for column in np.loadtxt(target_file, delimiter=",", unpack=True):
    # prints all the columns np.loadtxt found
    print(f"found column with shape: {np.shape(column)}")


y_data = np.loadtxt(target_file, delimiter=",", usecols=(1), unpack=True)  # usecols = 1 means: use the SECOND column!
y_mean = np.mean(y_data)
y_standard_deviation = np.std(y_data, ddof=1)


print(f"Selected column has mean {y_mean}")
print(f"Selected column has standard deviation {y_standard_deviation}")
