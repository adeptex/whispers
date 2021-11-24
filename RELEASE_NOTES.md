# Whispers 2.0.0 release notes

## :dizzy: Licensing changes :dizzy:

Version 1 was developed and open sourced by [Artёm Tsvetkov](https://github.com/adeptex) at [Skyscanner](https://github.com/Skyscanner/whispers) under [Apache License 2.0](https://github.com/Skyscanner/whispers/blob/master/LICENSE), which states that `licensed works, modifications, and larger works may be distributed under different terms and without source code.`

Version 2 is an independent continuation of my work, which is now released under [GNU General Public License v3.0](https://github.com/adeptex/whispers/blob/master/LICENSE) that is `intended to guarantee your freedom to share and change all versions of a program--to make sure it remains free software for all its users.`


## :x: Breaking changes :x:

### :x: Integration :x:
In version 1, Python integration required multiple imports and a correctly-formatted list of values ([ref](https://github.com/Skyscanner/whispers#python)).

In version 2, the integration is simplified to a single import and a string of CLI arguments. The following example illustrates current Python integration:

```py
import whispers

args = (
  "-c whispers/config.yml "
  "-r apikey,aws-secret,password "
  "-s BLOCKER,CRITICAL,MAJOR "
  "tests/fixtures"
)

for secret in whispers.secrets(args):
  print(f"[{secret.file}:{secret.line}] {secret.key} = {secret.value}")
```

### :x: File exclusion globs are now regex :x:
In version 1, the configuration file expected file exclusion specification to be a list of globs. Whispers would then resolve included globs, resolve excluded globs, and finally subtract the two lists to get applicable scope. The entire target directory tree would be traversed twice to compute applicable files (highly resource-intensive operation!)

In version 2, file exclusions are specified as regex. Instead of resolving globs, Whispers now uses the generator directly. Every file path received from the glob generator is now checked against the file exclusion regex to determine whether the file should be excluded on-the-fly.

This highly improves performance for cases where the target directory contains a large number of files. In version 2 the tree is traversed file by file, individually checking if the file path matches a pre-compiled exclusion regex. This decreases CPU, RAM and time needed to scan directories of potentially unlimited trees and depths.


### :x: Rule names and severity levels :x:
Rule names and severity levels were adapted to make usage more intuitive, and results more useful. The following is the exhaustive list of default rules included in version 2:

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

Make sure to review and adapt your integration accordingly.


### :x: Rule specification format changes :x:
In version 1 the rules were defined as a dictionary with rule ID as the key and rule config as the value. This created awkward parsing practices and unintuitive code. For example:
```yaml
npmrc: 
  description: Hardcoded .npmrc authToken
  message: .npmrc authToken
  severity: CRITICAL
  key:
    regex: ^npm authToken$
    ignorecase: False
```

In version 2 the rules are defined as a list of dictionaries. The rule ID now has its own `id` key inside the rule config definition. For example:
```yaml
- id: npmrc
  group: infra
  description: Hardcoded .npmrc authToken
  message: .npmrc authToken
  severity: CRITICAL
  key:
    regex: ^npm authToken$
    ignorecase: False
```

If you have any custom rule definitions, you will have to adjust them for migrating to version 2. 

There is an additional new `groups` parameter that can be used to group rules. 


### :x: Rule naming :x:

Some rules IDs were changed to gain a consitent naming format, please [refer to rules](whispers/rules).


### :x: Output file format :x:
In version 1 the output file was written in YAML with awkward indexing, which made results unusable.

In version 2 the same JSON output as `stdout` is written to the output file, making it easier to parse.


### :x: Log file :x:
In version 1, `whispers.log` is always created in the same directory from which Whispers was executed. The log file remains after execution.

In version 2, the log file will not be created by default, unless explicitly enabled with an argument: `whispers --log src`. The log is only useful for reviewing exceptions and bugs, not for common usage. In addition, the log will now be written to `/tmp/whispers.log` (Posix) or `%TEMP%\whispers.log` (Windows) so that it does not interfere with analysis or permissions.

Together, `--log` and `--debug` can be used to investigate exceptions and bugs. Please [submit a bug report](issues/new) if you find something unexpected!


### :x: Removed support for dynamic languages :x:
In version 1 the following language files were parsed as text and checked for common variable declaration and assignment patterns:
* JavaScript
* Java
* Go
* PHP

It is not possible to parse these languages as Abstract Syntax Trees (ASTs) in Python. The initial attempt was to detect "low hanging fruit" by parsing the files as text instead. This lead to poor functional coverage, as well as a potentially false sense of security.

In version 2 the support for these dynamic languages is dropped. This allowed bringing unit test coverage up to 100%, and in this way ensuring result reliability and true security coverage. It is recommended to rely on AST-based parsing for dynamic languages for getting reliable results. Check out [Semgrep](https://github.com/returntocorp/semgrep)!

Python3 remains fully supported in Whispers 2.


### :x: Replace Levenshtein with Jaro-Winkler :x:
In version 1, [python-Levenshtein](https://github.com/ztane/python-Levenshtein) was used for key-value similarity comparisons (`similar` config parameter). This library is written in Cython and requires additional dependencies for installing. This made it not easily compatible with Windows systems, because additional Visual Studio dependencies needed to be present before installing Whispers.

In version 2, [Jaro-Winkler](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) algorithm is used for similarity comparisons, using the [jellyfish](https://github.com/jamesturk/jellyfish) library, for improved approximate and phonetic string matching. As an additional effect, this change allows installing Whispers on Windows through `pip` without Visual Studio dependencies.

This change should have no effect and behave in a consistent manner. If you have rules that specifically rely on `similar` for key-value comparisons, these may need to be manually tuned.


## :hammer_and_wrench: Improvements :hammer_and_wrench:

### :hammer_and_wrench: Improved support for Windows and MacOS :hammer_and_wrench:

Whispers now runs on Linux, MacOS, and Windows. Install it from PyPI like so: `pip3 install whispers`.

### :hammer_and_wrench: Secrets detection :hammer_and_wrench:

- Added support for Gradle and Maven credentials
- Improved private key detection
- Added known API key formats ([GitGuardian](https://docs.gitguardian.com/secrets-detection/detectors/))
- Added knwon file extensions ([tell_me_your_secrets](https://github.com/valayDave/tell-me-your-secrets/blob/master/tell_me_your_secrets/config.yml))


### :hammer_and_wrench: Include and Exclude by Rule and Severity :hammer_and_wrench:
Individual and grouped rules and severity levels to be included or excluded can now be directly specified with CLI args:

Exclude known files from results: `whispers -R known-file`
Exclude miscellaneous results: `whispers -G misc`
Exclude MAJOR and MINOR severity level results: `whispers -S MAJOR,MINOR`

It is also possible to specify included and excluded rules and severity levels via config.yml. Custom rules can be added directly to the list using the following format:
```yaml
exclude:
  files:
    - \.npmrc
    - .*coded.*
    - \.git/.*
  keys:
    - SECRET_VALUE_KEY
  values:
    - SECRET_VALUE_PLACEHOLDER
  rules:
    - password
    - uri
    - id: starks
      message: Whispers from the North
      severity: CRITICAL
      value:
        regex: (Aria|Ned) Stark
        ignorecase: True
  groups:
    - misc

exclude:
  severity:
    - MINOR

```

If you don't specify any rules, all built-in rules will be used be default. If you do, only those that you specify will be applicable. For a full list of available rules check `whispers --info`.

If you don't specify any severity, all built-in severity levels will be used be default - BLOCKER, CRITICAL, MAJOR, MINOR, INFO. 
If you do, only those that you specify will be applicable.


## :white_check_mark: New features :white_check_mark:

**No new features** were introduced in this release. Whispers 2 still does the same thing as 1, only better and faster. 

The primary objective of the present release was to optimize version 1 logic in order to make it easier to read, understand, and work with in general. This refactoring, along with the aforementioned breaking changes, have shown to increase scanning speed up to 7-10 times (depending on conditions). In addition, it allowed achieving 100% unit test coverage. 

Other focus areas of version 2 were improving usability, like being able to easily filter results in and out from CLI; not writing a log file by default; dropping support for untestable dynamic code scanning; and making code more Pythonic by using built-in features and dataclass models.

Complete list of arguments, rules, and severity levels can be found in `whispers --info`, along with documentation in [README.md](https://github.com/adeptex/whispers/blob/master/README.md).
