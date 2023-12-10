#include <algorithm>
#include <iostream>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include "stats/stats.hh"
#include "envir/env.hh"

using namespace std;
unordered_map<uint64_t, double> Scan_To_Get_OPTBPK::GetOptBPK(DbStats db_stats) {
  
  if (db_stats.num_levels <= 1) return {}; // do nothing when L <= 1
  uint64_t total_filter_memory = db_stats.num_entries * _env->bits_per_key;
  // solve \sum - ln p_i / (ln 2)^2 * n_i = M where n_i is the number of entries per file
  // plugged with Lagrange multiplier we have p_i * z_i / n_i should be a constant C where z_i is the number of non-existing
  // queries per file. Let C = p_i * z_i / n_i, we try to solve C first and then calculate p_i per file
  std:: cout << "Total memory: " << total_filter_memory << std::endl;
  // let S = \sum (ln n_i / z_i) * n_i, we have - (\sum z_i) * C - S = M * (ln 2)^2

  // p_i refers to the false positive rate of the i-th file, fp_queries represent the number of empty queries
  double S = 0;
  uint64_t fileID = 0;
  uint64_t fp_queries = 0;
  uint64_t num_entries_with_fp_queries = 0;
  std::priority_queue<pair<double, uint64_t> > entries_over_fp_with_fileID;
  double tmp;
  // fileID2entries represents the map between fileID and the number of entries of the associated file
  // fileID2fp_enrties represents the number of empty queries of the associated file
  for(auto iter = db_stats.fileID2entries.begin(); iter != db_stats.fileID2entries.end(); iter++) {
    if (db_stats.fileID2fp_queries.find(iter->first) != db_stats.fileID2fp_queries.end()) {
      fp_queries = db_stats.fileID2fp_queries.at(iter->first);
      if (fp_queries != 0 && iter->second != 0) {
	      tmp = iter->second*1.0/db_stats.fileID2fp_queries.at(iter->first);
        //std::cout << " fileID: " << iter->first << " tmp: " << tmp << std::endl;
        S += std::log(tmp*db_stats.num_total_fp_queries*1.0)*iter->second;
	      num_entries_with_fp_queries += iter->second;
	      entries_over_fp_with_fileID.push(make_pair(tmp, iter->first));
      }      
    }
  }
  const double log_2_squared = pow(std::log(2), 2);
  double num_total_fp_queries = db_stats.num_total_fp_queries;
  double C = -(total_filter_memory*log_2_squared + S)*1.0/num_entries_with_fp_queries;

  // final bpk assignments are stored in fileID2bpk
  unordered_map<uint64_t, double> fileID2bpk;
  // fileID with no bpk will also be stored in fileIDwithNobpk
  unordered_set<uint64_t> fileIDwithNobpk;
  // Calculating S = \sum (ln z_i / n_i) * z_i
  while (!entries_over_fp_with_fileID.empty() && std::log(entries_over_fp_with_fileID.top().first) + C > 0.0) {
     uint64_t fileID = entries_over_fp_with_fileID.top().second;
     S -= std::log(entries_over_fp_with_fileID.top().first*num_total_fp_queries*1.0)*db_stats.fileID2entries.at(fileID);
     num_entries_with_fp_queries -= db_stats.fileID2entries.at(fileID);
     S += num_entries_with_fp_queries*std::log((num_total_fp_queries - db_stats.fileID2fp_queries.at(fileID))*1.0/num_entries_with_fp_queries);
     num_total_fp_queries -= db_stats.fileID2fp_queries.at(fileID);
     fileIDwithNobpk.insert(fileID);
     fileID2bpk.emplace(fileID, 0.0);
     C = -(total_filter_memory*log_2_squared + S)/num_entries_with_fp_queries;
     entries_over_fp_with_fileID.pop();
     std::cout << "log(entries_over_fp_with_fileID.top().first) + C : " << std::log(entries_over_fp_with_fileID.top().first) + C << std::endl;
  }
  double bpk = 0.0;
  double final_total_memory = 0.0;
  for (auto iter = db_stats.fileID2entries.begin(); iter != db_stats.fileID2entries.end(); iter++) {
    if (db_stats.fileID2fp_queries.find(iter->first) != db_stats.fileID2fp_queries.end()) {
      fp_queries = db_stats.fileID2fp_queries.at(iter->first);
      if (fp_queries != 0 && fileIDwithNobpk.find(iter->first) == fileIDwithNobpk.end()) {
        bpk = -(std::log(iter->second*num_total_fp_queries*1.0/fp_queries) + C)/log_2_squared;
        fileID2bpk.emplace(iter->first, bpk);
        final_total_memory += bpk*iter->second;
      } else {
        fileID2bpk.emplace(iter->first, 0.0);
      }
    }
  }
  
  return fileID2bpk;
}
