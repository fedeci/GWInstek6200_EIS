import csv
import datetime
from pathlib import Path
import numpy as np

# Accepts vectors in the form of
# frequencies[]
# mag(frequencies, samples)[?] and
# phase(frequencies, samples)[?]
# bias_list[]
def save_to_csv(
    frequencies, mag, phase, bias_list, mode="STA", level=0.05, average=1, outdir=None, title=None
):
    if outdir is None:
        return

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Generate a safe timestamp filename
    filename = datetime.datetime.today().strftime("%y%m%d-%H%M%S") + "_sweep" + ("" if title is None else f"_{title}") + ".csv"
    filepath = outdir / filename

    mag_list = mag if len(bias_list) > 1 else [mag]
    phase_list = phase if len(bias_list) > 1 else [phase]

    with open(filepath, mode="w", newline="") as f:
        writer = csv.writer(f)

        # Write CSV Header with metadata columns
        writer.writerow(
            [
                "Mode",
                "Level (V)",
                "Average",
                "Bias (V)",
                "Frequency (Hz)",
                "Sample Index",
                "Magnitude",
                "Phase (deg)",
            ]
        )

        for b_idx, b_val in enumerate(bias_list):
            m_matrix = mag_list[b_idx]
            p_matrix = phase_list[b_idx]

            num_freqs, num_samples = m_matrix.shape

            for f_idx in range(num_freqs):
                freq = frequencies[f_idx]
                for s_idx in range(num_samples):
                    writer.writerow(
                        [
                            mode,
                            level,
                            average,
                            b_val,
                            freq,
                            s_idx,
                            m_matrix[f_idx, s_idx],
                            p_matrix[f_idx, s_idx],
                        ]
                    )

    print(f"CSV data successfully saved to: {filepath}")
