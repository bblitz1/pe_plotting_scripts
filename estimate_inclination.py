from emcee_funcs import log_likelihood
from emcee_funcs import emcee_trial
from wave_funcs import damped_wave
from plotting_funcs import PlottingWrapper
import numpy as np
import emcee
import matplotlib.pyplot as plt

def generate_noise(signal, snr=1.0):
    signal_power = np.sum(np.square(signal)) / len(signal)
    noise_power = signal_power / snr
    noise = np.sqrt(noise_power) * np.random.randn(len(signal))
    return noise

def simulate_data():
    REAL_AMPLITUDE = 7.0
    REAL_DAMPING = 0.3
    REAL_ANGULAR_FREQ = 1.2
    REAL_THETA = np.array([REAL_AMPLITUDE, REAL_DAMPING, REAL_ANGULAR_FREQ])

    RANGES = np.array(
        [
            [0.1, 10.0],  # Amplitude (A)
            [0.1, 3.0],   # Damping (b)
            [0.1, 10.0],  # Angular frequency (ω)
        ]
    )

    DATA_STEPS = 1000
    TIMESPAN = 20
    WAVE_KWARGS = {"phase": 0.0, "seconds": TIMESPAN, "steps": DATA_STEPS}

    time, real_wave = damped_wave(REAL_THETA, return_time=True, **WAVE_KWARGS)
    noise = generate_noise(real_wave, snr=1.0)
    yerr = 1 / 1.0  # SNR = 1.0, so yerr = 1/SNR

    return real_wave, noise, RANGES, WAVE_KWARGS, REAL_THETA, yerr

def estimate_inclination():
    simulated_data, noise, ranges, wave_kwargs, real_theta, yerr = simulate_data()

    NDIM = 3
    NWALKERS = 50
    NUM_ITERATIONS = 10000

    p0 = [simulated_data + 1e-4 * np.random.randn(len(simulated_data)) for i in range(NWALKERS)]

    sampler_kwargs = {
        "nwalkers": NWALKERS,
        "ndim": NDIM,
        "log_prob_fn": log_likelihood,
        "kwargs": {
            "noise": noise,
            "yerr": yerr,
            "ranges": ranges,
            "wave_fcn": damped_wave,
            "wave_kwargs": wave_kwargs,
        }
    }

    samples, rms = emcee_trial(
        real=simulated_data,
        num_iterations=NUM_ITERATIONS,
        sampler_kwargs=sampler_kwargs,
        priors=p0,
        wave_fcn=damped_wave,
        wave_kwargs=wave_kwargs,
        use_met_hastings=False,
        met_hastings_kwargs=None
    )

    plotter = PlottingWrapper(
        samples=samples,
        param_ranges=ranges,
        wave_fcn=damped_wave,
        wave_kwargs=wave_kwargs,
        real_parameters=real_theta,
        noise=noise
    )

    figure, axes = plotter.plot_mcmc_wave_results()
    plt.show()

if __name__ == "__main__":
    estimate_inclination()

