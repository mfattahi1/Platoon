# Simple simulation of a vehicle platoon with an attacker

import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_vehicles = 5  # Number of cars in the platoon
ts = 0.1  # Time step (seconds)
sim_time = 30  # Total simulation time (seconds)
kp = 0.2  # Proportional gain
kd = 0.7  # Derivative gain
headway = 0.35  # Desired headway (seconds)

# Time steps
steps = int(sim_time / ts)

# Initialize arrays for positions, velocities, and accelerations
positions = np.zeros((num_vehicles, steps))
velocities = np.zeros((num_vehicles, steps))
accelerations = np.zeros((num_vehicles, steps))

# Define the lead vehicle's acceleration profile
lead_acc = np.zeros(steps)
lead_acc[:50] = 2  # Accelerate for 5 seconds
lead_acc[150:200] = -2  # Decelerate for 5 seconds

# Simulate the platoon
for t in range(1, steps):
    for i in range(num_vehicles):
        if i == 0:
            # Lead vehicle dynamics
            accelerations[i, t] = lead_acc[t]
            velocities[i, t] = velocities[i, t - 1] + accelerations[i, t] * ts
            positions[i, t] = positions[i, t - 1] + velocities[i, t] * ts
        elif i == 3:  # Attacker (Vehicle 4)
            # Stop-and-Go Attack: Alternating acceleration and braking
            if (t // int(2 / ts)) % 2 == 0:  # Switch every 2 seconds
                accelerations[i, t] = 5  # Sudden acceleration
            else:
                accelerations[i, t] = -5  # Sudden braking
            velocities[i, t] = velocities[i, t - 1] + accelerations[i, t] * ts
            positions[i, t] = positions[i, t - 1] + velocities[i, t] * ts
        else:
            # Following vehicles use proportional-derivative control
            spacing_error = positions[i - 1, t - 1] - positions[i, t - 1] - headway * velocities[i, t - 1]
            velocity_error = velocities[i - 1, t - 1] - velocities[i, t - 1]
            accelerations[i, t] = kp * spacing_error + kd * velocity_error
            velocities[i, t] = velocities[i, t - 1] + accelerations[i, t] * ts
            positions[i, t] = positions[i, t - 1] + velocities[i, t] * ts


# Introduce an attacker (Vehicle 4) braking suddenly
attack_start = 100  # Attack starts at t = 10 seconds
for t in range(attack_start, steps):
    accelerations[3, t] = -5  # Aggressive braking

# Plot the positions of the vehicles
plt.figure(figsize=(10, 6))
for i in range(num_vehicles):
    plt.plot(np.arange(0, sim_time, ts), positions[i, :], label=f'Car {i + 1}')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Vehicle Positions in a Platoon')
plt.legend()
plt.grid()
plt.show()