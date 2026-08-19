
import pandas as pd

xl = pd.ExcelFile("12_2_2015_Incremental OCV test_SP20-1.xlsx")
ch1 = pd.read_excel("12_2_2015_Incremental OCV test_SP20-1.xlsx", sheet_name="Channel_1-005_1")
ch2 = pd.read_excel("12_2_2015_Incremental OCV test_SP20-1.xlsx", sheet_name="Channel_1-005_2")
ch3 = pd.read_excel("12_2_2015_Incremental OCV test_SP20-1.xlsx", sheet_name="Channel_1-005_3")

combined = pd.concat([ch1, ch2, ch3], ignore_index=True)
print(combined.shape)
print(combined["Step_Index"].unique())

rest_steps = [4, 6, 8, 10]
rest_data = combined[combined["Step_Index"].isin(rest_steps)]
print(rest_data.shape)

combined["rest_flag"] = combined["Step_Index"].isin(rest_steps)
combined["rest_block"] = (combined["rest_flag"] != combined["rest_flag"].shift()).cumsum()
rest_blocks = combined[combined["rest_flag"]]["rest_block"].nunique()
print("Number of separate rest periods:", rest_blocks)

rest_only = combined[combined["rest_flag"]]

ocv_points = rest_only.groupby("rest_block").last()
print(ocv_points[["Voltage(V)", "Charge_Capacity(Ah)", "Discharge_Capacity(Ah)", "Step_Index"]])

rated_capacity = 2.0
ocv_points = ocv_points.reset_index()

discharged_ah = ocv_points["Discharge_Capacity(Ah)"]
charged_ah = ocv_points["Charge_Capacity(Ah)"]

ocv_points["soc_discharge"] = 100 - (discharged_ah / rated_capacity) * 100
ocv_points["soc_charge"] = (charged_ah / rated_capacity) * 100

print(ocv_points[["rest_block", "Step_Index", "Voltage(V)", "soc_discharge", "soc_charge"]])

discharge_sweep = ocv_points[ocv_points["Step_Index"].isin([4, 6, 8])]
charge_sweep = ocv_points[ocv_points["Step_Index"].isin([10])]

print(discharge_sweep.shape)
print(charge_sweep.shape)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.figure()
plt.plot(discharge_sweep["soc_discharge"], discharge_sweep["Voltage(V)"], marker="o", label="Discharge sweep")
plt.plot(charge_sweep["soc_charge"], charge_sweep["Voltage(V)"], marker="o", label="Charge sweep")
plt.xlabel("SoC (%)")
plt.ylabel("Voltage (V)")
plt.title("True OCV-SoC Curve (INR 18650-20R, CALCE Data)")
plt.legend()
plt.grid(True)
plt.savefig("true_ocv_curve.png")
print("Saved true OCV curve!")