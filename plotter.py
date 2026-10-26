import matplotlib.pyplot as plt
import numpy as np


# Accepts vectors in the form of
# mag[frequencies, samples] and
# phase[frequencies, samples]
def plot(frequencies, mag, phase):
    mag_mean = np.mean(mag, axis=1)
    mag_std = np.std(mag, axis=1)

    phase_mean = np.mean(phase, axis=1)
    phase_std = np.std(phase, axis=1)

    # --- Plotting ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(frequencies, mag_mean, color="tab:blue", label="Mean Magnitude", linewidth=2)
    ax1.fill_between(frequencies, mag_mean - mag_std, mag_mean + mag_std, color='tab:blue', alpha=0.2, label='± 1 Std Dev')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Frequency (Hz)', fontsize=11)
    ax1.set_ylabel('Magnitude', fontsize=11)
    ax1.set_title('Frequency Sweep: Magnitude', fontsize=12)
    ax1.grid(True, which="both", ls="--", alpha=0.6)
    ax1.legend()

    ax2.plot(frequencies, phase_mean, color="tab:orange", label="Mean Phase", linewidth=2)
    ax2.fill_between(
        frequencies,
        phase_mean - phase_std,
        phase_mean + phase_std,
        color="tab:orange",
        alpha=0.2,
        label="± 1 Std Dev",
    )
    ax2.set_xscale("log")
    ax2.set_ylim(-90, 0)
    ax2.set_xlabel("Frequency (Hz)", fontsize=11)
    ax2.set_ylabel("Phase (Degrees)", fontsize=11)
    ax2.set_title("Frequency Sweep: Phase", fontsize=12)
    ax2.grid(True, which="both", ls="--", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    plt.show()
