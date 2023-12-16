cd build 

cmake --build . --config Release

cd ..\tests

..\build\Release\main.exe -f .\Z0.0_ZD0_dump_query_stats.txt
..\build\Release\main.exe -f .\Z0.5_ZD0_dump_query_stats.txt
..\build\Release\main.exe -f .\Z1.0_ZD0_dump_query_stats.txt