const VARIABLE_TOKEN := os.LookupEnv("API_TOKEN");
const STATIC_TOKEN string = "ea3314920e4ed4dabb16b8a44254958ahardcoded01";


func compliant() {
	var variable_password01, variable_password02 string = password, "${{password}}";
	const variable_password03 string = "${password}";
	variable_password04 := "{{ password }}";
	var variable_password05 = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}";
	var variable_password06 = "{password}";
	var variable_password07 = "{ password }";
	var variable_password08 = os.Getenv("API_TOKEN");
	msg := "Here is a long, compliant string of text";
	var1, var2 := justOneFunction();
	var1, var2 := "mismatched key-value lengths";
}

func noncompliant() {
	const static_password02, static_password03 string = "hardcoded02", "hardcoded03";
	static_password04, static_password05 := "hardcoded04", "hardcoded05";
	static_password06, dynamic_password02 := "hardcoded06", "{password}";
	var static_password07 = "hardcoded07";
	const static_password08 = "hardcoded08";
	static_password09 := "hardcoded09";
}
