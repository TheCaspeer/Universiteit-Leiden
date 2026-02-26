import astronomy as stk

parent_dic = 'year2_semester2\Planetenstelsels\Computerpractica'

# Opdracht 4
height_iss = 407e3 # (m)
mass_iss = 1 # considering F is a linear function of the ISS's mass, and A = F/m, we can set m = 1 kg for simplicity
moon_mass = 7.342e22 # kg
moon_radius = 1737e3 # m
moon_distance = 384400e3 # m

acc1 = stk.gravitational_force(mass_iss, stk.earth_mass, stk.earth_radius + height_iss) # m/s^2
acc2 = stk.gravitational_force(mass_iss, moon_mass, moon_distance+moon_radius-height_iss) #m/s^2
acc3 = stk.gravitational_force(mass_iss, stk.solar_mass, stk.au-height_iss) # m/s^2

print(f'The accelerations are as follows: \n' f'Due to the Earth: {acc1:.2e} m/s^2 \n' f'Due to the Moon: {acc2:.2e} m/s^2 \n' f'Due to the Sun: {acc3:.2e} m/s^2 ')

# Opdracht 5 & 6
from astropy.table import Table
import matplotlib.pyplot as plt

# Reading the data from the file
planeten = Table.read(f'{parent_dic}\planeet-gegevens.ecsv', format='ascii.ecsv')
planeten.add_index('name')
planeten[0]['name']


# Plotting
fig, ax = plt.subplots(figsize=(12, 8)) 
y_axis = planeten['density']
x_axis = planeten['Rmean']

# Labeling planetss
for index, item in enumerate(x_axis):
    x_offset = 0.03 * item
    y_offset = 0.03 * y_axis[index]
    location = (item + x_offset, y_axis[index] + y_offset)
    plt.annotate(planeten[index]['name'], xy=location, xytext=(0, 10), textcoords='offset points')

# Plotting refrence densities
water_density = 1 # g/cm^3 (liquid water), #https://www.usgs.gov/water-science-school/science/water-density
plt.axhline(y=water_density, color='r', linestyle='--', label='Density of liquid water')
rock_density = 2.65 # g/cm^3 (typical density of rocks) #https://www.thoughtco.com/densities-of-common-rocks-and-minerals-1439119
plt.axhline(y=rock_density, color='g', linestyle='--', label='Density of typical rock')
iron_density = 6.98 # g/cm^3 (density of iron) #https://periodictable.com/Properties/A/LiquidDensity.al.html
plt.axhline(y=iron_density, color='b', linestyle='--', label='Density of liquid iron')

plt.scatter(x_axis, y_axis)
plt.xlabel('Radius (km)')  
plt.ylabel('Density (g/cm^3)') 
plt.title('Density of Planets versus their Radius') #
plt.xscale('log')
plt.yscale('log')

# Manually adding tick to the plot
ax.set_xticks([3e3, 5e3, 1e4, 2e4, 3e4, 4e4, 6e4, 8e4])
ax.set_yticks([0.5, 1, 2, 5, 10])
import matplotlib.ticker as ticker
ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())

plt.grid()
plt.legend()
plt.show()

# Opdracht 7
acc_string = 'The graviational accelerations of the planets are as follows: \n'
for planet in planeten:
   # considering F is a linear function of the smaller mass, and A = F/m, we can set m = 1 kg for simplicity
   acc = stk.gravitational_force(1,planet['mass']*1e24,planet['Rmean']*1e3) # converting Rmean from km to m, convering mass from 10^24 kg to kg
   acc_string += f'{planet["name"]}: {acc:.2f} m/s^2 \n'

print(acc_string)







