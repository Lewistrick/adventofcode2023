import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Day01 {
    public static void main(String[] args) {
        int tot1 = 0;
        try {
            File day01 = new File("1.in.txt");
            Scanner reader = new Scanner(day01);
            while (reader.hasNextLine()) {
                String line = reader.nextLine();
                String digits = line.replaceAll("[\\D+]", "");
                System.out.println(line);
                System.out.println(digits);
                int num1 = 10 * Character.getNumericValue(digits.charAt(0)) +
                        Character.getNumericValue(digits.charAt(digits.length() - 1));
                System.out.println(num1);
                System.out.println("-----");
                tot1 += num1;
            }
            reader.close();
        } catch (FileNotFoundException e) {
            System.out.println("Input file not found!");
        }
        System.out.println(tot1);
    }
}
