import pandas as pd



points = pd.read_csv("ocv_soc_points.csv")
print(points.columns.tolist())

discharge_sweep = points[points["Step_Index"].isin([4, 6, 8])]
charge_sweep = points[points["Step_Index"].isin([10])]

discharge_sweep = discharge_sweep.sort_values("soc_discharge")

import numpy as np

def voltage_to_soc(voltage):
    return np.interp(voltage, discharge_sweep["Voltage(V)"], discharge_sweep["soc_discharge"])

discharge_sweep_by_voltage = discharge_sweep.sort_values("Voltage(V)")

def soc_to_voltage(soc):
    return np.interp(soc, discharge_sweep["soc_discharge"], discharge_sweep["Voltage(V)"])

test_voltage = 3.6
print(f"At {test_voltage}V, estimated SoC: {voltage_to_soc(test_voltage):.2f}%")

test_soc = 50
print(f"At {test_soc}% SoC, estimated voltage: {soc_to_voltage(test_soc):.2f}V")