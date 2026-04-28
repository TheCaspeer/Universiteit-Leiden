import astropy.units as u
import numpy as np
import astropy as ap
import os
import matplotlib.pyplot as plt


curr_folder = os.path.dirname(os.path.abspath(__file__))
def read_file(filename: str):
    """
    Reads a text file and returns its contents as a dictionary.
    
    @param path (str): The relative path to the text file.
    
    @return dict: A dictionary containing the data from the text file.
    """''
    file = open(os.path.join(curr_folder,"Data",filename), 'r')
    data = np.loadtxt(file, skiprows=5,usecols=(1,2))
    return {
        'period': data[:, 0] * u.day,
        'mv': data[:, 1] * u.mag
    }

def cepheid_mag(period: u.Quantity, err_period: u.Quantity):
    """
    Calculate the absolute magnitude of a Cepheid variable star based on its period.

    
    @param period (float): The period of the Cepheid variable star in days.
    @param err_period (float): The uncertainty in the period.

    @return tuple: A tuple containing the absolute magnitude and its uncertainty.
    """
    # Using the period-luminosity relation for Cepheid variables
    period = period.value  
    err_period = err_period.value  
    M = -2.43 * (np.log10(period)-1) - 4.05
    M = M * u.mag  # Convert to magnitudes

    # Calculating the error
    err_M = 2.43/(period * np.log(10)) * err_period
    err_M = err_M * u.mag  # Convert to magnitudes

    return M, err_M

def distance_modulus(m:float, M:float,  err_m:float, err_M:float):
    """
    Calculate the distance modulus given the apparent magnitude and absolute magnitude.

    @param m (float): The apparent magnitude of the star.
    @param M (float): The absolute magnitude of the star.
    @param err_M (float): The uncertainty in the absolute magnitude.
    @param err_m (float): The uncertainty in the apparent magnitude.

    @return tuple: A tuple containing the distance and its uncertainty.
    """
    m = m.value
    M = M.value
    err_m = err_m.value
    err_M = err_M.value
    # Using: m-M = 5log10(d)-5
    d = 10**((m-M) / 5 + 1)
    d = d * u.pc  # Convert to parsecs

    # Calculating the error using error propagation
    err_d = ((np.log(10) / 5) * d.value * np.sqrt(err_M**2 + err_m**2)) * u.pc    
    return d,err_d


# Reading Data
dat_files = ["PS20D2NGC14251.DAT", "PS20D2NGC25411.DAT", "PS20D2NGC33511.DAT","PS20D2NGC36211.DAT", "PS20D2NGC43211.DAT","PS20D2NGC45481.DAT"]
galaxies = [read_file(dat_file) for dat_file in dat_files] # arr of dicts 
v_hels = {
    "NGC1425": 1512,
    "NGC2541": 559,
    "NGC3351": 778,
    "NGC3621": 805,
    "NGC4321": 1571,
    "NGC4548": 486
}


# Calculating absolute magnitudes, distances and corresponding errors for each cepheid in each galaxy
for galaxy in galaxies:
    # No error given assumes an error of 0
    abs_mag = cepheid_mag(galaxy['period'],0*u.day)[0]
    galaxy['abs_mags'] = abs_mag
    std_M = np.std(abs_mag)
    distances, err_distance = distance_modulus(galaxy['mv'], abs_mag, 0*u.mag, std_M*u.mag)
    galaxy['distances'], galaxy['err_distances'] = distances, err_distance


# Calculating mean distance and magnitudes for each galaxy
for index, galaxy in enumerate(galaxies):
    name = dat_files[index][6:-5] # Only keeps NGC#### from the filaname

    # Preventing astropy units from interfering 
    # TODO: Refactor to avoid this
    d_err = galaxy['err_distances'].value
    d = galaxy['distances'].value

    weights = 1 / d_err**2
    d_mean = np.sum(weights*d)/np.sum(weights)*u.pc
    d_mean_err = np.sqrt(1/np.sum(weights))*u.pc

    app_mag = np.mean(galaxy['mv'].value)
    app_mag_err = np.std(galaxy['mv'].value)

    # Writing to dictionary 
    galaxy['mean_distance'] = d_mean
    galaxy['mean_distance_err'] = d_mean_err
    galaxy['mean_app_mag'] = app_mag
    galaxy['mean_app_mag_err'] = app_mag_err
    galaxy['name'] = name
    galaxy['v_hel'] = v_hels[name]

lit_value = 70 * u.km / (u.s * u.Mpc) # Literature value for Hubble parameter, TODO: source

# Calculating Hubble parameter for each galaxy and its deviation from the literature value
hubble_params = []
for galaxy in galaxies:
    hubble_param = galaxy['v_hel']*(u.km/u.s) / galaxy['mean_distance'].to(u.Mpc)
    hubble_err = hubble_param * np.sqrt((galaxy['mean_distance_err']/galaxy['mean_distance'])**2)

    hubble_params.append(hubble_param.value)
    print(f"{galaxy['name']}: Hubble parameter = {hubble_param:.2f} ± {hubble_err:.2f}, Deviation from literature value = {(hubble_param - lit_value)/lit_value*100:.2f}%")

# Calculating the mean Hubble parameter of the galaxies
mean_hubble = np.mean(hubble_params)
std_hubble = np.std(hubble_params)
print(f"Mean Hubble parameter: {mean_hubble:.2f} ± {std_hubble:.2f}")


# Plotting the Hubble diagram and the residuals
fig1, ax1 = plt.subplots(figsize=(10, 6))
fig2, ax2 = plt.subplots(figsize=(10, 6))
for galaxy in galaxies:
    ax1.errorbar(galaxy['v_hel'], galaxy['mean_distance'].to(u.Mpc).value, yerr=galaxy['mean_distance_err'].to(u.Mpc).value, fmt='o', label=galaxy['name'])
    ax1.annotate(galaxy['name'], (galaxy['v_hel'], galaxy['mean_distance'].to(u.Mpc).value), textcoords="offset points", xytext=(0,17), ha='center')

    residual = galaxy['v_hel']-mean_hubble*galaxy['mean_distance'].to(u.Mpc).value
    ax2.errorbar(galaxy['v_hel'], residual, yerr=galaxy['mean_distance_err'].to(u.Mpc).value*mean_hubble, fmt='o', label=galaxy['name'])
    ax2.annotate(galaxy['name'], (galaxy['v_hel'], residual), textcoords="offset points", xytext=(0,17), ha='center')


ax1.set_ylabel('Distance [Mpc]')
ax1.set_xlabel('Recessional Velocity [km/s]')
ax1.set_title('Hubble Diagram')
ax1.grid(True, color='lightgray', linestyle='--', zorder=-1)
ax1.legend()

ax2.set_ylabel('Residual Velocity [km/s]')
ax2.set_xlabel('Recessional Velocity [km/s]')
ax2.set_title('Residuals from Hubble Law')
ax2.grid(True, color='lightgray', linestyle='--', zorder=-1)

plt.show()