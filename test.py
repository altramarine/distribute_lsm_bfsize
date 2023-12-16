import os
import pandas as pd
root_dir = ".\\file-access-exp-data"
dir_lists_1 = os.listdir(root_dir)
print(dir_lists_1)

stats = {
  "test": [],
  "workload": [],
  "time_monkey": [],
  "time_scan": [],
  "fpr_monkey": [],
  "fname": [],
  "fpr_scan": []
}

for file in dir_lists_1:
  workload_name = os.path.join(root_dir, file)
  dir_lists_2 = os.listdir(workload_name)
  for tests in dir_lists_2:
    test_name = os.path.join(workload_name, tests)
    dir_lists_3 = os.listdir(test_name)
    for nfile in dir_lists_3:
      file_name = os.path.join(test_name, nfile)
      print(file_name)
      os.system(f".\\build\\Release\\main.exe -f {file_name} 2> temp.out")
      df = pd.read_csv("temp.out", sep=':', header=None)
      print(df)
      stats["fpr_monkey"].append(df[1][0])
      stats["fpr_scan"].append(df[1][1])
      stats["time_monkey"].append(df[1][2])
      stats["time_scan"].append(df[1][3])
      stats["test"].append(tests)
      stats["fname"].append(nfile)
      stats["workload"].append(file)
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