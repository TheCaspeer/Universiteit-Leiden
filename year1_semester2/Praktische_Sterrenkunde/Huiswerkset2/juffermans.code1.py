import astropy as ap
from astropy import units as u
from astropy import constants as const
import numpy as np
import matplotlib.pyplot as plt


# Known values
d = 42 * u.uas # ring diameter
sigma_d = 3 * u.uas # uncertainty in ring diameter
D = 16.8 * u.megaparsec # distance to M87
sigma_D = 0.8 * u.megaparsec # uncertainty in distance to M87
theta_g = (d / (2 * 27**0.5)).to('', equivalencies=u.dimensionless_angles())
sigma_theta_g = (sigma_d / (2 * 27**0.5) ).to('', equivalencies=u.dimensionless_angles())

# Analytical approach
# the uncertainity in both c and G is regarded as 0 due to their high precision compared to the other values.
analytical_sigma_M = ( (const.c**2 * D / const.G  * sigma_theta_g )**2 + (theta_g * const.c**2 / const.G * sigma_D )**2 )**0.5
analytical_M = (theta_g * const.c**2 * D ) / const.G

# Monte Carlo approach
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Monte Carlo Simulations of Black Hole Mass Estimation')
N = 500 # number of Monte Carlo samples

def monte_carlo1_sample(d, sigma_d, D, sigma_D):
    d_sample = np.random.normal(d.value, sigma_d.value) * u.uas
    D_sample = np.random.normal(D.value, sigma_D.value) * u.Mpc
    theta_g_sample = (d_sample / (2 * 27**0.5)).to('', equivalencies=u.dimensionless_angles())
    M_sample = (theta_g_sample * const.c**2 * D_sample / const.G) 
    M_sample = M_sample.to(u.Msun)
    return M_sample

monte_carlo1_samples = u.Quantity([
    monte_carlo1_sample(d, sigma_d, D, sigma_D)
    for _ in range(N)
    ]) # solar masses
ax1.hist(monte_carlo1_samples, bins=15, alpha=0.7)
ax1.set_title('Histogram of Monte Carlo Samples of M')
mc1_M = monte_carlo1_samples.mean()
mc1_sigma_M = monte_carlo1_samples.std()

def monte_carlo2_sample(d, sigma_d, D, sigma_D):
    d_sample = np.random.normal(d.value, sigma_d.value) * u.uas
    d_sample = d_sample/np.random.uniform(9.6,11.5) # removing the artificial's effect
    D_sample = np.random.normal(D.value, sigma_D.value) * u.Mpc
    theta_g_sample = (d_sample / (2 * 27**0.5)).to('', equivalencies=u.dimensionless_angles())
    M_sample = (theta_g_sample * const.c**2 * D_sample / const.G) 
    M_sample = M_sample.to(u.Msun)
    return M_sample

monte_carlo2_samples = u.Quantity([
    monte_carlo2_sample(d, sigma_d, D, sigma_D)
    for _ in range(N)
    ]) # solar masses
ax2.hist(monte_carlo2_samples, bins=15, alpha=0.7)
ax2.set_title('Histogram of Monte Carlo Samples of M with added parameter alpha')
mc2_M = monte_carlo2_samples.mean()
mc2_sigma_M = monte_carlo2_samples.std()

# Formatting plots
for ax in [ax1, ax2]:
    ax.ticklabel_format(style='sci')
    ax.set_xscale('log')
    ax.grid(True, 'both')
    ax.set_xlabel('Mass (M_sun)') 
    ax.set_ylabel('Frequency')

print(f"The mass and error on the black hole are: M = {mc1_M:.2e} ± {mc1_sigma_M:.2e} (Monte Carlo approach without alpha)\n"
      f"M = {mc2_M:.2e} ± {mc2_sigma_M:.2e} (Monte Carlo approach with alpha)\n" 
      f"Analytical approach: M = {analytical_M.to(u.Msun):.2e} ± {analytical_sigma_M.to(u.Msun):.2e}")


parent_dic = rf'year1_semester2\Praktische_Sterrenkunde\Huiswerkset2'
plt.savefig(rf'{parent_dic}\monte_carlo_histograms.png')
plt.show()
