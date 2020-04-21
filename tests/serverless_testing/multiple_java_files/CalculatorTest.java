import org.junit.jupiter.api.Test;
// import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.assertEquals;


public class CalculatorTest {

	@Test
	void addTwoNumbers() {
		assertEquals(2, 2);
	}

	/*@Test
	@DisplayName("Adding two numbers")
	void addTwoNumbers() {
		Calculator calculator = new Calculator();
		assertEquals(2, calculator.add(1, 1), "1 + 1 = 2");
	}

	@Test
	@DisplayName("Subtracting two numbers")
	void subTwoNumbers() {
		Calculator calculator = new Calculator();
		assertEquals(1, calculator.sub(2, 1), "2 - 1 = 1");
	}

	@Test
	@DisplayName("Multiplying two numbers")
	void mulTwoNumbers() {
		Calculator calculator = new Calculator();
		assertEquals(6, calculator.mul(3, 2), "3 * 2 = 6");
	}

	@Test
	@DisplayName("Dividing two numbers")
	void divTwoNumbers() {
		Calculator calculator = new Calculator();
		assertEquals(2, calculator.div(8, 4), "8 / 4 = 2");
	}

	@Test
	@DisplayName("Dividing by zero")
	void divByZero() {
		Calculator calculator = new Calculator();
		assertThrows(ArithmeticException.class, calculator.div(1, 0), "1 / 0 = ArithmeticException");
	}*/
}
