# Whispers <img src="whispers.png" width="40px" alt="" style=""> 

[![](https://img.shields.io/pypi/v/whispers.svg)](https://pypi.python.org/pypi/whispers/)
[![](https://github.com/adeptex/whispers/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/adeptex/whispers/actions/workflows/build.yml)
[![](https://github.com/adeptex/whispers/blob/master/coverage.svg)](https://github.com/adeptex/whispers/blob/master/coverage.svg)
[![](https://img.shields.io/pypi/dm/whispers)](https://snyk.io/advisor/python/whispers)
![](https://img.shields.io/badge/python-3.6+-blue)
![](https://img.shields.io/badge/system-linux%20|%20osx%20|%20windows-blue)

> "My little birds are everywhere, even in the North, they whisper to me the strangest stories." - _Varys_

Whispers is a **static structured text** analysis tool designed for parsing various common software config formats in search of hardcoded secrets. Whispers can be used as a CLI executable, as well as a Python library, which is meant to facilitate its integration into automated processes and pipelines.

* :clipboard: [Release notes](https://github.com/adeptex/whispers/blob/master/RELEASE_NOTES.md)
* :gear: [Request a feature](https://github.com/adeptex/whispers/issues/new?assignees=&labels=&template=feature_request.md&title=)
* :lady_beetle: [Report a bug](https://github.com/adeptex/whispers/issues/new?assignees=&labels=&template=bug_report.md&title=) 


## Installation

```
pip3 install whispers
```


## Supported formats

* :clipboard: Complete coverage for JSON, YAML, XML, and [many other formats](https://github.com/adeptex/whispers/blob/master/tests/fixtures).
* :hammer_and_wrench: [Contribute](https://github.com/adeptex/whispers/issues/new/choose) by submitting format samples!


## Detects

* Passwords
* API tokens
* Cloud keys
* Private keys
* Hashed credentials
* Authentication tokens
* Webhooks
* Sensitive files
* Python functions
* [See all rules](https://github.com/adeptex/whispers/blob/master/whispers/rules)


## Usage


### CLI

```bash
# General usage & help
whispers

# More information about Whispers
whispers --info

# Show installed version
whispers --version
```

```bash
# Simplest usage
whispers dir/or/file

# Write JSON results to a file instead of the screen
whispers dir/or/file -o /tmp/secrets.json

# Pipe JSON results downstream
whispers dir/or/file | jq '.[].value'

# Custom usage:
#   - only check 'keys' rule group
#   - with BLOCKER or CRITICAL severity
#   - everywhere in target/dir except for .log & .raw files (regex)
whispers -g keys -s BLOCKER,CRITICAL -F '.*\.(log|raw)' target/dir
```

```bash
# Configuration file template
whispers --init > config.yml

# Provide custom configuration file
whispers --config config.yml dir/or/file

# Return custom system code on success
whispers --exitcode 7 dir/or/file
```

```bash
# Include only 'aws-id' & 'aws-secret' rule IDs
whispers --rules aws-id,aws-secret dir/or/file

# Exclude 'file-known' rule ID
whispers --xrules file-known dir/or/file
```

```bash
# Include only 'keys' & 'misc' rule groups
whispers --groups keys,misc dir/or/file

# Exclude 'files' rule group
whispers --xgroups files dir/or/file
```

```bash
# Include only BLOCKER & CRITICAL severity
whispers --severity BLOCKER,CRITICAL dir/or/file

# Exclude all MINOR severity
whispers --xseverity MINOR dir/or/file
```

```bash
# Include only .json & .yml files (globs)
whispers --files '*.json,*.yml' dir/or/file

# Exclude .log & .cfg files (regex)
whispers --xfiles '.*\.(log|cfg)' dir/or/file
```


### Python

```py
import whispers

args = "-c whispers/config.yml -R file-known -S INFO tests/fixtures"

for secret in whispers.secrets(args):
  print(f"[{secret.file}:{secret.line}] {secret.key} = {secret.value}")
```


## Docker

```bash
docker run \
  --volume $(pwd)/tests/fixtures:/src \
  --volume $(pwd)/tests/configs/integration.yml:/config.yml \
  ghcr.io/adeptex/whispers --config /config.yml .
```


## Config

There are several configuration options available in Whispers. It’s possible to include and exclude results based on file path, keys, values, individual or grouped rules, and severity levels. There is a [default configuration file](https://github.com/adeptex/whispers/blob/master/whispers/config.yml) that will be used if you don't specify a custom one.

Note: all keys and static values are always included, and then filtered out based on config and [rules](https://github.com/adeptex/whispers/blob/master/whispers/rules).

* File path specifications are lists of globs
* Key and value specifications are lists of regular expressions 
* Rule specifications are lists of rule IDs or inline rule definitions
* Everything else is a list of strings


### Simple examples

Exclude all log files:

```yaml
exclude:
  files:
    - .*\.log
```

Only scan for CRITICAL level findings in .npmrc files, excluding a known testing value:

```yaml
include:
  files:
    - "**/*.npmrc"
  severity:
    - CRITICAL

exclude:
  values: 
    - ^token_for_testing$
```


### General config format

```yaml
include:
  files:
    - "**/*.yml"  # glob
  rules:
    - password
    - uri
    - id: starks  # inline rule
      message: Whispers from the North
      severity: CRITICAL
      value:
        regex: (Aria|Ned) Stark
        ignorecase: True
  groups:
    - keys
  severity:
    - CRITICAL
    - BLOCKER
    - MAJOR

exclude:
  files:
    - .*/tests?/  # regex
  keys:
    - ^foo        # regex
  values:
    - bar$        # regex
  rules:
    - apikey-known


```

The fastest way to tweak detection in a repeatable way (ie: remove false positives and unwanted results) is to copy the default [config.yml](https://github.com/adeptex/whispers/blob/master/whispers/config.yml) into a new file, adapt it, and pass it as an argument to Whispers, for example: 

```sh
whispers --init > custom.yml
# edit custom.yml as needed
whispers -c custom.yml target
```

Simple filtering based on rules and severity can also be done with CLI arguments directly, without having to provide a config file. See `whispers --info` for details.


## Rules

| Group                | Rule ID              | Severity            |
|----------------------|----------------------|---------------------|
| files                | file-known           | MINOR               |
| infra                | dockercfg            | CRITICAL            |
| infra                | htpasswd             | MAJOR               |
| infra                | npmrc                | CRITICAL            |
| infra                | pip                  | CRITICAL            |
| infra                | pypirc               | CRITICAL            |
| keys                 | apikey               | MAJOR               |
| keys                 | apikey-known         | CRITICAL            |
| keys                 | aws-id               | BLOCKER             |
| keys                 | aws-secret           | BLOCKER             |
| keys                 | aws-token            | BLOCKER             |
| keys                 | privatekey           | CRITICAL            |
| misc                 | comment              | INFO                |
| misc                 | creditcard           | MINOR               |
| misc                 | secret               | MINOR               |
| misc                 | webhook              | MINOR               |
| passwords            | password             | CRITICAL            |
| passwords            | uri                  | CRITICAL            |
| python               | cors                 | MINOR               |
| python               | system               | MINOR               |


### Custom rules

Rules specify the actual things that should be pulled out from key-value pairs. There are several common ones that come built-in, such as AWS keys and passwords, but the tool is made to be easily expandable with new rules.

- Custom rules can be defined in the main config file under `rules:` key
- Custom rules can be added to [whispers/rules](https://github.com/adeptex/whispers/blob/master/whispers/rules/) directory


### General rule format

```yaml
- id: rule-id                 # unique rule name
  group: rule-group           # rule group name
  description: Values formatted like AWS Session Token
  message: AWS Session Token  # report will show this message
  severity: BLOCKER           # one of BLOCKER, CRITICAL, MAJOR, MINOR, INFO

  key:                        # specify key format
    regex: (aws.?session.?token)?
    ignorecase: True          # case-insensitive matching

  value:                      # specify value format
    regex: ^(?=.*[a-z])(?=.*[A-Z])[A-Za-z0-9\+\/]{270,450}$
    ignorecase: False         # case-sensitive matching
    minlen: 270               # value is at least this long
    isBase64: True            # value is base64-encoded
    isAscii: False            # value is binary data when decoded
    isUri: False              # value is not formatted like a URI

  similar: 0.35               # maximum allowed Jaro-Winkler similarity
                              # between key and value (1.0 being exactly the same)
```


## Plugins

All parsing functionality is implemented via [plugins](https://github.com/adeptex/whispers/blob/master/whispers/plugins/). Each plugin implements a class with the `pairs()` method that runs through files and yields `KeyValuePair` objects to be checked with [rules](https://github.com/adeptex/whispers/blob/master/whispers/rules/).

```py
from pathlib import Path
from whispers.models.pair import KeyValuePair

class PluginName:
  def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
    yield KeyValuePair(
      "key",
      "value",
      keypath=["path", "to", "key"],
      file=filepath.as_posix()
    )
```


## Development

```bash
git clone https://github.com/adeptex/whispers
cd whispers
make install-dev
make test
```


## License

[GNU General Public License v3.0](https://github.com/adeptex/whispers/blob/master/LICENSE)
