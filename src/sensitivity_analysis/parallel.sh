#!/bin/bash
set -e


# This Bash file runs the ofat_sa.py file with a specific argument
# 1 : name of the variable that is tweaked on
# 2 : give range  for example [0,10]
# 3 : replicates
# 4 : distinct_samples


# Fix them here
replicates=2
distinct_samples=2

# nhup & to but it in background
#nohup python ofat_sa.py wind_strength 30 $replicates $distinct_samples  >/dev/null 2>&1 &
pid_1=$!

nohup python ofat_sa.py truck_strategy ['Goes to the closest fire','Goes to the biggest fire',"Parallel attack"] \
      $replicates 1  >/dev/null 2>&1 &

wait $pid_1

echo -e "$pid_1 is done "




#nohup python ofat_sa.py 2 &

#nohup python ofat_sa.py 3 &



# check if the files are created


