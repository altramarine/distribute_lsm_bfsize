mkdir build
cd build 
cmake ..
make
cd ..
# TEST_DIR=../skew-aware-bpk-benchmark/output-stats-for-optimization-exp/
TEST_DIR=/scratchHDDa/zczhu/Mnemosyne/skew-aware-bpk-benchmark/output-stats-for-optimization-exp
OUTPUT_DIR=./temp_output
REPEAT_NUM=1
TEST_BPK=(2 4 8)
# ./build/main -f ./varyN_bpk6_E128_ED_Q4M/N16M_bpk6_E128_ED_Q4M/test2/Z0.75_ZD0_query_stats.txt -b 1
python ./run_experiments.py -d $TEST_DIR -r $REPEAT_NUM --bpk ${TEST_BPK[@]}
python ./plot_N-time_foreach_bpk.py --bpk ${TEST_BPK[@]} -d ${OUTPUT_DIR}

cp ${OUTPUT_DIR}/Z0.0_uniform_bpk2.pdf ../exp-figures/Fig5-a.pdf
cp ${OUTPUT_DIR}/Z0.0_uniform_bpk8.pdf ../exp-figure/s/Fig5-b.pdf