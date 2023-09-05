# Whispers 2.2.0 release notes

* License change
* Compatibility improvements
    * Standardize severity levels
    * Minor code refactor
* Detection improvements
    * Add XML cases
    * Add `apikey-maybe` rule



## 💫 Licensing changes (again) 💫

Version 2.1 was released under [GNU General Public License v3.0](https://github.com/adeptex/whispers/blob/3f5282ea3855d658ea37ec96dfc693598c16d7a7/LICENSE), which is `intended to guarantee your freedom to share and change all versions of a program--to make sure it remains free software for all its users.` 

Version 2.2 is released under [BSD 3-Clause License](https://github.com/adeptex/whispers/blob/master/LICENSE), which is a permissive license that `prohibits others from using the name of the copyright holder or its contributors to promote derived products without written consent.` 

This change removes source code disclosure requirement 🕵️


## ❌ Breaking changes ❌

### ❌ Severity levels ❌

Severity level names have been adapted to a more common format:

| Version 2.1 (before) | Version 2.2 (now) |
|---|---|
| BLOCKER | Critical |
| CRITICAL | High |
| MAJOR | Medium |
| MINOR | Low |
| INFO | Info |

Please update your custom rules and CLI args to reflect these changes.

See [README](https://github.com/adeptex/whispers#readme) for details.


# Changelog

|Version|Release notes|
|---|---|
|2.0.0|https://github.com/adeptex/whispers/releases/tag/2.0.0|
|2.1.0|https://github.com/adeptex/whispers/releases/tag/2.1.0|
|2.2.0|https://github.com/adeptex/whispers/releases/tag/2.2.0|
