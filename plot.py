import pandas as pd
import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

# mpl.rcParams['text.usetex'] = True

root_dir = ".\\varyN_bpk6_E128_ED_Q4M"
BPK = [1, 2, 3, 4, 5, 6, 7, 8]
dir_lists_1 = os.listdir(root_dir)
# Zlist = ["Z0.0_ZD0_query_stats.txt", "Z0.25_ZD0_query_stats.txt", "Z0.5_ZD0_query_stats.txt", "Z0.75_ZD0_query_stats.txt", "Z1.0_ZD0_query_stats.txt"]
Ns = [1, 2, 4, 8, 16, 32]

df = pd.read_csv("output/stats.csv")
print(df)

algos = ["monkey", "binarysearch", "scan"]
lines = ["--", "-.", "-"]
def plot_for_n_as_xaxis_split_bpk():
  plt.figure(f'run_for_n, split_n_bpk',figsize=(12 * 3, 9 * 8))
  for bpk in BPK:
    _df = df[df["bpk"] == bpk]
    for zd, __df in _df.groupby(_df["ZD"]):
      if zd == 0:
        Col = plt.get_cmap('Blues')
      else:
        Col = plt.get_cmap('Greens')
      for z, ___df in __df.groupby(_df["Z"]):
        for i in range(3):
          algo = algos[i]
          line = lines[i]
          x = []
          y = []
          for n in Ns:
            if(len(___df[___df["N"] == n]) > 0):
              _x = n;
              _y = np.average(___df[___df["N"] == n][f't_{algo}'])
              x.append(_x)
              y.append(_y)
          plt.subplot(8, 3, bpk * 3 + i - 2)
          plt.title(f"bpk={bpk}")
          plt.plot(x, y, color = Col(int(z * 10 + 3) / 14), linestyle = line, label = f"z={z}, zd={zd}, {algo}")
          plt.xlabel("n(M)")
          plt.ylabel("time")
          # plt.ylim(0)
        # for N, ____df in ___df.groupby(___df["N"]):
          plt.subplot(8, 3, bpk * 3 + i - 2).legend()
  # plt.plot()
  # plt.show()
  plt.savefig("./fig/split_bpk.png")

plot_for_n_as_xaxis_split_bpk()


def plot_for_bpk_as_xaxis_split_n():
  plt.figure(f'run_for_n, split_n_bpk',figsize=(12 * 3, 9 * 6))
  ii = 0
  for n in Ns:
    ii += 1
    _df = df[df["N"] == n]
    for zd, __df in _df.groupby(_df["ZD"]):
      if zd == 0:
        Col = plt.get_cmap('Blues')
      else:
        Col = plt.get_cmap('Greens')
      for z, ___df in __df.groupby(_df["Z"]):
        for i in range(3):
          algo = algos[i]
          line = lines[i]
          x = []
          y = []
          for bpk in BPK:
            _x = bpk;
            _y = np.average(___df[___df["bpk"] == bpk][f't_{algo}'])
            x.append(_x)
            y.append(_y)
          plt.subplot(6, 3, ii * 3 + i - 2)
          plt.title(f"N = {n}")
          # print(int(z * 10 + 1) / 11, Col(int(z * 10 + 1) / 11))
          plt.plot(x, y, color = Col(int(z * 10 + 3) / 14), linestyle = line, label = f"z={z}, zd={zd}, {algo}")
        # for N, ____df in ___df.groupby(___df["N"]):
          plt.xlabel("pbk")
          plt.ylabel("time")
          # plt.ylim(0)
          plt.subplot(6, 3, ii * 3 + i - 2).legend()
  plt.savefig("./fig/split_n.png")
  # plt.show()

plot_for_bpk_as_xaxis_split_n()

# for x in dir_lists_1:
#   Z = df[df["workload"] == x];
#   for key, val in Z.groupby(Z['fname']):  
#     plt.figure(f'{x}-{key}',figsize=(8 * 3,6))
#     plt.subplot(1, 3, 1)
#     X_monkey = []
#     Y_monkey = []
#     X_scan = []
#     Y_scan = []
    
#     monkey_t = []
#     binary_t= []
#     scan_t = []
#     for bpk in BPK:
#       H = val[val["bpk"] == bpk]
#       monkey_t.append(np.average(H['t_monkey']))
#       binary_t.append(np.average(H['t_binarysearch']))
#       scan_t.append(np.average(H['t_scan']))
#     plt.plot(BPK, monkey_t, label=f'monkey-{key}')
#     # plt.plot(BPK, binary_t, label=f'binary-{key}')
#     # plt.plot(BPK, scan_t, label=f'scan-{key}')
#     plt.xlabel("bpk")
#     plt.ylabel("time")
#     # plt.xscale('log')
    
#     plt.legend()
#   # plt.show()
  
  
#     plt.subplot(1, 3, 2)
#     Z = df[df["workload"] == x];
#     print(Z)
#     X_monkey = []
#     Y_monkey = []
#     X_scan = []
#     Y_scan = []
#     monkey_t = []
#     binary_t= []
#     scan_t = []
#     for bpk in BPK:
#       H = val[val["bpk"] == bpk]
#       monkey_t.append(np.average(H['t_monkey']))
#       binary_t.append(np.average(H['t_binarysearch']))
#       scan_t.append(np.average(H['t_scan']))
#     # plt.plot(BPK, monkey_t, label=f'monkey-{key}')
#     plt.plot(BPK, binary_t, label=f'binary-{key}')
#     # plt.plot(BPK, scan_t, label=f'scan-{key}')
#     plt.xlabel("bpk")
#     plt.ylabel("time")
#     # plt.xscale('log')
    
#     plt.legend()
#   # plt.show()

#     plt.subplot(1, 3, 3)
#     Z = df[df["workload"] == x];
#     print(Z)
#     X_monkey = []
#     Y_monkey = []
#     X_scan = []
#     Y_scan = []
#     monkey_t = []
#     binary_t= []
#     scan_t = []
#     for bpk in BPK:
#       H = val[val["bpk"] == bpk]
#       monkey_t.append(np.average(H['t_monkey']))
#       binary_t.append(np.average(H['t_binarysearch']))
#       scan_t.append(np.average(H['t_scan']))
#     # plt.plot(BPK, monkey_t, label=f'monkey-{key}')
#     # plt.plot(BPK, binary_t, label=f'binary-{key}')
#     plt.plot(BPK, scan_t, label=f'scan-{key}')
#     plt.xlabel("bpk")
#     plt.ylabel("time")
#     # plt.xscale('log')
#     plt.legend()
#     # plt.rcParams['figure.figsize'] = [8000, 2000]
#     # plt.show()
#     plt.savefig(f'./fig/{x}---{key}.png')