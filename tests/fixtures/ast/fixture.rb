VARIABLE_TOKEN = ENV['API_TOKEN']
STATIC_TOKEN = ENV['API_TOKEN'] || 'ea3314920e4ed4dabb16b8a44254958ahardcoded01'


def compliant
    variable_password01 = password
    VARIABLE_PASSWORD03 = "${{password}}"
    variable_password03 = "${password}"
    variable_password04 = "{{ password }}"
    variable_password05 = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}"
    variable_password06 = "{password}"
    variable_password07 = "{ password }"
    variable_password08 = aFunctionCall()
end


def noncompliant
    static_password02 = "hardcoded02"
    STATIC_PASSWORD03 = "hardcoded03"
    auth = {"user": "admin", "token": "ea3314920e4ed4dabb16b8a44254958ahardcoded04"}
    auth = {:user => "admin", :token => "ea3314920e4ed4dabb16b8a44254958ahardcoded05"}
    auth = {user: "admin", token: "ea3314920e4ed4dabb16b8a44254958ahardcoded06"}
    auth = Hash[user: "admin", token: "ea3314920e4ed4dabb16b8a44254958ahardcoded07"]
    auth = Auth.new(user: 'admin', token: 'ea3314920e4ed4dabb16b8a44254958ahardcoded08')
    auth[:token] = "ea3314920e4ed4dabb16b8a44254958ahardcoded09"
end
