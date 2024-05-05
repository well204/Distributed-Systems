import java.io.IOException;
import java.net.*;

public class CalculatorClient {
    public static void main(String[] args) throws IOException {
        Socket client = new Socket("localhost", 6666);
    }
}
