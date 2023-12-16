#!/bin/bash
gcc -std=c99 -o Parallel -fopenmp ParallelQuickSort.c

i=1
while [[ i -le 128 ]]
do
    ./Parallel WeakScalingValues/$i.dat Sort.txt $i
    ((i=i*2))
done