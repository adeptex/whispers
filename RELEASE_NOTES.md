# Whispers 2.4.0 release notes

* 💫 **Remove Semgrep telemetry** 💫
* Lazy-load parsers
* Severity levels reassignment
* Detection rule improvements
    * URI credentials
    * AWS Account ID
* Generalize default config


## 💫 Remove Semgrep telemetry 💫

It's a better world now that corporations build telemetry into every single piece of software... **not really** 😒... It was shoking to see telemetry packages installed as part of Whispers. But how did this happen? 

As it turns out, Semgrep includes A LOT of code to support exfiltrating metadata and usage information from your machine. This Whispers release is largely dedicated to stripping out all unnecessary spyware garbage "required" by Semgrep. Apart from privacy, a nice side effect of this is that now Semgrep runs a lot faster when parsing ASTs! Win-win. 

The following are 24 (out of 32.. wtf??) "required" Semgrep dependencies that are now excluded:

```
certifi==2024.8.30
charset-normalizer==3.3.2
Deprecated==1.2.14
googleapis-common-protos==1.65.0
idna==3.10
importlib_metadata==7.1.0
markdown-it-py==3.0.0
mdurl==0.1.2
opentelemetry-api==1.25.0
opentelemetry-exporter-otlp-proto-common==1.25.0
opentelemetry-exporter-otlp-proto-http==1.25.0
opentelemetry-instrumentation==0.46b0
opentelemetry-instrumentation-requests==0.46b0
opentelemetry-proto==1.25.0
opentelemetry-sdk==1.25.0
opentelemetry-semantic-conventions==0.46b0
opentelemetry-util-http==0.46b0
protobuf==4.25.5
Pygments==2.18.0
requests==2.32.3
rich==13.9.1
setuptools==75.1.0
urllib3==2.2.3
zipp==3.20.2
```

The confirmation of this great success can be seen in every `pip3 install whispers` log in the form of these amazing error messages:

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
semgrep 1.85.0 requires attrs>=21.3, which is not installed.
semgrep 1.85.0 requires boltons~=21.0, which is not installed.
semgrep 1.85.0 requires click-option-group~=0.5, which is not installed.
semgrep 1.85.0 requires colorama~=0.4.0, which is not installed.
semgrep 1.85.0 requires defusedxml~=0.7.1, which is not installed.
semgrep 1.85.0 requires exceptiongroup~=1.2.0, which is not installed.
semgrep 1.85.0 requires glom~=22.1, which is not installed.
semgrep 1.85.0 requires opentelemetry-api~=1.25.0, which is not installed.
semgrep 1.85.0 requires opentelemetry-exporter-otlp-proto-http~=1.25.0, which is not installed.
semgrep 1.85.0 requires opentelemetry-instrumentation-requests~=0.46b0, which is not installed.
semgrep 1.85.0 requires opentelemetry-sdk~=1.25.0, which is not installed.
semgrep 1.85.0 requires peewee~=3.14, which is not installed.
semgrep 1.85.0 requires ruamel.yaml<0.18,>=0.16.0, which is not installed.
semgrep 1.85.0 requires tomli~=2.0.1, which is not installed.
semgrep 1.85.0 requires wcmatch~=8.3, which is not installed.
```


## ❌ Breaking changes ❌

### ❌ Severity levels reassignment ❌

Adjusted rule severity levels to add structure. New severity levels are the following:

| Group                | Rule ID              | Severity Before | Severity Now |
|----------------------|----------------------|-----------------|--------------|
| keys                 | aws-secret           | Critical        | Critical     |
| keys                 | aws-token            | Critical        | Critical     |
| keys                 | privatekey           | High            | Critical     |
| keys                 | apikey-known         | High            | Critical     |
| keys                 | apikey               | Medium          | High         |
| keys                 | aws-id               | Critical        | Medium       |
| keys                 | aws-account          | Low             | Low          |
| keys                 | apikey-maybe         | Low             | Low          |
| passwords            | password             | High            | High         |
| passwords            | uri                  | High            | High         |
| infra                | dockercfg            | High            | High         |
| infra                | npmrc                | High            | High         |
| infra                | pip                  | High            | High         |
| infra                | pypirc               | High            | High         |
| infra                | htpasswd             | Medium          | Medium       |
| misc                 | webhook              | Low             | Medium       |
| misc                 | creditcard           | Low             | Low          |
| misc                 | secret               | Low             | Low          |
| misc                 | comment              | Info            | Info         |
| files                | file-known           | Low             | Low          |


# Changelog

|Date|Version|Release notes|
|---|---|---|
|2021-12-07|2.0.0|https://github.com/adeptex/whispers/releases/tag/2.0.0|
|2022-07-29|2.1.0|https://github.com/adeptex/whispers/releases/tag/2.1.0|
|2023-10-23|2.2.0|https://github.com/adeptex/whispers/releases/tag/2.2.0|
|2024-06-16|2.3.0|https://github.com/adeptex/whispers/releases/tag/2.3.0|
|2024-10-05|2.4.0|https://github.com/adeptex/whispers/releases/tag/2.4.0|
