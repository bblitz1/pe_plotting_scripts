import argparse
import json
import matplotlib.pyplot as plt

def plot_parameter(data_file, param_key, injected_val=None, sim_number=None):
    # Load data from JSON file
    with open(data_file, 'r') as f:
        data = json.load(f)

    # Extract parameter values based on the key provided
    parameter_values = data['posterior']['content'][param_key]

    # Plot histogram of the parameter values
    plt.hist(parameter_values, bins=30, density=True, color='skyblue', edgecolor='black', label='Data')

    # If an injected value is provided, add a vertical line to indicate it
    if injected_val is not None:
        plt.axvline(injected_val, color='red', linestyle='--', label=f'Injected Value: {injected_val}')

    #Label
    plt.xlabel(param_key)
    plt.ylabel('Frequency')
    plt.title(f'{param_key.capitalize()} Distribution - Simulation {sim_number}')
    plt.legend()

    filename = f"{param_key}_distribution_sim{sim_number}.png"
    plt.savefig(filename)
    print(f"Plot saved as {filename}")
    plt.close()

parser = argparse.ArgumentParser(description="Plot parameter distribution from multiple JSON files.")

parser.add_argument('--num_sims', type=int, choices=[10, 30, 50, 100], help="Number of simulations to run.")
parser.add_argument('--param', type=str, help="Parameter key to extract from JSON.")
parser.add_argument('--injected', type=float, default=None, help="Optional injected value to highlight.")
args = parser.parse_args()


for i in range(1, args.num_sims + 1):
    json_file = f"simulation_{i}.json"  
    try:
        plot_parameter(json_file, args.param, args.injected, sim_number=i)
    except FileNotFoundError:
        print(f"Warning: {json_file} not found, skipping.")
