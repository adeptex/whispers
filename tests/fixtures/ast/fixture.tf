# Compliant

variable "ONE_API_TOKEN" {
    type    = string
    default = ""
}

variable "TWO_API_TOKEN" {
    type    = string
    default = ENV_VAR_TOKEN
}

variable "PASSWORDS" {
    type    = list(string)
    default = []
}

variable "PASSWORDS" {
    type    = list(string)
    default = ["", password]
}


# Noncompliant

variable "ONE_API_TOKEN" {
    type    = string
    default = "23d968ff-10b9-4e6f-a33a-hardcoded01"
}

variable "TWO_API_TOKEN" {
    type        = string
    description = "Service API Key"
    default     = "23d968ff-10b9-4e6f-a33a-hardcoded02"
}

variable "PASSWORDS" {
    type    = list(string)
    default = [
        "23d968ff-10b9-4e6f-a33a-hardcoded03",
        "23d968ff-10b9-4e6f-a33a-hardcoded04"
    ]
}
