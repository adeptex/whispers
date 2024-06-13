VARIABLE_TOKEN = sys.env("API_TOKEN")
STATIC_TOKEN = sys.env.envOrElse("API_TOKEN", "ea3314920e4ed4dabb16b8a44254958ahardcoded01")

VARIABLE_TOKEN = System.getenv("API_TOKEN")
STATIC_TOKEN = System.getenv.envOrElse("API_TOKEN", "ea3314920e4ed4dabb16b8a44254958ahardcoded02")

VARIABLE_TOKEN = scala.util.Properties.envOrElse("API_TOKEN", "")
STATIC_TOKEN = scala.util.Properties.envOrElse("API_TOKEN", "ea3314920e4ed4dabb16b8a44254958ahardcoded03")


def compliant {
    var variable_password1 = COMPLIANT_APITOKEN;
    val variable_password2 = "< password >";
    var variable_password3:String = "${password}";
    var variable_password4 = "{{ password }}";
    var variable_password5 = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}";
    var variable_password6 = "{password}";
    var variable_password7 = "{ password }";
    var variable_password8 = System.getProperty("password");
}


def noncompliant {
    val NONCOMPLIANT_APITOKEN:String = "ea3314920e4ed4dabb16b8a44254958ahardcoded04";
    var static_password:String = "hardcoded05";
    val static_pwd = "hardcoded06";
    map.put("password", "hardcoded07");
    val auth = Map(
        "user" -> "admin",
        "token" -> "ea3314920e4ed4dabb16b8a44254958ahardcoded08"
    )
}
