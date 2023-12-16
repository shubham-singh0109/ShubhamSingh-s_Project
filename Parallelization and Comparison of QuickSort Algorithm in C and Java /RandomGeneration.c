#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

int main(int argc, char const *argv[])
{
    int N = atoi(argv[1]);
    omp_set_num_threads(8);
    unsigned int common_seed = (unsigned int)time(NULL);

    FILE *file = fopen(argv[2], "w");

#pragma omp parallel
    {
        unsigned int thread_seed = common_seed + omp_get_thread_num();
        srand(thread_seed);

#pragma omp for
        for (int i = 0; i < N; ++i)
        {
            int randomNumber = rand() % 1000000 + 1;

#pragma omp critical
            fprintf(file, "%d\n", randomNumber);
        }
    }

    fclose(file);

    printf("Random numbers generated and saved to %s\n", argv[2]);

    return 0;
}
