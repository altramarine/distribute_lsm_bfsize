import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
root_dir = ".\\file-access-exp-data"

dir_lists_1 = os.listdir(root_dir)
Zlist = ["Z0.0_ZD0_query_stats.txt", "Z0.25_ZD0_query_stats.txt", "Z0.5_ZD0_query_stats.txt", "Z0.75_ZD0_query_stats.txt", "Z1.0_ZD0_query_stats.txt"]

df = pd.read_csv("output/stats.csv")
print(df)
for x in dir_lists_1:
  plt.figure(x)
  Z = df[df["workload"] == x];
  print(Z)
  X_monkey = []
  Y_monkey = []
  X_scan = []
  Y_scan = []
  for (i, z) in enumerate(Zlist):
    # print(i, z)
    # print(Z)
    # print(Z[Z["fname"] == z].to_numpy())
    # print(Z[df["fname"] == z]["time_monkey"])
    avg_monkey = np.average(Z[df["fname"] == z]["time_monkey"].to_numpy())
    X_monkey.append(i * 0.25)
    Y_monkey.append(avg_monkey)
    avg_scan = np.average(Z[df["fname"] == z]["time_scan"].to_numpy())
    X_scan.append(i * 0.25)
    Y_scan.append(avg_scan)
  plt.plot(X_monkey, Y_monkey)
  plt.plot(X_scan, Y_scan)
  plt.show()
    