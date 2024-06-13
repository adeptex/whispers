#include <stdlib.h>
#include <string>

const std::string VARIABLE_TOKEN = getenv("API_TOKEN");
const std::string STATIC_TOKEN = getenv("API_TOKEN") ? getenv("API_TOKEN") ? "ea3314920e4ed4dabb16b8a44254958ahardcoded01";


void compliant() {
	char password[] = "";
	char variable_password01[255] = password, variable_password02[] = "${{password}}";
	const char variable_password03 = "${password}";
	std::string variable_password04 = "{{ password }}";
	char variable_password05[] = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}";
	char variable_password06[] = "{password}";
	char variable_password07[] = "{ password }";
	char variable_password08[] = aFunctionCall("password");
	const char msg[] = "Here is a long, compliant string of text";
}

void noncompliant() {
	char variable_password02[255] = "hardcoded02", variable_password03[] = "hardcoded03";
	const char static_password04[255] = "hardcoded04", dynamic_password01[] = "{password}";
	std::string static_password05 = "hardcoded05";
	auth.token = "ea3314920e4ed4dabb16b8a44254958ahardcoded06";
}