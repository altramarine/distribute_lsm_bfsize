mkdir -p build
cd build 
cmake ..
make
cd ..
# ./build/main -f ./varyN_bpk6_E128_ED_Q4M/N16M_bpk6_E128_ED_Q4M/test2/Z0.75_ZD0_query_stats.txt -b 1
python ./test.py
python ./plot.py
