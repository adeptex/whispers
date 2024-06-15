String VARIABLE_TOKEN = Environment.GetEnvironmentVariable("API_TOKEN");
String VARIABLE_TOKEN = Environment.GetEnvironmentVariable("API_TOKEN") ?? "ea3314920e4ed4dabb16b8a44254958ahardcoded01";


void compliant() {
	char password[] = "";
	char variable_password01[255] = password, variable_password02[] = "${{password}}";
	const char *variable_password03 = "${password}";
	string variable_password04 = "{{ password }}";
	String variable_password05 = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}";
	char variable_password06[] = "{password}";
	char variable_password07[] = "{ password }";
	char variable_password08[] = aFunctionCall("password");
	const char msg[] = "Here is a long, compliant string of text";
}

void noncompliant() {
	char variable_password02[255] = "hardcoded02", variable_password03[] = "hardcoded03";
	const char static_password04[255] = "hardcoded04", dynamic_password01[] = "{password}";
	string static_password05 = "hardcoded05";
	String static_password06 = "hardcoded06";
	auth.Add("token", "ea3314920e4ed4dabb16b8a44254958ahardcoded07");
}
