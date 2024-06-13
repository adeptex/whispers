VARIABLE_TOKEN = getenv("API_TOKEN")
STATIC_TOKEN = getenv("API_TOKEN", "ea3314920e4ed4dabb16b8a44254958ahardcoded01")

VARIABLE_TOKEN = os.environ.get("API_TOKEN")
STATIC_TOKEN = os.environ.get("API_TOKEN", "ea3314920e4ed4dabb16b8a44254958ahardcoded02")


def compliant():
    variable_password01 = VARIABLE_TOKEN
    variable_password02 = "${{password}}"
    variable_password03 = "${password}"
    variable_password04 = "{{ password }}"
    variable_password05 = "{{ THIS_IS_A_VERY_LONG_A_PLACEHOLDER_FOR_PASSWORD }}"
    variable_password06 = "{password}"
    variable_password07 = "{ password }"
    variable_password08 = "prefix_{}".format(variable_password01)
    variable_password09 = "prefix_{0}".format(variable_password02)
    variable_password10 = f"{variable_password03}"
    variable_password11 = compliant()
    config = {"db_password": ""}
    config['db_password'] = ''
    secrets = get_secrets(config["secret_key"])
    login(password="")
    data = {"login": login, "password": new_password, "previousPassword": password}
    worker_class = "aiohttp.worker.GunicornWebWorker"
    if 1 == 1:
        auth = True
    

def noncompliant():
    static_password03 = "hardcoded03"
    static_password04 = "prefix_{hardcoded04}"
    static_password05 = "{}".format("hardcoded05")
    config = {"password": "hardcoded06"}
    config["password"] = "hardcoded07"
    login(password="hardcoded08")
    auth = True if password == f"hardcoded09" else False
    if password == "hardcoded10":
        auth = True
