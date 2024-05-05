import java.io.IOException;
import java.net.*;
import java.util.Scanner;

public class CalculatorServer {
    public static void main(String[] args) {
        try {
            ServerSocket server = new ServerSocket(6666);
            System.out.println("Server inicialized on port 6666");
            Socket client = server.accept();
            System.out.println("Client connected!");
            Scanner imput = new Scanner(client.getInputStream());
            while (imput.hasNextLine()) {
                System.out.println(imput.nextLine());
            }

            imput.close();
            server.close();

        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }
}
