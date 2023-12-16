#include <iostream>
#include "stats/stats.hh"
#include "envir/env.hh"
#include <random>
#include "cmdline.hh"
#include <chrono>
Env env(1);

DbStats stats;

void print_bpk_distribution(const std::unordered_map<uint64_t, double> &di, std::string info)  {
  std::cerr << std::endl;
  std::cerr << "(" << info << ")" << std::endl;
  std::cerr << "bpk_distribution: [" << std::endl;
  int cnt = 0;
  for(auto iter = di.begin(); iter != di.end(); iter ++) {
    cnt ++;
    if(cnt == 5) {
      fprintf(stderr, "...\n");
      break;
    }
    fprintf(stderr, "fid: %3d, bpk %2.5f, entries: %4d, total_bits: %10.3f\n", iter->first, iter->second, stats.fileID2entries[iter->first], stats.fileID2entries[iter->first] * iter->second);
    // std::cerr << "  fid: " << iter->first << ", bpk: " << iter->second << ", entries " << stats.fileID2entries[iter->first] << ", total_bits: " << stats.fileID2entries[iter->first] * iter->second << std::endl;
  }
  std::cerr << "]" << std::endl;
  std::cerr << "fpr: " << stats.evaluate_total_fpr(di) << std::endl;
  std::cerr << std::endl;
}

inline void read_and_inititate(FILE *fp, Env &env, DbStats &db_stats) {
  fscanf(fp, "%d%d%d", &db_stats.num_entries, &env.bits_per_key, &db_stats.num_files);
  for(int i = 0; i < db_stats.num_files; i ++) {
    int fid, entries, fp_queries;
    fscanf(fp, "%d%d%d", &fid, &entries, &fp_queries);
    db_stats.fileID2entries[fid] = entries;
    db_stats.fileID2fp_queries[fid] = fp_queries;
    db_stats.num_total_fp_queries += fp_queries;
    // db_stats.num_entries += entries;
  }
  db_stats.num_levels = 2;
}

int main(int argc, char **argv) {
  cmdline::parser psr = cmdline::parser();
  psr.add<std::string>("fname", 'f', "fname", true, "");
  psr.add<int>("rounds", 'r', "rounds", false, 100);
  bool ok_ = psr.parse(argc, argv);
  if(!ok_) {
    std::cerr << "INVALID ARGS" << std::endl;
    return 0;
  }
  std::string fname = psr.get<std::string>("fname");
  FILE* Fp = stdin;
  if(fname != "") Fp = fopen(fname.c_str(), "r");
  read_and_inititate(Fp, env, stats);
  int rounds = psr.get<int>("rounds");
  Get_BPK *p = static_cast<Get_BPK*> (new Method_Of_Monkey(&env));
  Get_BPK *p2 = static_cast<Get_BPK*> (new Scan_To_Get_OPTBPK(&env));
  // std::cerr << "using_p" << std::endl;
  double total_fpr_p = 0, total_fpr_p2 = 0;
  double total_time_p = 0, total_time_p2 = 0;
  for(int i = 0; i < rounds; i ++) {
    auto start = std::chrono::high_resolution_clock::now();
    
    auto x = p->GetOptBPK(stats);
    total_fpr_p += stats.evaluate_total_fpr(x);
    // print_bpk_distribution(x, "monkey");
    
    auto end1 = std::chrono::high_resolution_clock::now();
    
    auto x2 = p2->GetOptBPK(stats);
    total_fpr_p2 += stats.evaluate_total_fpr(x2);
    // print_bpk_distribution(x2, "scan_normalized");
    
    auto end2 = std::chrono::high_resolution_clock::now();

    total_time_p += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start).count() / 1e9;
    total_time_p2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - end1).count() / 1e9;
  }
  std::cerr << "avg_fpr  monkey:  " << total_fpr_p / rounds << "\n" << "avg_fpr scan_normalized:  " << total_fpr_p2 / rounds << std::endl;
  std::cerr << "avg_time monkey:  " << total_time_p / rounds << "\n" << "avg_time scan_normalized:  " << total_time_p2 / rounds << std::endl;
  
}