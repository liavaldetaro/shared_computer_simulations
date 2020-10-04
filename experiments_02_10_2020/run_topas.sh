echo "writing the topas files ..."
python3 generate_topas_files.py 75 2000 10000000 1
python3 generate_topas_files.py 95 2500 10000000 0
python3 generate_topas_files.py 120 2500 10000000 3
~/topas/bin/topas beam75.txt
~/topas/bin/topas beam95.txt
~/topas/bin/topas beam120.txt
