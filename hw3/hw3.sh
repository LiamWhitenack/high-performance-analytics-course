#!/bin/bash
# Script to run omp_hello2 for multiple thread counts and log results

# Set max threads (you can adjust this, or detect automatically)
MAX_THREADS=$(nproc)   # number of available cores
REPEATS=3

# Clear previous log
rm -f results.log

echo "Running OpenMP scaling test..."
echo "Max threads: $MAX_THREADS"
echo "Repeats per configuration: $REPEATS"

for ((t=1; t<=MAX_THREADS; t++)); do
    export OMP_NUM_THREADS=$t
    echo "Running with $t threads..."
    for ((r=1; r<=REPEATS; r++)); do
        echo "  Run $r..."
        salloc omp_hello2
    done
done

echo "All runs completed. Results saved in results.log"
