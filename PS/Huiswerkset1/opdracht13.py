import numpy as np

# Known parameters
mean = 64.65 # in milliarcseconds (mas) 
standard_deviation = 0.12 # (mas) 
rel_error = [0.01,0.02,0.05,0.2,0.5] # relative error in parallax measurement 
sample_size = 100

# Simulate parallax measurements with the given mean and standard deviation
p_1 = np.array([]) # list of parallax measurements (mas)
for i in range(0,sample_size):
    measurement = np.random.normal(mean, standard_deviation) # simulate parallax measurement
    p_1 = np.append(p_1, measurement)

# Simulate parallax measurements with relative errors
p_r = [[],[],[],[],[]] # list of parallax measurements with relative errors (mas)
for index, error in enumerate(rel_error):
    for i in range(0,sample_size):
        measurement = np.random.rand()*mean*error # simulate parallax measurement with relative error
        p_r[index].append(measurement)
p_r = np.array(p_r) # convert list to numpy array for easier computations


# Calculating mean parallax and error for datasets
par_1 = np.mean(p_1)
err_par_1 = np.std(p_1)
d_1 = np.round(1/(par_1*1e-3),2) # distance in parsecs (pc)
err_d1 = np.round((err_par_1/par_1)*d_1,2) # error in distance (pc)

par_arr = np.mean(p_r, axis=1)
err_par_arr = np.std(p_r, axis=1)
d_arr = np.round(1/(par_arr*1e-3),2) # distance in parsecs (pc)
err_d_arr = np.round((err_par_arr/par_arr)*d_arr,2) # error in distance (pc)

table = [
    f"{d_1} {err_d1}\n",
    f"{d_arr[0]} {err_d_arr[0]}\n",
    f"{d_arr[1]} {err_d_arr[1]}\n",
    f"{d_arr[2]} {err_d_arr[2]}\n",
    f"{d_arr[3]} {err_d_arr[3]}\n",
    f"{d_arr[4]} {err_d_arr[4]}\n"]

print(f"Value (pc),     Error (pc)\n"
      f"-----------------------------\n"
      f"{"".join(table)}")
