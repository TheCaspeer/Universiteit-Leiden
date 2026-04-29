from astropy import constants as const
from astropy import units as u 
import numpy as np
import os 
import matplotlib.pyplot as plt

H0 = 70*u.km/u.s/u.Mpc # Hubble constant, source TODO

def standard_model(z: float, H0: float, M: float = -19.3, q: float = -0.55):
    """
    Standard cosmological model for the apparent magnitude of a supernova as a function of redshift.
    
    @param z: Redshift of the supernova. (float)
    @param H0: Hubble constant in km/s/Mpc. (float)
    @param M: Absolute magnitude of the supernova (default is -19.3) (float).
    @param q: Deceleration parameter (default is -0.55) (float). 
    @return: Apparent magnitude of the supernova.
    """
    m = M + 5 * np.log10(const.c.to(u.km/u.s).value * z / H0) + 25 + 5 * np.log10((1-q)/2*z**2+z) # TODO: check
    return m


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


data_distant = data[data["zhel"] >= 0.1] # Excluding stars with non-relativistic redshift

q=-0.55
superlog_zhel = np.log10((1-q)/2*data_distant["zhel"]**2+data_distant["zhel"]) 
log_distant_zhel = np.log10(data_distant["zhel"]) # To ensure the x-axis is consistent for the plot

fit_distant = np.polyfit(superlog_zhel, data_distant["mb"], 1) # First order polynomial fit (linear)
x_distant = np.linspace(log_distant_zhel.min(), log_distant_zhel.max(), 100)
y_distant = np.polyval(fit_distant, x_distant)

# Plotting stars with relativistic redshift and overlaying the linear fit
fig2, ax2 = plt.subplots()

ax2.errorbar(log_zhel_near, data_near["mb"], yerr=data_near["dmb"], fmt='o', label="Near stars", ms=3, capsize=2,zorder=-1)
ax2.plot(x_near, y_far, label="Linear Fit (near)", color='red',zorder=1)

ax2.errorbar(superlog_zhel, data_distant["mb"], yerr=data_distant["dmb"], fmt='o', label="Distant stars", ms=3, capsize=2,zorder=-1)
ax2.plot(x_distant, y_distant, label="Linear Fit (distant)", color='green',zorder=1)

ax2.set_xlabel("Log Redshift [log z]")
ax2.set_ylabel("Apparent Magnitude [m]")
ax2.invert_yaxis() # Invert y-axis to have brighter stars at the top (magnitude has a reversed scale)
ax2.legend()




# Calculating Hubble parameters 
 
M = -19.3 # Absolute magnitude of any and all snIa (source TODO)

b_near = fit_near[1]  # Intercept of the fit for distant stars
near_exponent = 10**((b_near-25-M)/5) # Calculate the exponent for the near stars s(seperate to prevent overflow errors)
H0_near = const.c.to(u.km/u.s).value / near_exponent
H0_near *= u.km/u.s/u.Mpc # Convert to km/s/Mpc

b_far = fit_distant[1]  # Intercept of the fit for distant stars
far_exponent = 10**((b_far-25-M)/5) # Calculate the exponent for the distant stars(seperate to prevent overflow errors)
H0_far =  const.c.to(u.km/u.s).value / far_exponent
H0_far *=  u.km/u.s/u.Mpc # Convert to km/s/Mpc


print(f"Hubble parameter from near stars: {H0_near:.2f}")
print(f"Hubble parameter from distant stars: {H0_far:.2f}")




# plt.show()

