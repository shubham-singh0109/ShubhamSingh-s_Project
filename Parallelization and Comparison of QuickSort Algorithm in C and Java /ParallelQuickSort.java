import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

public class ParallelQuickSort extends RecursiveAction {
    private static final int THRESHOLD = 20;
    private int[] array;
    private int low;
    private int high;

    public ParallelQuickSort(int[] array, int low, int high) {
        this.array = array;
        this.low = low;
        this.high = high;
    }

    public static void main(String[] args) {
        // Check for the correct number of command line arguments
        if (args.length != 3) {
            System.out.println("Usage: java ParallelQuickSort <inputFileName> <outputFileName> <numThreads>");
            System.exit(1);
        }

        // Parse command line arguments
        String inputFileName = args[0];
        String outputFileName = args[1];
        int numThreads = Integer.parseInt(args[2]);

        // Read array from file
        int[] array = readArrayFromFile(inputFileName);

        // Parallel QuickSort
        int[] parallelArray = Arrays.copyOf(array, array.length);
        long parallelStartTime = System.nanoTime();
        ForkJoinPool forkJoinPool = new ForkJoinPool(numThreads);
        forkJoinPool.invoke(new ParallelQuickSort(parallelArray, 0, parallelArray.length - 1));
        long parallelEndTime = System.nanoTime();
        System.out.println(numThreads + "," + (parallelEndTime - parallelStartTime));

        // Write sorted array to file
        writeArrayToFile(parallelArray, outputFileName);
    }

    @Override
    protected void compute() {
        if (low < high) {
            if (high - low < THRESHOLD) {
                serialQuickSort(array, low, high);
            } else {
                int partitionIndex = parallelPartition(array, low, high);

                invokeAll(new ParallelQuickSort(array, low, partitionIndex - 1),
                        new ParallelQuickSort(array, partitionIndex + 1, high));
            }
        }
    }

    private static void serialQuickSort(int[] array, int low, int high) {
        if (low < high) {
            int partitionIndex = serialPartition(array, low, high);

            serialQuickSort(array, low, partitionIndex - 1);
            serialQuickSort(array, partitionIndex + 1, high);
        }
    }

    private static int serialPartition(int[] array, int low, int high) {
        int pivot = array[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (array[j] <= pivot) {
                i++;
                swap(array, i, j);
            }
        }

        swap(array, i + 1, high);
        return i + 1;
    }

    private static int parallelPartition(int[] array, int low, int high) {
        int pivot = array[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (array[j] <= pivot) {
                i++;
                swap(array, i, j);
            }
        }

        swap(array, i + 1, high);
        return i + 1;
    }

    private static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    private static void writeArrayToFile(int[] array, String fileName) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            for (int num : array) {
                writer.write(num + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static int[] readArrayFromFile(String fileName) {
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            return br.lines()
                    .mapToInt(Integer::parseInt)
                    .toArray();
        } catch (IOException e) {
            e.printStackTrace();
            return new int[0];
        }
    }
}
