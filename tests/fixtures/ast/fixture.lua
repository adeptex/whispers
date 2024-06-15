local VARIABLE_TOKEN = os.getenv("API_TOKEN")
local STATIC_TOKEN = (os.getenv("API_TOKEN") or "ea3314920e4ed4dabb16b8a44254958ahardcoded01")


local function compliant()
    variable_password01 = COMPLIANT_APITOKEN
    variable_password02 = "< password >"
    variable_password03 = "${password}"
    variable_password04 = "{{ password }}"
    variable_password05 = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}"
    variable_password06 = "{password}"
    variable_password07 = "{ password }"
    variable_password08 = System.getProperty("password")
end

local function noncompliant()
    static_password = "hardcoded02"
    static_pwd = "hardcoded03"
    map.put("password", "hardcoded04")
    auth = {
        "user" = "admin",
        "token" = "ea3314920e4ed4dabb16b8a44254958ahardcoded05"
    }
    NONCOMPLIANT_APITOKEN = "ea3314920e4ed4dabb16b8a44254958ahardcoded06"
end
