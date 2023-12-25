import pandas as pd
import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

# mpl.rcParams['text.usetex'] = True

root_dir = ".\\varyN_bpk6_E128_ED_Q4M"
BPK = [2, 4, 6, 8, 16, 32]
dir_lists_1 = os.listdir(root_dir)
# Zlist = ["Z0.0_ZD0_query_stats.txt", "Z0.25_ZD0_query_stats.txt", "Z0.5_ZD0_query_stats.txt", "Z0.75_ZD0_query_stats.txt", "Z1.0_ZD0_query_stats.txt"]

df = pd.read_csv("output/stats.csv")
print(df)
for x in dir_lists_1:
  Z = df[df["workload"] == x];
  for key, val in Z.groupby(Z['fname']):  
    plt.figure(f'{x}-{key}',figsize=(8 * 3,6))
    plt.subplot(1, 3, 1)
    X_monkey = []
    Y_monkey = []
    X_scan = []
    Y_scan = []
    
    monkey_t = []
    binary_t= []
    scan_t = []
    for bpk in BPK:
      H = val[val["bpk"] == bpk]
      monkey_t.append(np.average(H['t_monkey']))
      binary_t.append(np.average(H['t_binarysearch']))
      scan_t.append(np.average(H['t_scan']))
    plt.plot(BPK, monkey_t, label=f'monkey-{key}')
    # plt.plot(BPK, binary_t, label=f'binary-{key}')
    # plt.plot(BPK, scan_t, label=f'scan-{key}')
    plt.xlabel("bpk")
    plt.ylabel("time")
    # plt.xscale('log')
    
    plt.legend()
  # plt.show()
  
  
    plt.subplot(1, 3, 2)
    Z = df[df["workload"] == x];
    print(Z)
    X_monkey = []
    Y_monkey = []
    X_scan = []
    Y_scan = []
    monkey_t = []
    binary_t= []
    scan_t = []
    for bpk in BPK:
      H = val[val["bpk"] == bpk]
      monkey_t.append(np.average(H['t_monkey']))
      binary_t.append(np.average(H['t_binarysearch']))
      scan_t.append(np.average(H['t_scan']))
    # plt.plot(BPK, monkey_t, label=f'monkey-{key}')
    plt.plot(BPK, binary_t, label=f'binary-{key}')
    # plt.plot(BPK, scan_t, label=f'scan-{key}')
    plt.xlabel("bpk")
    plt.ylabel("time")
    # plt.xscale('log')
    
    plt.legend()
  # plt.show()

    plt.subplot(1, 3, 3)
    Z = df[df["workload"] == x];
    print(Z)
    X_monkey = []
    Y_monkey = []
    X_scan = []
    Y_scan = []
    monkey_t = []
    binary_t= []
    scan_t = []
    for bpk in BPK:
      H = val[val["bpk"] == bpk]
      monkey_t.append(np.average(H['t_monkey']))
      binary_t.append(np.average(H['t_binarysearch']))
      scan_t.append(np.average(H['t_scan']))
    # plt.plot(BPK, monkey_t, label=f'monkey-{key}')
    # plt.plot(BPK, binary_t, label=f'binary-{key}')
    plt.plot(BPK, scan_t, label=f'scan-{key}')
    plt.xlabel("bpk")
    plt.ylabel("time")
    # plt.xscale('log')
    plt.legend()
    # plt.rcParams['figure.figsize'] = [8000, 2000]
    # plt.show()
    plt.savefig(f'./fig/{x}---{key}.png')