import argparse
from meter import Meter
import numpy as np
import plotter


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Run a frequency sweep using the LCR 6200 device."
  )

  # Connection arguments
  parser.add_argument(
    "-p",
    "--port",
    required=True,
    help="Serial port connected to the meter (e.g., COM3 or /dev/ttyUSB0)",
  )
  parser.add_argument(
    "-b",
    "--baudrate",
    type=int,
    default=115200,
    help="Serial baudrate (default: 115200)",
  )

  # Measurement configuration arguments
  parser.add_argument(
    "-l",
    "--level",
    type=float,
    default=0.05,
    help="Stimulus voltage level in volts (default: 0.05)",
  )

  parser.add_argument(
    "--bias", type=float, default=0.0, help="Bias voltage in volts (default: 0.0)"
  )

  parser.add_argument(
    "-a",
    "--average",
    type=int,
    default=1,
    help="Number of samples to average per frequency (default: 1)",
  )

  # Frequency sweep options
  parser.add_argument(
    "-f",
    "--from",
    dest="freq_from",
    type=float,
    default=10,
    help="Minimum frequency value in the sweep",
  )

  parser.add_argument(
    "-t",
    "--to",
    type=float,
    default=200000,
    help="Maximum frequency value in the sweep",
  )

  parser.add_argument(
    "-N",
    "--count",
    type=int,
    default=7,
    help="Frequencies per decade",
  )

  args = parser.parse_args()

  f_min = args.freq_from
  f_max = args.to
  N = args.count

  # Calculate total decades and total number of points
  num_decades = np.log10(f_max / f_min)
  total_points = int(round(num_decades * N)) + 1

  # Generate log-spaced frequencies
  frequencies = np.logspace(np.log10(f_min), np.log10(f_max), num=total_points)

  meter = Meter(port=args.port, baudrate=args.baudrate)
  meter.connect()

  # print(f"Connected to {args.port} at {args.baudrate} baud.")
  print(f"Running sweep across {frequencies} frequencies...")

  mag, phase = meter.sweep(
    frequencies=args.frequencies,
    level=args.level,
    bias=args.bias,
    average=args.average,
  )

  plotter.plot(frequencies, mag, phase)

  print("\n--- Sweep Complete ---")
  print("Magnitude:\n", mag)
  print("Phase:\n", phase)
