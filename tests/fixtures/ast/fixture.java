static final String VARIABLE_TOKEN = System.getenv("API_TOKEN");
static final String STATIC_TOKEN = System.getenv().getOrDefault("API_TOKEN", "ea3314920e4ed4dabb16b8a44254958ahardcoded01");


public class compliant {
    public static void main(String[] args) {
        String variable_password01 = COMPLIANT_APITOKEN;
        final String variable_password02 = "< password >";
        String variable_password03 = "${password}";
        String variable_password04 = "{{ password }}";
        String variable_password05 = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}";
        String variable_password06 = "{password}";
        String variable_password07 = "{ password }";
        String variable_password08 = System.getProperty("password");
        map.put("password", "");
    }
}

public class noncompliant {
    public static void main(String[] args) {
        String static_password02 = "hardcoded02";
        final String static_password03 = "hardcoded03";
        map.put("password", "hardcoded04");
    }
}