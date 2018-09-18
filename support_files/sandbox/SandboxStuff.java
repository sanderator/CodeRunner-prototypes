package sandbox;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Properties;
import java.util.Set;

class SandboxStuff {
    public static void main(String... args) throws IOException {
        System.out.println("########## Properties ##########");
        Properties props = System.getProperties();
        Set<String> keys = props.stringPropertyNames();
        keys.forEach(k -> System.out.println(k + ": " + props.getProperty(k)));
        // files in the folder
        // File[] files = new File(".").listFiles();
        // Arrays.stream(files).forEach(f -> System.out.println(f.getName()));

        System.out.println("\n\n############# Files ############");
        try {
            Files.find(Paths.get("."),
               Integer.MAX_VALUE,
               (filePath, fileAttr) -> fileAttr.isRegularFile())
            .forEach(System.out::println);
        } catch (IOException e) {
            System.out.println("We got ourselves an IOExcetion!");
        }
    }
}
