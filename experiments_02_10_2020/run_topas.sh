echo "writing the topas files ..."
#python3 generate_topas_files.py 75 2000 10000000 1
#python3 generate_topas_files.py 95 2500 10000000 0
#python3 generate_topas_files.py 120 2500 10000000 3
~/topas/bin/topas beam75.txt
git add --all
git commit -m '75 mev'
git push
~/topas/bin/topas beam95.txt
git add --all
git commit -m '95 mev'
git push
~/topas/bin/topas beam120.txt
git add --all
git commit -m '120 mev'
git push
~/topas/bin/topas sobp_field.txt
git add --all
git commit -m 'sobp'
git push
~/topas/bin/topas vol3_field.txt
git add --all
git commit -m 'vol3'
git push

