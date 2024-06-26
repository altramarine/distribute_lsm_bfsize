import pandas as pd
import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.font_manager as font_manager


prop = font_manager.FontProperties(fname="./fonts/LinLibertine_Mah.ttf")
mpl.rcParams['font.family'] = prop.get_name()
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'font.size': 23})
#plt.rc('font',family='Linux Libertine Mono', size=15)

BPK = [1, 2, 3, 4, 5, 6, 7, 8]
# Zlist = ["Z0.0_ZD0_query_stats.txt", "Z0.25_ZD0_query_stats.txt", "Z0.5_ZD0_query_stats.txt", "Z0.75_ZD0_query_stats.txt", "Z1.0_ZD0_query_stats.txt"]
Ns = [1, 2, 4, 8, 16, 32]

df = pd.read_csv("output/stats.csv")
print(df)

algos = ["monkey", "binarysearch", "scan"]
algoname = ["gradient descent", "binary search", "scan"]
lines = ["--", "-.", "-"]
linecolors = ["black", "blue", "red"]
linemarkers = ["o", "s", "x"]
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
          #plt.title(f"bpk={bpk}")
          plt.plot(x, y, color = Col(int(z * 10 + 3) / 14), linestyle = line, label = f"z={z}, zd={zd}, {algo}")
          plt.xlabel("n(M)")
          plt.ylabel("time")
          # plt.ylim(0)
        # for N, ____df in ___df.groupby(___df["N"]):
          plt.subplot(8, 3, bpk * 3 + i - 2).legend()
  # plt.plot()
  # plt.show()
  plt.tight_layout()
  plt.savefig("./fig/split_bpk.pdf", bbox_inches = "tight", dpi=900)



def plot_for_linear_plot(bpk: int, zd = 0):
  allZ = [0.0, 0.5, 1.0]
  length = len(allZ)
  ____uniform = 'uniform'
  ____zipf ='zipf'
  # plt.figure(f'z = [0.0, 0.5, 1.0], {____uniform if zd==0 else ____zipf}, bpk = {bpk}', figsize=(12 * length, 9 * 1))
  ii = 0
  entries_per_file = 262144
  for z in allZ:
    plt.figure(f'Z{z:.1f}_{____uniform if zd==0 else ____zipf}_bpk{bpk}', figsize = (8, 6))
    ii += 1
    _df = df[df["bpk"] == bpk][df["ZD"] == zd][df["Z"] == z]
    for i in range(3):
      algo = algos[i]
      name = algoname[i]
      line = lines[i]
      x = []
      y = []
      for n in Ns:
        # print(n)
        if(len(_df[_df["N"] == n]) > 0):
          _x = int(round((n * 1000000)/entries_per_file)) 
          _y = np.average(_df[_df["N"] == n][f't_{algo}'])
          _h = np.average(_df[_df["N"] == n][f'n_file'])
          # x.append(_x)
          x.append(_h)
          y.append(_y)
      # plt.subplot(1, length, ii)
      #plt.title(f"Z{z:.1f}_{____uniform if zd==0 else ____zipf}_bpk{bpk}")
      # plt.plot(x, y, linestyle = line, label = f"{name}")
      plt.plot(x, y, label = f"{name}", color=linecolors[i], marker=linemarkers[i], markersize=16, fillstyle='none')
      plt.ticklabel_format(axis="x", style="sci", scilimits=(0,6))
      plt.yscale("log")
      plt.ylim(1e-6, 100)
      plt.yticks([1e-6,1e-4,0.01,1,100])
      plt.xlabel("\#SST files ($F$)")
      plt.ylabel("time (seconds)")
      # plt.ylim(0)
    # for N, ____df in ___df.groupby(___df["N"]):
    plt.legend()
    # plt.subplot(1, length, ii).legend()
    plt.tight_layout()
    plt.savefig(f"./fig/split/Z{z:.1f}_{____uniform if zd==0 else ____zipf}_bpk{bpk}.pdf", bbox_inches = "tight", dpi=900)
  # plt.savefig(f"./fig/{____uniform if zd==0 else ____zipf},bpk={bpk}.png")
  # plt.savefig("./fig/split_n.png")

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
  plt.tight_layout()
  plt.savefig("./fig/split_n.pdf", bbox_inches = "tight", dpi=900)
  # plt.show()



def main():
  for bpk in range(1, 8 + 1):
    plot_for_linear_plot(bpk = bpk, zd = 0)
    plot_for_linear_plot(bpk = bpk, zd = 3)
  #plot_for_n_as_xaxis_split_bpk()
  #plot_for_bpk_as_xaxis_split_n()

if __name__ == "__main__":
  main()
