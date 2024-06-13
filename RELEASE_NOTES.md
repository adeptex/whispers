# Whispers 2.3.0 release notes

* 💫 <u>**New Feature: Static Code Analysis**</u> is now supported!
    * Complements classic Whispers' structured text analysis with [Semgrep](https://semgrep.dev)'s AST generator for [common programming languages](https://semgrep.dev/docs/supported-languages) like Python, PHP, Java/Scala/Kotlin, JavaScript/TypeScript, Go, etc etc.
    * New argument `--ast` for enabling this feature via the CLI (it is disabled by default)
    * New setting `ast: true` for enabling this feature via a custom config file (set to `ast: false` by default)
    * Replaced [`astroid`](https://github.com/adeptex/whispers/blob/8f17f77e2199c55458ff125e3fb477a2a9349593/whispers/plugins/python.py) Python AST generator with [`semgrep`](https://github.com/adeptex/whispers/blob/master/whispers/plugins/semgrep.py)

* [Detection rule](https://github.com/adeptex/whispers/blob/master/whispers/rules) improvements
    * Known API keys
    * AWS account ID
    * Passwords
    * Creditcards

* Dependency tracking improvements
    * New [`requirements-dev.txt`](https://github.com/adeptex/whispers/blob/master/requirements-dev.txt) file allows Dependabot updates for dev dependencies
    * Modified [`setup.py`](https://github.com/adeptex/whispers/blob/master/setup.py) to read from `requirements.txt` and `requirements-dev.txt`
    * Updated build CI to use Python 3.12.3

* Debugging and troubleshooting
    * Modified [`config.yml`](https://github.com/adeptex/whispers/blob/master/whispers/config.yml) to exclude known false positives
    * Fixed [`Dockerfile`](https://github.com/adeptex/whispers/blob/master/Dockerfile) to work with `docker build -t whispers .` or the same `make image`
    * New arg `--dump` for generating an AST of a file: `whispers --dump src/example.ts`


## 💫 New Feature: Static Code Analysis 💫

With the release of Whispers 2.3, it is now possible to accurately apply Whispers' secret detection techniques for structured text to static code. Before this release, Whispers only supported structured text formats, such as JSON or XML. [Semgrep](https://semgrep.dev) is an open source SAST tool, which has a built-in feature for generating Abstract Structure Trees (ASTs) for [many common programming languages](https://semgrep.dev/docs/supported-languages). Generating an AST for static code yields an accurate structured text representation, which can be checked for secrets with Whispers' rules and plugins. As such, generating ASTs requires an additional "format conversion" step, which naturally affects runtime speed. When AST is enabled it will take longer to scan the same scope if any source code files are present. The increased amount of runtime time would be however long it takes to run the following command on all static code files in scope:

```sh
semgrep scan --metrics=off --quiet --dump-ast --json --lang $LANG $SRCFILE
```

Consider the following benchmarks:

```sh
time whispers -F " " tests/fixtures
# 313 detected secrets
# 0,51s user 0,03s system 99% cpu 0,540 total
# 0,60s user 0,04s system 99% cpu 0,642 total

time whispers -a -F " " tests/fixtures
# 421 detected secrets
# 2,20s user 0,40s system 100% cpu 2,589 total
# 2,32s user 0,46s system 100% cpu 2,772 total
```

AST conversion is **disabled by default** - `semgrep` will **not** execute at all unless explicitly enabled. Custom config files that are missing `ast: false` or `ast: true` will default to `false`.

```yaml
ast: true  # enable AST in config.yml
```

```sh
whispers --ast target/dir/or/file  # enable AST in CLI
```


## ❌ Breaking changes ❌

### ❌ Replaced `astroid` with `semgrep` ❌

Before Whispers 2.3, only Python AST scanning was natively supported by `astroid`, and integrated via [`plugins/python.py`](https://github.com/adeptex/whispers/blob/8f17f77e2199c55458ff125e3fb477a2a9349593/whispers/plugins/python.py). With the release of Whispers 2.3, this functionality is superseded by `semgrep`, and integrated via [`plugins/semgrep.py`](https://github.com/adeptex/whispers/blob/master/whispers/plugins/semgrep.py). As a base line, the new `semgrep` plugin detects the same findings as the `astroid` plugin, but supports more programming languages.

Unfortunately `semgrep` has telemetry enabled by default, but can be turned off via [`--metrics=off`](https://github.com/adeptex/whispers/blob/master/whispers/plugins/semgrep.py#L57). In any case, `semgrep` will not execute unless explicitly enabled via args or config.


# Changelog

|Date|Version|Release notes|
|---|---|---|
|2021-12-07|2.0.0|https://github.com/adeptex/whispers/releases/tag/2.0.0|
|2022-07-29|2.1.0|https://github.com/adeptex/whispers/releases/tag/2.1.0|
|2023-10-23|2.2.0|https://github.com/adeptex/whispers/releases/tag/2.2.0|
|2024-06-13|2.3.0|https://github.com/adeptex/whispers/releases/tag/2.3.0|
