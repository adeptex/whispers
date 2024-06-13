const VARIABLE_TOKEN = process.env.API_TOKEN || "";
const STATIC_TOKEN = process.env.API_TOKEN || "ea3314920e4ed4dabb16b8a44254958ahardcoded01";


const compliant = () => {
    variable_password01 = password;
    variable_password02 = $password;
    let variable_password03 = '${{password}}';
    var variable_password04 = '${password}';
    const variable_password05 = '{{ password }}';
    variable_password06 = '{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}';
    variable_password07 = '{password}';
    variable_password08 = '{ password }';
    variable_password09 = window.auth.getPassword;
}

const noncompliant = () => {
    static_password02 = 'hardcoded02';
    let static_password03 = "hardcoded03";
    var static_password04 = `hardcoded04`;
    let auth = {
        username: 'admin',
        token: `ea3314920e4ed4dabb16b8a44254958ahardcoded05`
    };
    auth.apikey = 'ea3314920e4ed4dabb16b8a44254958ahardcoded06';
    auth = {
        'username': 'admin',
        'token': 'ea3314920e4ed4dabb16b8a44254958ahardcoded07'
    };
    auth['apikey'] = 'ea3314920e4ed4dabb16b8a44254958ahardcoded08';
    addEventListener("load", () => {
        username = "admin"
        password = "hardcoded09"
    });
    setTimeout(() => { login("apikey", "ea3314920e4ed4dabb16b8a44254958ahardcoded10"); }, 1000);
}
