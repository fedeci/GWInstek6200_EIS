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
        self.conn = serial.Serial(self.port, self.baudrate, timeout=1.5 * max(SLOW_SCAN_SPEED_FREQUENCY) / 1000)
        time.sleep(0.1)

    def set_meas_page(self):
        self.conn.write(b"DISP:PAGE MEAS\n")
        time.sleep(1)

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
        self.conn.write(b"TRIG:DLY min\n")
        time.sleep(0.1)

    def trigger_fetch(self):
        self.conn.write(b"*TRG\n")
        return self.conn.readline()  
        # undocumented, but TRIG:IMM returns an empty line when the measurement is complete; i.e. we can immediately perform a fetch after a trigger because self.conn.readline will block the program until the trigger is complete

    def decode_fetch(self, bytes: bytes):
        mag, phase, _, _, _ = bytes.decode("utf-8").split(",")
        print(f"\t{mag}\t{phase}")
        return float(mag.strip()), float(phase.strip())

    def sweep(self, frequencies, level, bias, average):
        self.set_meas_page()
        self.set_function_impedance()
        self.set_bias_voltage(bias)
        self.set_stim_voltage(level)
        self.set_average(average)
        self.set_slow_scan_speed()
        self.set_trigger()
        print("Initialized System.")

        time.sleep(5) # wait 5 seconds before starting measurements
        results_magnitude = []
        results_phase = []
        for i, frequency in enumerate(frequencies):
            results_magnitude.append([])
            results_phase.append([])
            self.set_frequency(frequency)
            print(f"Set frequency to {frequency}.")

            # trigger two times to reset the value
            for _ in range(2):
                self.trigger_fetch()
                time.sleep(0.5)

            for _ in range(self.average):
                raw = self.trigger_fetch()
                data = self.decode_fetch(raw)
                results_magnitude[i].append(data[0])
                results_phase[i].append(data[1])
                time.sleep(0.05)

        return np.array(results_magnitude), np.array(results_phase)

    def __del__(self):
        self.conn.close()
