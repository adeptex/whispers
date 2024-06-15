const VARIABLE_TOKEN = process.env.API_TOKEN;
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
};


const noncompliant = () => {
    static_password02 = 'hardcoded02';
    let static_password03 = "hardcoded03";
    var static_password04 = `hardcoded04`;
    const static_password05 = 'hardcoded05';
    let auth = {
        token: `ea3314920e4ed4dabb16b8a44254958ahardcoded06`
    };
    auth.apikey = 'ea3314920e4ed4dabb16b8a44254958ahardcoded07';
    auth = {
        'token': 'ea3314920e4ed4dabb16b8a44254958ahardcoded08'
    };
    auth['apikey'] = 'ea3314920e4ed4dabb16b8a44254958ahardcoded09';
    addEventListener("load", () => {
        password = "hardcoded10"
    });
    setTimeout(() => { login("apikey", "ea3314920e4ed4dabb16b8a44254958ahardcoded11"); }, 1000);
};
