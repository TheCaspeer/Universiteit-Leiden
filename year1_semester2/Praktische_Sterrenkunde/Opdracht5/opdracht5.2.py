from astropy import constants as const
from astropy import units as u 
import numpy as np
import os 
import matplotlib.pyplot as plt

H0 = 70*u.km/u.s/u.Mpc

def get_m(M,z):
    '''
    Calculate the apparent magnitude of a star given its absolute magnitude and redshift.
    
    @param M (float): The absolute magnitude of the star.
    @param z (float): The redshift of the star.

    @return m (float): The apparent magnitude of the star.
    '''
    
    v = z * const.c
    d = v / H0

    m = 5 * np.log10(d.to(u.pc).value) - 5 + M.value
    m = m * u.mag  # Convert to magnitudes

    return m

def get_M(m,m_err,z,z_err):
    v = z * const.c
    v_err = z_err * const.c
    d = v / H0
    d_err = v_err / H0

    M = m - 5 * np.log10(d.to(u.pc).value) + 5
    M_err = np.sqrt(m_err**2 + (5 * d_err / (d * np.log(10)))**2)


    return M, M_err

curr_folder = os.path.dirname(os.path.abspath(__file__))

data = np.loadtxt(os.path.join(curr_folder,"Data","redshift_app_mag_SAi.html"), skiprows=1, dtype=np.dtype([
                  ("name", "U50"),  ("zhel", float), ("mb", float), ("dmb", float)]), delimiter=None, usecols=(0, 2, 4, 5) )

data_near = data[data["zhel"] < 0.1]

fig1, ax1 = plt.subplots()

log_zhel = np.log10(data_near["zhel"])

fit = np.polyfit(log_zhel, data_near["mb"], 1)
x_fit = np.linspace(log_zhel.min(), log_zhel.max(), 100)
y_fit = np.polyval(fit, x_fit)

ax1.errorbar(log_zhel, data_near["mb"], yerr=data_near["dmb"], fmt='o', label="Data", ms=3, capsize=2)
ax1.plot(x_fit, y_fit, label="Linear Fit", color='red')
ax1.set_xlabel("Log Redshift (log z)")
ax1.set_ylabel("Apparent Magnitude (m)")
ax1.invert_yaxis()
ax1.legend()


distant_data = data[data["zhel"] >= 0.1]

fig2, ax2 = plt.subplots()
log_zhel_distant = np.log10(distant_data["zhel"])
fit_distant = np.polyfit(log_zhel_distant, distant_data["mb"], 1)
x_fit_distant = np.linspace(log_zhel_distant.min(), log_zhel_distant.max(), 100)
y_fit_distant = np.polyval(fit_distant, x_fit_distant)
ax2.errorbar(log_zhel_distant, distant_data["mb"], yerr=distant_data["dmb"], fmt='o', label="Distant stars", ms=2, capsize=1, zorder=-1)
ax2.plot(x_fit_distant, y_fit_distant, label="Linear Fit (distant)", color='red', zorder=1)

ax2.errorbar(log_zhel, data_near["mb"], yerr=data_near["dmb"], fmt='o', label="Near stars", ms=3, capsize=2, zorder=-1)
ax2.plot(x_fit, y_fit, label="Linear Fit (near)", color='blue', zorder=1)
         
ax2.set_xlabel("Log Redshift (log z)")
ax2.set_ylabel("Apparent Magnitude (m)")
ax2.invert_yaxis()
ax2.legend()
plt.show()

