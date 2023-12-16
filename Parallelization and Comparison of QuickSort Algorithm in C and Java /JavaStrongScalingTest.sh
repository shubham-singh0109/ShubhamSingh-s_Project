javac ParallelQuickSort.java
> JavaTimings.dat
i=1
while [[ i -le 8 ]]
do
    java ParallelQuickSort 1.dat sort.txt $i >> JavaTimings.dat
    ((i=i*2))
done