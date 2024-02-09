import os
import re
import pandas as pd
import platform

__plat__ = platform.system().lower()

if __plat__ == 'windows':
  root_dir = ".\\varyN_bpk6_E128_ED_Q4M"
elif __plat__ == 'linux':
  root_dir = "./varyN_bpk6_E128_ED_Q4M"
else:
  print("Unsupported System")
  exit()
dir_lists_1 = os.listdir(root_dir)
print(dir_lists_1)

BPK = [1, 2, 3, 4, 5, 6, 7, 8]

stats = {
  "test": [],
  "fname": [],
  "workload": [],
  "bpk": [],
  "Z": [], 
  "ZD": [],
  "N": [],
  "fpr_monkey": [],
  "fpr_binarysearch": [],
  "fpr_scan": [],
  "t_monkey": [], 
  "t_binarysearch": [],
  "t_scan": [],
  "zeroes": [],
  "n_file": []
}
attributes = [
  "fpr_monkey",
  "fpr_binarysearch",
  "fpr_scan",
  "t_monkey", 
  "t_binarysearch",
  "t_scan",
  "zeroes",
  "n_file"
]

for file in dir_lists_1:
  pattern = re.compile(r'N\d+')
  n = int(pattern.findall(file)[0][1:])
  workload_name = os.path.join(root_dir, file)
  dir_lists_2 = os.listdir(workload_name)
  for tests in dir_lists_2:
    test_name = os.path.join(workload_name, tests)
    dir_lists_3 = os.listdir(test_name)
    for nfile in dir_lists_3:
      # print(nfile)
      pattern1 = re.compile(r'Z\d+.\d+')
      pattern2 = re.compile(r'ZD\d+')
      z = float(pattern1.findall(nfile)[0][1:])
      zd = int(pattern2.findall(nfile)[0][2:])
      # print(z, zd)
      for bpk in BPK:
        file_name = os.path.join(test_name, nfile)
        print(f'n = {n}*1e6 testing: {nfile} with bpk {bpk}, ')
        # os.system(f".\\build\\Release\\main.exe -f {file_name} -b {bpk}")
        if __plat__ == 'windows':
          os.system(f".\\build\\Release\\main.exe -f {file_name} -b {bpk} 2> temp.out")
        elif __plat__ == 'linux':
          os.system(f"./build/main -f {file_name} -b {bpk} 2> temp.out")
        # os.system(f".\\build\\Release\\main.exe -f {file_name} -b {bpk} 2> temp.out")
        df = pd.read_csv("temp.out", sep=':', header=None)
        print(df)
        for i,key in enumerate(attributes):
          print(key)
          stats[key].append(df[1][i])
        stats['N'].append(n)
        stats['Z'].append(z)
        stats['ZD'].append(zd)
        stats["test"].append(tests)
        stats["fname"].append(nfile)
        stats["workload"].append(file)
        stats["bpk"].append(bpk)
        df = pd.DataFrame(data=stats)
        print(df)
        df.to_csv("output/stats.csv")
        # df = pd.DataFrame(data=stats)
        # print(df)
  # print(stats)

df = pd.DataFrame(data=stats)
print(df)
df.to_csv("output/stats.csv")

  # temp_name = os.path.join(temp_dir, file)
  # calculate(file_name, temp_name)
  # print(datetime.datetime.now(), "Finish file: {}".format(file_name))