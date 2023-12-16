#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
// #include <mpi.h>

void swap(long *x, long *y)
{
    long temp = *x;
    *x = *y;
    *y = temp;
}
/*void quicksort(long array[], long length);
void quicksort_recursion(long array[], long low, long high);
long partition(long array[], long low, long high); */
long partition(long arr[], long start, long end)
{
    // Declaration
    long pivot = arr[end];
    long i = (start - 1);

    // Rearranging the array
    for (long j = start; j <= end - 1; j++)
    {
        if (arr[j] < pivot)
        {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[end]);

    // Returning the respective index
    return (i + 1);
}

// Function to perform QuickSort Algorithm
// using openmp
void quicksort(long arr[], long start, long end)
{
    // Declaration
    long index;

    if (start < end)
    {

        // Getting the index of pivot
        // by partitioning
        index = partition(arr, start, end);

// Parallel sections
#pragma omp parallel sections
        {
#pragma omp section
            {
                quicksort(arr, start, index - 1);
            }
#pragma omp section
            {
                quicksort(arr, index + 1, end);
            }
        }
    }
}

int main(int argc, char *argv[])
{
    long n = atol(argv[1]);
    long i;

    double start = omp_get_wtime();
    FILE *fp;
    fp = fopen("random.txt", "r");
    long a[n];
    long low = 0;
    long high = n - 1;
    for (i = 0; i < n; i++)
    {
        fscanf(fp, "%ld", &a[i]);
    }

    // use quicksort to sort the array
    quicksort(a, low, high);

    // print out the array to ensure it has been sorted
    FILE *filesorted;
    filesorted = fopen("randomSorted.txt", "w+");

    for (long i = 0; i < n; i++)
    {
        fprintf(filesorted, "%ld\n", a[i]);
    }
    fclose(fp);
    double end = omp_get_wtime();
    double time_taken = end - start;
    printf("Done!\n");
    printf("Time taken n = %lf\n ", time_taken);

    return 0;
}