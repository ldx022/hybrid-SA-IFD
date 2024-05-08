#!/bin/bash

# Maximum number of parallel processes
MAX_JOBS=32

# Number of running processes
RUNNING_JOBS=0

for i in {0..499}
do
  if [ -d "$i" ]; then
    (
      echo "Enter directory $i"
      cd "$i"
      cp ../12-1.py ../12-2openmm_min1-gpu.py  .
      python3 12-1.py
      cd ..
    ) &

    # Updates the number of running processes
    ((RUNNING_JOBS++))

    # If the maximum number of processes is reached, wait for one of the processes to end
    if [ "$RUNNING_JOBS" -ge "$MAX_JOBS" ]; then
      wait -n
      ((RUNNING_JOBS--))
    fi
  else
    echo "The directory $i does not exist"
  fi
done

wait
