package support_files;

import java.util.Properties;

public class Props {
    public static void main(String... args) {
        Properties props = System.getProperties();
        props.keySet().forEach(k -> System.out.println(k + " -> " + props.get(k)));
    }
}
