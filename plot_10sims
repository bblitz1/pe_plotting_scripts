import json
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_parameter(param_key, injected_val=None):
    num_sims = 30
    all_values = []

    for i in range(1, num_sims + 1):
        file_name = f"simulation_{i}.json"
        if not os.path.exists(file_name):
            print(f"Warning: {file_name} not found, skipping.")
            continue

        with open(file_name, 'r') as f:
            data = json.load(f)

        try:
            all_values.extend(data['posterior']['content'][param_key])
        except KeyError:
            print(f"Error: {param_key} not found in {file_name}, skipping.")
            continue

    if not all_values:
        print("No valid data found. Exiting.")
        return

    all_values = np.array(all_values)

    plt.hist(all_values, bins=30, density=True, color='skyblue', edgecolor='black', label='Data')

    if injected_val is not None:
        plt.axvline(injected_val, color='red', linestyle='--', label=f'Injected Value: {injected_val}')

    plt.xlabel(param_key)
    plt.ylabel('Frequency')
    plt.title(f'{param_key.capitalize()} Distribution for {num_sims} Simulations')
    plt.legend()

    filename = f"{param_key}_distribution_{num_sims}sims.png"
    plt.savefig(filename)
    print(f"Plot saved as {filename}")
    plt.close()

plot_parameter("inclination_angle", injected_val=5.0)
