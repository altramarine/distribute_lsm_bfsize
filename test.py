import os
import pandas as pd
root_dir = ".\\varyN_bpk6_E128_ED_Q4M"
dir_lists_1 = os.listdir(root_dir)
print(dir_lists_1)

BPK = [2, 4, 6, 8, 16, 32]

stats = {
  "test": [],
  "fname": [],
  "workload": [],
  "bpk": [],
  "fpr_monkey": [],
  "fpr_binarysearch": [],
  "fpr_scan": [],
  "t_monkey": [], 
  "t_binarysearch": [],
  "t_scan": []
}
attributes = [
  "fpr_monkey",
  "fpr_binarysearch",
  "fpr_scan",
  "t_monkey", 
  "t_binarysearch",
  "t_scan"
]

for file in dir_lists_1:
  workload_name = os.path.join(root_dir, file)
  dir_lists_2 = os.listdir(workload_name)
  for tests in dir_lists_2:
    test_name = os.path.join(workload_name, tests)
    dir_lists_3 = os.listdir(test_name)
    for nfile in dir_lists_3:
      for bpk in BPK:
        file_name = os.path.join(test_name, nfile)
        print(file_name)
        os.system(f".\\build\\Release\\main.exe -f {file_name} -b {bpk} 2> temp.out")
        df = pd.read_csv("temp.out", sep=':', header=None)
        print(df)
        for i,key in enumerate(attributes):
          print(key)
          stats[key].append(df[1][i])
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