import astropy as ap
from astropy import units as u
from astropy import constants as const
import numpy as np


# Known values
d = 42 * u.uas # ring diameter
sigma_d = 3 * u.uas # uncertainty in ring diameter
D = 16.8 * u.megaparsec # distance to M87
sigma_D = 0.8 * u.megaparsec # uncertainty in distance to M87
theta_g = (d / (2 * 27**0.5)).to('', equivalencies=u.dimensionless_angles())
sigma_theta_g = (sigma_d / (2 * 27**0.5) ).to('', equivalencies=u.dimensionless_angles())
sigma_theta_g = sigma_theta_g.to('', equivalencies=u.dimensionless_angles())
# Analytical approach
# the uncertainity in both c and G is regarded as 0 due to their high precision compared to the other values.
analytical_sigma_M = ( (const.c**2 * D / const.G  * sigma_theta_g )**2 + (theta_g * const.c**2 / const.G * sigma_D )**2 )**0.5
analytical_M = (theta_g * const.c**2 * D ) / const.G

# Monte Carlo approach
N = 500
M_samples = []

for i in range(N):
    d_sample = np.random.normal(d.value, sigma_d.value) * u.uas
    D_sample = np.random.normal(D.value, sigma_D.value) * u.Mpc
    theta_g_sample = (d_sample / (2 * 27**0.5)).to('', equivalencies=u.dimensionless_angles())
    M_sample = (theta_g_sample * const.c**2 * D_sample / const.G)
    M_samples.append(M_sample)

M_samples = u.Quantity(M_samples)
mc_M = M_samples.mean()
mc_sigma_M = M_samples.std()

print(f"Analytical approach: M = {analytical_M.to(u.Msun):.2e} ± {analytical_sigma_M.to(u.Msun):.2e}")
print(f"Monte Carlo approach: M = {mc_M.to(u.Msun):.2e} ± {mc_sigma_M.to(u.Msun):.2e}")
