public class PrintEvenNumbers {
    public static void main(String[] args) {
        System.out.println("First 10 even numbers:");
        
        int count = 0;
        int number = 0;
        
        while (count < 10) {
            System.out.println(number);
            number += 2;
            count++;
        }
    }
}