# Whispers 2.1.0 release notes

## :x: Breaking changes :x:

### :x: Arguments :x:

| 2.0 | 2.1 |
|-----|-----|
| `--print_config` | `--init` |
| `--log` | `--log log.txt` |


### :x: Logging :x:

**Version 2.0:** Opt-in logging for tracing execution flow, useful only for debugging. Results printed to `stdout` using `print()` as a JSON dict, one result per line. Enabling logging required adding the `--log` argument.

**Version 2.1:** Logging is used to alert identified secrets during execution with `WARNING` level. Results are written to `stdout` as a JSON list at the end. This improves results parseability as a JSON list, while maintaining live results display that was previously achieved by JSON dicts per line.


## :white_check_mark: New features :white_check_mark:

### :white_check_mark: JSON results :white_check_mark:

Final results are now presented as a JSON list all together, instead of one JSON dictionary per line.

### :white_check_mark: Docker image :white_check_mark:

Whispers now publishes a Docker image: `ghcr.io/adeptex/whispers:latest`
