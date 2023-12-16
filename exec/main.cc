#include <iostream>
#include "stats/stats.hh"
#include "envir/env.hh"
#include <random>

Env env(1);

DbStats stats;

void print_bpk_distribution(const std::unordered_map<uint64_t, double> &di, std::string info)  {
  std::cerr << std::endl;
  std::cerr << "(" << info << ")" << std::endl;
  std::cerr << "bpk_distribution: [" << std::endl;
  for(auto iter = di.begin(); iter != di.end(); iter ++) {
    fprintf(stderr, "fid: %3d, bpk %2.5f, entries: %4d, total_bits: %10.3f\n", iter->first, iter->second, stats.fileID2entries[iter->first], stats.fileID2entries[iter->first] * iter->second);
    // std::cerr << "  fid: " << iter->first << ", bpk: " << iter->second << ", entries " << stats.fileID2entries[iter->first] << ", total_bits: " << stats.fileID2entries[iter->first] * iter->second << std::endl;
  }
  std::cerr << "]" << std::endl;
  std::cerr << "fpr: " << stats.evaluate_total_fpr(di) << std::endl;
  std::cerr << std::endl;
}

int main() {
  std::mt19937 rd(114514);
  for(int ii = 0 ; ii < 100; ii ++) {
  int n = 3;
  // std::cout << "Hello World" << std::endl;
  std::uniform_int_distribution<int> randentries(1, 10);
  std::uniform_int_distribution<int> randqueries(1, 10);
  stats.num_entries = 0;
  stats.num_total_fp_queries = 0;
  std::cerr << "input data" << std::endl;
  for(size_t i = 1; i <= n; i ++) {
    stats.fileID2entries[i] = randentries(rd);
    stats.fileID2fp_queries[i] = randqueries(rd);
    std::cerr << "entries: " << stats.fileID2entries[i] << ", queries: " << stats.fileID2fp_queries[i] << std::endl;
    stats.num_entries += stats.fileID2entries[i];
    stats.num_total_fp_queries += stats.fileID2fp_queries[i];
  }
  stats.num_levels = 2;
  // stats.num_entries = 40;
  // stats.num_total_fp_queries = 6;
  Get_BPK *p = static_cast<Get_BPK*> (new Method_Of_Monkey(&env));
  Get_BPK *p2 = static_cast<Get_BPK*> (new Scan_To_Get_OPTBPK(&env));
  // std::cerr << "using_p" << std::endl;
  auto x = p->GetOptBPK(stats);
  print_bpk_distribution(x, "monkey");
  auto x2 = p2->GetOptBPK(stats);
  print_bpk_distribution(x2, "scan_normalized");
  }
}