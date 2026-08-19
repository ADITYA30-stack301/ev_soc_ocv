import scipy.io

mat = scipy.io.loadmat("B0005.mat")
cycles = mat["B0005"][0, 0]["cycle"][0]

impedance_cycles = [c for c in cycles if c["type"][0] ==  "impedance"]
print("Number of impedance cycles :", len(impedance_cycles))

one_cycle = impedance_cycles[0]
print(list(one_cycle["data"].dtype.names))

one_discharge = [c for c in cycles if c["type"][0] == "discharge"][0]
time = one_discharge["data"]["Time"][0, 0][0]

gaps = [time[i] - time[i-1] for i in range(1, len(time))]
print("Max gap between readings (seconds):", max(gaps))
print("Min gap:", min(gaps))