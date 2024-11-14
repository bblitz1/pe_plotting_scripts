import argparse
import json
import matplotlib.pyplot as plt

def plot_parameter(data_file, param_key, injected_val=None):
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

    # Labeling the plot
    plt.xlabel(param_key)
    plt.ylabel('Frequency')
    plt.title(f'{param_key.capitalize()} Distribution')
    plt.legend()

    # Save the plot to a file
    plt.savefig(f"{param_key}_distribution.png")
    print(f"Plot saved as {param_key}_distribution.png")
    plt.close()

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Plot parameter distribution from a JSON file.")
    
    # Add arguments
    parser.add_argument('input', type=str, help="Path to the JSON file.")
    parser.add_argument('param', type=str, help="Parameter key to extract from JSON.")
    parser.add_argument('--injected', type=float, default=None, help="Optional injected value to highlight.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the plotting function with parsed arguments
    plot_parameter(args.input, args.param, args.injected)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
