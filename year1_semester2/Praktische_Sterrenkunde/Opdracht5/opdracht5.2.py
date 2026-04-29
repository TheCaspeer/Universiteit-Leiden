from astropy import constants as const
from astropy import units as u 
import numpy as np
import os 
import matplotlib.pyplot as plt

def standard_model(z: float, H0: float, H0_err:float,  M: float = -19.3, q: float = -0.55):
    """
    Standard cosmological model for the apparent magnitude of a supernova as a function of redshift.
    
    @param z: Redshift of the supernova. (float)
    @param H0: Hubble constant in km/s/Mpc. (float)
    @param H0_err: Error in the Hubble constant. (float)
    @param M: Absolute magnitude of the supernova (default is -19.3) (float).
    @param q: Deceleration parameter (default is -0.55) (float). 
    @return: Apparent magnitude of the supernova.
    """
    m = 5 * np.log10( const.c.to(u.km/u.s).value / H0 * z *(1 + (1-q)/2* z)) + 25 + M 
    m_err = 5 / np.log(10) * (1 / H0) * H0_err * z * (1 + (1-q)/2* z) # Error propagation for the apparent magnitude
    return m, m_err

def constant_model(z:float,H0:float,H0_err:float,M:float=-19.3):
    """
    Constant expansion model for the apparent magnitude of a supernova as a function of redshift.
    
    @param z: Redshift of the supernova. (float)
    @param H0: Hubble constant in km/s/Mpc. (float)
    @param H0_err: Error in the Hubble constant. (float)
    @param M: Absolute magnitude of the supernova (default is -19.3) (float).
    @return: Apparent magnitude of the supernova.
    """
    m = 5 * np.log10( const.c.to(u.km/u.s).value / H0 * z) + 25 + M 
    m_err = 5 / np.log(10) * (1 / H0) * H0_err * z # Error propagation for the apparent magnitude
    return m, m_err


# Reading data
curr_folder = os.path.dirname(os.path.abspath(__file__))
data = np.loadtxt(os.path.join(curr_folder,"Data","redshift_app_mag_SAi.html"), skiprows=1, dtype=np.dtype([
                  ("name", "U50"),  ("zhel", float), ("mb", float), ("dmb", float)]), delimiter=None, usecols=(0, 2, 4, 5) )

data_near = data[data["zhel"] < 0.1] # Excluding stars with relativistic redshift

log_zhel_near = np.log10(data_near["zhel"]) 

# Fitting linear model to near data
fit_near, cov_near = np.polyfit(log_zhel_near, data_near["mb"], 1, cov=True) # First order polynomial fit (linear)

data_distant = data[data["zhel"] >= 0.1] # Excluding stars with non-relativistic redshift

q=-0.55
superlog_zhel = np.log10((1-q)/2*data_distant["zhel"]**2+data_distant["zhel"]) 

fit_distant, cov_distant = np.polyfit(superlog_zhel, data_distant["mb"], 1, cov=True) # First order polynomial fit (linear)

# Generating values for the fits:
x_plot = np.linspace(min(data["zhel"]), max(data["zhel"]), 250)
x_plot_near = np.log10(x_plot) 
y_near = np.polyval(fit_near, x_plot_near)

x_plot_distant = np.log10((1-q)/2*x_plot**2+x_plot)
y_distant = np.polyval(fit_distant, x_plot_distant)


# Plotting stars with non-relativistic redshift and overlaying the linear fit
fig1, ax1 = plt.subplots(figsize=(8,6), constrained_layout=True)
ax1.errorbar(log_zhel_near, data_near["mb"], yerr=data_near["dmb"], fmt='o', label="Near stars", ms=3, capsize=2)
ax1.plot(x_plot_near, y_near, label="Linear Fit (near)", color='red')
ax1.set_xlabel("Log Redshift [log z]")
ax1.set_ylabel("Apparent Magnitude [m]")
ax1.invert_yaxis() # Invert y-axis to have brighter stars at the top (magnitude has a reversed scale)
ax1.grid(True, color='lightgray', linestyle='--', zorder=-1, alpha=0.7)
ax1.legend()

fig1.suptitle("Apparent Magnitude vs Log Redshift for Near Stars (z < 0.1)")

# Plotting stars with relativistic redshift and overlaying the linear fit
fig2, (ax2,ax3) = plt.subplots(2,1, figsize=(8,12), constrained_layout=True)

ax2.errorbar(np.log(data_near["zhel"]), data_near["mb"], yerr=data_near["dmb"], fmt='o', label="Near stars", ms=3, capsize=2,zorder=-1)
ax2.plot(np.log(x_plot), y_near, label="Linear Fit (near)", color='pink',zorder=1)

ax2.errorbar(np.log(data_distant["zhel"]), data_distant["mb"], yerr=data_distant["dmb"], fmt='o', label="Distant stars", ms=3, capsize=2,zorder=-1)
ax2.plot(np.log(x_plot), y_distant, label="Linear Fit (distant)", color='green',zorder=1)

