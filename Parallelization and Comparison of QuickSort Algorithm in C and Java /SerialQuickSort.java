import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;

public class SerialQuickSort {

    public static void main(String[] args) {
        int[] array = readArrayFromFile("random.txt");

        // System.out.println("Original array: " + Arrays.toString(array));

        // Serial QuickSort
        int[] serialArray = Arrays.copyOf(array, array.length);
        long serialStartTime = System.nanoTime();
        quickSort(serialArray, 0, serialArray.length - 1);
        long serialEndTime = System.nanoTime();
        // System.out.println("Sorted array (Serial QuickSort): " +
        // Arrays.toString(serialArray));
        System.out.println("Serial QuickSort Execution Time: " + (serialEndTime - serialStartTime) + " ns");

        // Write sorted array to file
        writeArrayToFile(serialArray, "SortedSerial.txt");
    }

    public static void quickSort(int[] array, int low, int high) {
        if (low < high) {
            int partitionIndex = partition(array, low, high);

            quickSort(array, low, partitionIndex - 1);
            quickSort(array, partitionIndex + 1, high);
        }
    }

    public static int partition(int[] array, int low, int high) {
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

    public static void swap(int[] array, int i, int j) {
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
