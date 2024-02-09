cd build 

cmake --build . --config Release

cd ..
python ./test.py

@REM cd ..\tests
@REM .\build\Release\main.exe -f .\varyN_bpk6_E128_ED_Q4M\N1M_bpk6_E128_ED_Q4M\test4\Z0.0_ZD0_query_stats.txt
@REM ..\build\Release\main.exe -f .\Z0.0_ZD0_dump_query_stats.txt
@REM ..\build\Release\main.exe -f .\Z0.5_ZD0_dump_query_stats.txt
@REM ..\build\Release\main.exe -f .\Z1.0_ZD0_dump_query_stats.txt