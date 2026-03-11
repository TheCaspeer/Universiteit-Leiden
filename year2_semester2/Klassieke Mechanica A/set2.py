import numpy as np
import matplotlib.pyplot as plt

x1,x2 = np.meshgrid(np.linspace(-5,5,20), np.linspace(-5,5,20)) 
values = {
    'alpha': 0,
    'beta': 0.5,
    'gamma': 1
}

# The force is given by -(4alpha x^3, 3 beta y^2, 2 gamma z). Considering alpha = 0, we shall be plotting the force in the yz-plane.

y = 3* values['beta'] * x1**2
z = 2* values['gamma'] * x2

plt.quiver(x1, x2, y,z)
plt.title('Force field in the yz-plane')
plt.xlabel('y ->')
plt.ylabel('z ->')
plt.grid()
plt.show()
