#ifndef STATS_HH
#define STATS_HH
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include "envir/env.hh"

struct DbStats {
  uint32_t fst_level_with_entries = 0;
  uint32_t num_levels = 0;
  uint32_t num_entries = 0;
  uint32_t num_files = 0;
  uint64_t num_total_fp_queries = 0;
  std::vector<uint64_t> level2entries;
  std::vector<uint64_t> entries_in_level0;
  std::unordered_map<uint64_t, uint64_t> fileID2fp_queries; // number of false positive queries for a fileID
  std::unordered_map<uint64_t, uint64_t> fileID2entries;    // number of entries for a fileID
};


class Get_BPK {
public:
  Get_BPK(Env *_env) : _env(_env) {}
  virtual std::unordered_map<uint64_t, double> GetOptBPK(DbStats db_stats) = 0;
  Env *_env;
};

class Scan_To_Get_OPTBPK: public Get_BPK {
public:
  Scan_To_Get_OPTBPK(Env *_env) : Get_BPK(_env) {}
  std::unordered_map<uint64_t, double> GetOptBPK(DbStats db_stats);
};

#endif