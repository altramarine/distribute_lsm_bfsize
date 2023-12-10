#include <iostream>
#include "stats/stats.hh"
#include "envir/env.hh"

Env env(8);

DbStats stats;

int main() {
  // std::cout << "Hello World" << std::endl;
  stats.fileID2entries[1] = 20;
  stats.fileID2fp_queries[1] = 3;
  stats.fileID2entries[2] = 20;
  stats.fileID2fp_queries[2] = 3;
  stats.num_levels = 2;
  stats.num_entries = 40;
  stats.num_total_fp_queries = 6;

  Get_BPK *p = static_cast<Get_BPK*> (new Scan_To_Get_OPTBPK(&env));
  // std::cerr << "using_p" << std::endl;
  auto x = p->GetOptBPK(stats);
  // std::cerr << "used_p" << std::endl;
  for(auto iter = x.begin(); iter != x.end(); iter ++) {
    std::cerr << "fid: " << iter->first << ", bpk: " << iter->second << ", entries " << stats.fileID2entries[iter->first] << ", total_bits: " << stats.fileID2entries[iter->first] * iter->second << std::endl;
  }
}