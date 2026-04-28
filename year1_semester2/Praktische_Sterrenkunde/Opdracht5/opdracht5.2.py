from astropy import constants as const
from astropy import units as u 
import numpy as np
import os 
import matplotlib.pyplot as plt

H0 = 70*u.km/u.s/u.Mpc # Hubble constant, source TODO

# Reading data
curr_folder = os.path.dirname(os.path.abspath(__file__))
data = np.loadtxt(os.path.join(curr_folder,"Data","redshift_app_mag_SAi.html"), skiprows=1, dtype=np.dtype([
                  ("name", "U50"),  ("zhel", float), ("mb", float), ("dmb", float)]), delimiter=None, usecols=(0, 2, 4, 5) )

data_near = data[data["zhel"] < 0.1] # Excluding stars with relativistic redshift

log_zhel_near = np.log10(data_near["zhel"]) 

# Fitting linear model to near data
fit_near = np.polyfit(log_zhel_near, data_near["mb"], 1) # First order polynomial fit (linear)
x_near = np.linspace(log_zhel_near.min(), log_zhel_near.max(), 100)
y_far = np.polyval(fit_near, x_near)

# Plotting stars with non-relativistic redshift and overlaying the linear fit
fig1, ax1 = plt.subplots()
ax1.errorbar(log_zhel_near, data_near["mb"], yerr=data_near["dmb"], fmt='o', label="Near stars", ms=3, capsize=2)
ax1.plot(x_near, y_far, label="Linear Fit (near)", color='red')
ax1.set_xlabel("Log Redshift [log z]")
ax1.set_ylabel("Apparent Magnitude [m]")
ax1.invert_yaxis() # Invert y-axis to have brighter stars at the top (magnitude has a reversed scale)
ax1.legend()



distant_data = data[data["zhel"] >= 0.1] # Excluding stars with non-relativistic redshift

# Fitting linear model to distant data
log_zhel_distant = np.log10(distant_data["zhel"])
fit_distant = np.polyfit(log_zhel_distant, distant_data["mb"], 1) # First order polynomial fit (linear)
x_distant = np.linspace(log_zhel_distant.min(), log_zhel_distant.max(), 100)
y_distant = np.polyval(fit_distant, x_distant)

# Overlaying plot 1 onto plot 2 (relativistic redshift stars)
fig2, ax2 = plt.subplots()
ax2.errorbar(log_zhel_distant, distant_data["mb"], yerr=distant_data["dmb"], fmt='o', label="Distant stars", ms=2, capsize=1, zorder=-1)
ax2.plot(x_distant, y_distant, label="Linear Fit (distant)", color='red', zorder=1)

ax2.errorbar(log_zhel_near, data_near["mb"], yerr=data_near["dmb"], fmt='o', label="Near stars", ms=3, capsize=2, zorder=-1)
ax2.plot(x_near, y_far, label="Linear Fit (near)", color='blue', zorder=1)

ax2.set_xlabel("Log Redshift [log z]")
ax2.set_ylabel("Apparent Magnitude [m]")
ax2.invert_yaxis() # Invert y-axis to have brighter stars at the top (magnitude has a reversed scale)
ax2.legend()


plt.show()