ax2.set_xlabel("Log Redshift [log z]")
ax2.set_ylabel("Apparent Magnitude [m]")
ax2.invert_yaxis() # Invert y-axis to have brighter stars at the top (magnitude has a reversed scale)

# Calculating Hubble parameters 
 
M = -19.3 # Absolute magnitude of any and all snIa 
b_near = fit_near[1]  # Intercept of the fit for distant stars
near_exponent = 10**((b_near-25-M)/5) # Calculate the exponent for the near stars s(seperate to prevent overflow errors)
H0_near = const.c.to(u.km/u.s).value / near_exponent
H0_near *= u.km/u.s/u.Mpc # Convert to km/s/Mpc

b_far = fit_distant[1]  # Intercept of the fit for distant stars
far_exponent = 10**((b_far-25-M)/5) # Calculate the exponent for the distant stars(seperate to prevent overflow errors)
H0_far =  const.c.to(u.km/u.s).value / far_exponent
H0_far *=  u.km/u.s/u.Mpc # Convert to km/s/Mpc

b_err_near = np.sqrt(cov_near[1,1]) # Error in the intercept for near stars
b_err_far = np.sqrt(cov_distant[1,1]) # Error in the intercept for distant stars

H0_near_err = H0_near * np.log(10) * b_err_near / 5 # Error propagation for Hubble parameter from near stars
H0_far_err = H0_far * np.log(10) * b_err_far / 5 # Error propagation for Hubble parameter from distant stars

print(f"Hubble parameter from near stars: {H0_near:.2f} ± {H0_near_err:.2f}")
print(f"Hubble parameter from distant stars: {H0_far:.2f} ± {H0_far_err:.2f}")

# Calculating expected values with 1sigma erros
z = np.linspace(min(data["zhel"]), max(data["zhel"]), 250)
standard_model_res = standard_model(z, H0_far.value, H0_far_err.value)
constant_model_res = constant_model(z, H0_near.value, H0_near_err.value)
ax2.plot(np.log(z), constant_model_res[0], label="Constant model", color='blue')
ax2.plot(np.log(z), standard_model_res[0], label="Standard model", color='orange')

ax2.fill_between(
    np.log(z),
    constant_model_res[0] - constant_model_res[1],
    constant_model_res[0] + constant_model_res[1],
    color='blue',
    alpha=0.2,
    label="Constant model 1σ error"
)
ax2.fill_between(
    np.log(z),
    standard_model_res[0] - standard_model_res[1],
    standard_model_res[0] + standard_model_res[1],
    color='orange',
    alpha=0.2,
    label="Standard model 1σ error"
)
ax2.axvline(np.log10(0.1), color='gray', linestyle='--', label="Relativistic Redshift Threshold")
ax2.grid(True, color='lightgray', linestyle='--', zorder=-1, alpha=0.7)
ax2.legend()



# Calculating expected magnitudes:
m_expected_const, m_expected_const_err = constant_model(data["zhel"], H0_near.value, H0_near_err.value)
m_expected_strd, m_expected_strd_err = standard_model(data["zhel"], H0_far.value, H0_far_err.value)

from numpy.lib import recfunctions as rfn

data = rfn.append_fields(
    data,
    ["m_expected_const", "m_expected_strd", "m_expected_const_err", "m_expected_strd_err"],
    [m_expected_const, m_expected_strd, m_expected_const_err, m_expected_strd_err],
    usemask=False
)

# Calculating residuals:
residual_const = data["mb"] - data["m_expected_const"]
residual_strd = data["mb"] - data["m_expected_strd"]

data = rfn.append_fields(
    data,
    ["residual_const", "residual_strd"],
    [residual_const, residual_strd],
    usemask=False
)

# Using either a regular dictionary or Pandas df would be cleaner, 
# but as this project was already done with np structured arrays it was not deemed necessary to refactor this to avoid this small block of code

# Plotting residuals:
ax3.errorbar(data["zhel"], data["residual_const"], yerr=data["m_expected_const_err"], fmt='o', label="Constant model", ms=3, capsize=2) # TODO: fix yerr
ax3.errorbar(data["zhel"], data["residual_strd"], yerr=data["m_expected_strd_err"], fmt='o', label="Standard model", ms=3, capsize=2) # TODO: fix yerr
ax3.axvline(0.1, color='gray', linestyle='--', label="Relativistic Redshift Threshold")
ax3.set_xlabel("Redshift [z]")
ax3.set_ylabel("Residual Apparent Magnitude [m]")
ax3.invert_yaxis() # Invert y-axis to have brighter stars at the top (magnitude has a reversed scale)
ax3.grid(True, color='lightgray', linestyle='--', zorder=-1, alpha=0.7)
ax3.legend(loc="lower right")

fig2.suptitle("Fits, Models, and Residuals for Near, and Distant Stars")

plt.show()

