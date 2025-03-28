import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

def plot_parameter(data_files, param_key, injected_val=None):
    all_values = []

    for data_file in data_files:
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            all_values.extend(data['posterior']['content'][param_key])
        except FileNotFoundError:
            print(f"Warning: {data_file} not found, skipping.")

    if not all_values:
        print("No valid data found. Exiting.")
        return

    all_values = np.array(all_values)

    plt.hist(all_values, bins=30, density=True, color='skyblue', edgecolor='black', label='Data')

    if injected_val is not None:
        plt.axvline(injected_val, color='red', linestyle='--', label=f'Injected Value: {injected_val}')

    plt.xlabel(param_key)
    plt.ylabel('Frequency')
    plt.title(f'{param_key.capitalize()} Distribution for {len(data_files)} Simulations')
    plt.legend()

    filename = f"{param_key}_distribution_{len(data_files)}sims.png"
    plt.savefig(filename)
    print(f"Plot saved as {filename}")
    plt.close()

parser = argparse.ArgumentParser(description="Plot parameter distribution from multiple JSON files.")
parser.add_argument('--param', type=str, required=True, help="Parameter key to extract from JSON.")
parser.add_argument('--injected', type=float, default=None, help="Optional injected value to highlight.")
parser.add_argument('--simulations', type=int, choices=[10, 30, 50, 100], required=True, help="Number of simulations to include.")

args = parser.parse_args()

data_files = [f"simulation_{i}.json" for i in range(1, args.simulations + 1)]

plot_parameter(data_files, args.param, args.injected)
