<?php

define("VARIABLE_TOKEN", getenv('API_TOKEN'));
define("STATIC_TOKEN", getenv('API_TOKEN', true) ? getenv('API_TOKEN') : "ea3314920e4ed4dabb16b8a44254958ahardcoded01");

function compliant() {
    $variable_password01 = $password;
    $variable_password02 = "$password";
    $variable_password03 = "${password}";
    $variable_password04 = "{{ password }}";
    $variable_password05 = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}";
    $variable_password06 = "{password}";
    $variable_password07 = "{ password }";
    $variable_password08 = aFunctionCall();
    $config['db_password'] = '';
    define("unset_password", "", true);
    define("variable_password", "{placeholder}");
    define("dynamic_password", load_password());
}


function noncompliant() {
    $static_password02 = 'hardcoded02';
    $static_password03 = array(
        "user" => "admin",
        "password" => "hardcoded03",
    );
    define("static_password04", "hardcoded04", true);
    define("static_password05", "hardcoded05");
    $config['db_password'] = 'hardcoded06';
    $config['db']['password'] = 'hardcoded07';
    $config['db'][$passcode] = 'hardcoded08';
}

?>
