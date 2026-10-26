import serial
import numpy as np
import time

SLOW_SCAN_SPEED_FREQUENCY = [10, 20, 100, 1000, 2000, 10000, 100000, 300000] # Hz
SLOW_SCAN_SPEED_TIME = [1600, 800, 483, 342, 336, 332, 332, 332] # ms

class Meter:
  conn: serial.Serial

  def __init__(self, port, baudrate = 115200):
    self.port = port
    self.baudrate = baudrate

  def connect(self):
    self.conn = serial.Serial(self.port, self.baudrate, timeout=2.0)
    time.sleep(0.1)

  def set_function_impedance(self):
    self.conn.write(b'FUNC Z-thd\n')
    time.sleep(0.1)

  def set_bias_voltage(self, v = 0):
    self.bias = v
    self.conn.write(f'BIAS {v}\n'.encode())
    time.sleep(0.1)

  def set_frequency(self, f = 1000):
    self.frequency = f
    self.conn.write(f'FREQ {f}\n'.encode())
    time.sleep(0.1)

  def set_stim_voltage(self, v = 0.05):
    self.stim = v
    self.conn.write(f'LEV:VOLT {v}\n'.encode())
    time.sleep(0.1)

  def set_average(self, samples):
    self.average = samples

  def set_slow_scan_speed(self):
    self.conn.write(b"APER SLOW\n")
    time.sleep(0.1)

  def set_trigger(self):
    self.conn.write(b"TRIG:SOUR BUS\n")
    time.sleep(0.1)

  def trigger(self):
    self.conn.write(b"TRIG\n")
    time.sleep(0.1)

  def fetch(self):
    self.conn.write(b'FETC:MAIN?\n')
    return self.conn.readline() # it waits for an entire line until serial.Serial timeouts

  def decode_fetch(self, bytes: bytes):
    mag, phase = bytes.decode("utf-8").split(",")
    print(f"\t{mag}\t{phase}")
    return float(mag.strip()), float(phase.strip())

  def sweep(self, frequencies, level, bias, average):
    self.set_function_impedance()
    self.set_bias_voltage(bias)
    self.set_stim_voltage(level)
    self.set_average(average)
    self.set_slow_scan_speed()
    self.set_trigger()
    print("Initialized System.")


    delays = np.interp(frequencies, SLOW_SCAN_SPEED_FREQUENCY, SLOW_SCAN_SPEED_TIME) * 1.5 / 1000 # s

    time.sleep(5) # wait 5 seconds before starting measurements
    results_magnitude = []
    results_phase = []
    for i, (frequency, delay) in enumerate(zip(frequencies, delays)):
      results_magnitude.append([])
      results_phase.append([])
      self.set_frequency(frequency)
      print(f"Set frequency to {frequency}.")

      for _ in range(self.average):
        self.trigger()
        time.sleep(delay)
        raw = self.fetch()
        data = self.decode_fetch(raw)
        results_magnitude[i].append(data[0])
        results_phase[i].append(data[1])
        time.sleep(0.05)

    return np.array(results_magnitude), np.array(results_phase)

  def __del__(self):
    self.conn.close()


