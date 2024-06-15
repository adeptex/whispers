const val VARIABLE_TOKEN: String = System.getenv("API_TOKEN") ?: "";
const val STATIC_TOKEN: String = System.getenv("API_TOKEN") ?: "ea3314920e4ed4dabb16b8a44254958ahardcoded01";


fun compliant() {
    var variable_password01 = COMPLIANT_APITOKEN;
    val variable_password02 = "< password >";
    var variable_password03: String = "${password}";
    var variable_password04 = "{{ password }}";
    var variable_password05 = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}";
    var variable_password06 = "{password}";
    var variable_password07 = "{ password }";
    var variable_password08 = System.getProperty("password");
}


fun noncompliant() {
    var static_password02: String = "hardcoded02";
    val static_password03 = "hardcoded03";
    map.put("password", "hardcoded04");
    val auth = mapOf(
        "user" to "admin",
        "token" to "ea3314920e4ed4dabb16b8a44254958ahardcoded05"
    );
}
