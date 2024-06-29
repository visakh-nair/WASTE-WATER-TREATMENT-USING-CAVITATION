# Calculation Model Used:
# Cavitation Number - Euler's Equation
# Water Density - IAPWS Formulation 1995 equation
# Vapor Pressure - Antoine equation of water vapor

# Assumptions:
# 1. Cavitation will incept at cavitation number of 1 (i.e, unity)
# 2. Pure water is considered

# Note:
# Install Prettytable Library before running this program by executing following command: pip install prettytable
# Under General Public License (GNU)
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Constants
p1 = 1  # downstream pressure in bar
Cv = 100  # flow coefficient of the valve
T = float(input("Enter the temperature in °C: "))

# Tables created for printing various data
table1 = PrettyTable(['Flow Rate (LPH)', 'Cavitation Number', 'Velocity (m/s)'])
table2 = PrettyTable(['Temperature (°C)', 'Flow Rate (LPH)', 'Velocity (m/s)', 'Cavitation Number', 'Density (kg/m3)', 'Vapor Pressure (Bar)'])

# Calculation of vapor pressure of water
# Antoine equation of water vapor
Av, B, C = 8.07131, 1730.63, 233.426  # Antoine constants for water
pv = (10 ** (Av - (B / (T + C))))/750.1  # vapor pressure of water in bar at input temperature

# rho = 1000  # density of water in kg/m^3 at 15°C
# IAPWS Formulation 1995 equation
rho = 999.84847 + 6.337563e-2 * T - 8.523829e-3 * T**2 + 6.943248e-5 * T**3 - 3.821216e-7 * T**4

# Taking input for flow rate and cross-sectional area
Q = float(input("Enter the flow rate in LPH: "))
A = float(input("Enter the cross-sectional area in m^2: "))

# Calculation of Velocity
Q_m3s = Q / 3600 / 1000  # convert flow rate from LPH to m^3/s
v = Q_m3s / A  # calculate velocity in m/s

# Calculation of Cavitation number
sigma_c = ((p1 - pv)*100000) / (0.5 * rho * v**2)

print('-' * 75)
print("REPORT")
print('-' * 75)

print(f"Velocity at orifice plate: {v:.2f} m/s")
print(f"The vapor pressure of water at {T}°C: {pv:.4f} bar")
print(f"Cavitation number: {sigma_c:.4f}")

for Q in range(10, 1000, 10):
    # Calculation of Velocity
    Q_m3s = Q / 3600 / 1000  # convert flow rate from LPH to m^3/s
    v = Q_m3s / A  # calculate velocity in m/s

    # Calculation of Cavitation number
    sigma_c = ((p1 - pv)*100000) / (0.5 * rho * v**2)
    
    if sigma_c < 1:
        print(f"Cavitation will occur at a flow rate of {Q} LPH at velocity of {v:.2f} m/s.")
        break


# Calculation of Cavitation number
def calc_cavitation_number(Q,A):
    
    # Calculation of Velocity
    Q_m3s = Q / 3600 / 1000  # convert flow rate from LPH to m^3/s
    v = Q_m3s / A  # calculate velocity in m/s

    # Calculation of Cavitation number
    sigma_c = ((p1 - pv)*100000) / (0.5 * rho * v**2)
    return sigma_c

# Print table of LPH vs Cavitation number vs Velocity (m/s)
sigma_c_list = []
Q_range = []
V_range = []

for Q in range(10, 1010, 10):
    
    Q_m3s = Q / 3600 / 1000  # convert flow rate from LPH to m^3/s
    v = Q_m3s / A  # calculate velocity in m/s
    V_range.append(v)
    sigma_c = calc_cavitation_number(Q,A)
    table1.add_row([Q, round(sigma_c, 4) , round(v, 4)])
    if sigma_c < 2:
        sigma_c_list.append(sigma_c)
        Q_range.append(Q)
print(table1)

print("\nTable of cavitation inception at different temperature")
# Print table of cavitation inception with respect to temperature
cvt_list = []
vt_list = []
for Tv in range(1, 100, 1):
    
    pvt = ((10 ** (Av - (B / (Tv + C))))/750.1)
    rhot = 999.84847 + 6.337563e-2 * Tv - 8.523829e-3 * Tv**2 + 6.943248e-5 * Tv**3 - 3.821216e-7 * Tv**4
    
    for Qt in range(10, 1000, 10):
        # Calculation of Velocity
        Q_m3st = Qt / 3600 / 1000  # convert flow rate from LPH to m^3/s
        vt = Q_m3st / A  # calculate velocity in m/s

        # Calculation of Cavitation number
        cvt = ((p1 - pvt)*100000) / (0.5 * rhot * vt**2)
        
        if cvt < 1:
            vt_list.append(vt)
            table2.add_row([Tv , Qt , round(vt, 4) , round(cvt, 4) , round(rhot, 4) , round(pvt, 4)])
            break        
print(table2)    


# Plot the cavitation number vs flow rate
plt.plot(Q_range, sigma_c_list)
plt.xlabel("Flow Rate (LPH)")
plt.ylabel("Cavitation Number")
plt.title("Cavitation Number vs Flow Rate")
plt.show()

# Plot the Temperature vs Inception Velocity
TempG = np.arange(1, 100, 1)
plt.plot(TempG, vt_list)
plt.xlabel("Temperature (°C)")
plt.ylabel("Inception Velocity (m/s)")
plt.title("Temperature vs Inception Velocity")
plt.show()

# Plot the velocity vs flow rate
Q_velo = np.arange(10, 1010, 10)
plt.plot(Q_velo, V_range)
plt.xlabel("Flow Rate (LPH)")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity vs Flow Rate")
plt.show()



