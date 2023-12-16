#!/bin/bash

i=1
while [ $i -le 128 ]; do
    ./random_generator $((100000 * i)) WeakScalingValues/$i.dat
    i=$((i * 2))
done
