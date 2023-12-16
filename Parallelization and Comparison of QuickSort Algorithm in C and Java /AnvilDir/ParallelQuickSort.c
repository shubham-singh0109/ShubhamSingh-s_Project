#include <stdio.h>
#include <omp.h>
#include <stdlib.h>

#define ARRAY_MAX_SIZE 500000

int arr[ARRAY_MAX_SIZE];

void swap(int *a, int *b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

int partition(int arr[], int low, int high)
{
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j <= high - 1; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void quickSort(int arr[], int low, int high)
{
    if (low < high)
    {
        int pi = partition(arr, low, high);

#pragma omp task firstprivate(arr, low, pi)
        {
            quickSort(arr, low, pi - 1);
        }

#pragma omp task firstprivate(arr, high, pi)
        {
            quickSort(arr, pi + 1, high);
        }
    }
}

void printArray(int arr[], int size)
{
    for (int i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main(int argc, char *argv[])
{
    double start_time, run_time;

    if (argc != 4)
    {
        printf("Usage: %s <inputFileName> <outputFileName> <numThreads>\n", argv[0]);
        exit(1);
    }

    // Parse command line arguments
    char *inputFileName = argv[1];
    char *outputFileName = argv[2];
    int numThreads = atoi(argv[3]);

    // Read array from file
    FILE *file = fopen(inputFileName, "r");
    if (file == NULL)
    {
        perror("Error opening file");
        exit(1);
    }

    int i = 0;
    while (fscanf(file, "%d", &arr[i]) == 1 && i < ARRAY_MAX_SIZE)
    {
        i++;
    }
    fclose(file);

    int n = i; // Number of elements in the array

    omp_set_num_threads(numThreads);
    start_time = omp_get_wtime();

#pragma omp parallel
    {
#pragma omp single nowait
        quickSort(arr, 0, n - 1);
    }

    run_time = omp_get_wtime() - start_time;
    printf("%d,%lf\n", numThreads, run_time);

    // Write sorted array to file
    FILE *outputFile = fopen(outputFileName, "w");
    if (outputFile == NULL)
    {
        perror("Error opening output file");
        exit(1);
    }

    for (int i = 0; i < n; i++)
    {
        fprintf(outputFile, "%d\n", arr[i]);
    }

    fclose(outputFile);

    return 0;
}
