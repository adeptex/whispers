# Whispers 2.1.0 release notes

## :x: Breaking changes :x:

### :x: Arguments :x:

Several arguments have been modified and/or adapted to improve usability.

- Human readable output is shown in logs (2.1), `-H` and `--human` (2.0) are removed.

- Version can be shown with `--version` (2.1), `-v` (2.0) is removed.

- Extended help can be shown with `--info` (2.1), `-i` (2.0) is removed.

- Debug mode can be enabled with `--debug` (2.1), `-d` (2.0) is removed.

- Logs can be redirected to a file with `--log log.txt` (2.1), constant `/tmp/whispers.log` (2.0) is removed.

- Configuration template can be created with `--init` (2.1), `--print_config` (2.0) is removed.


### :x: Logging :x:

**Version 2.0:** Opt-in logging for tracing execution flow, useful only for debugging. Results printed to `stdout` using `print()` as a JSON dict, one result per line. Enabling logging required adding the `--log` argument.

**Version 2.1:** Logging is used to alert identified secrets during execution with `WARNING` level. Results are written to `stdout` as a JSON list at the end. This improves results parseability as a JSON list, while maintaining live results display that was previously achieved by printing secrets as JSON one per line.


## :white_check_mark: New features :white_check_mark:

### :white_check_mark: Results as JSON list :white_check_mark:

To improve integration and downstream processing, Whispers now outputs results as a JSON list of dictionaries with all detected secrets together (2.1), instead of one JSON dictionary per line (2.0). This list is directly loadable and parsable as JSON.


# Changelog

|Version|Release notes|
|---|---|
|2.0.0|https://github.com/adeptex/whispers/releases/tag/2.0.0|
|2.1.0|https://github.com/adeptex/whispers/releases/tag/2.1.0|
