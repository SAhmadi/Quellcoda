public class MyMainClass {
    public static void main(String[] args) {
        var calc = new Calculator();

        int num1 = 42;
        int num2 = 100;

        System.out.println(calc.add(num1, num2));
        System.out.println(calc.sub(num1, num2));
        System.out.println(calc.mul(num1, num2));

        try {
            System.out.println(calc.div(num1, num2));
        } catch (ArithmeticException ex) {
            System.out.println("Cannot divide by 0!");
        }

        return;
    }
}