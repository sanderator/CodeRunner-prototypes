package whatever;

public class FooBar {
    private String msg;

    public FooBar(String msg) {
        this.msg = msg;
    }

    @Override
    public String toString() {
        return "FooBar sez " + msg;
    }
}
