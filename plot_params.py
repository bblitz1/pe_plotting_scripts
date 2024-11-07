import json
import matplotlib.pyplot as plt

def plot_parameter(data_file, param_key, injected_val=None):
    with open(data_file, 'r') as f:
        data = json.load(f)

    parameter_values = data['posterior']['content'][param_key]

    plt.hist(parameter_values, bins=30, color='skyblue', edgecolor='black', label='Data')

    if injected_val is not None:
        plt.axvline(injected_val, color='red', linestyle='--', label=f'Injected Value: {injected_val}')

    plt.xlabel(param_key)
    plt.ylabel('Frequency')
    plt.title(f'{param_key.capitalize()} Distribution')

    plt.legend()

    plt.savefig(f"{param_key}_distribution.png")
    print(f"Plot saved as {param_key}_distribution.png")
    plt.close()  




