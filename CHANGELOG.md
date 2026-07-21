# Changelog

All notable changes to this project will be documented in this file.


## [0.0.3] - 2026-07-21

### Added
- Added a library of built-in generic entities that are loaded automatically by `DSLTranslator`.
- Added support for using built-in entities without explicitly registering them.
- Added `builtin_entities()` helper to inspect the built-in entity library.

### Changed
- `DSLTranslator` now accepts optional custom entities.
- Improved the Quick Start guide to demonstrate automatic built-in entity support.
- Expanded the documentation with a new **Built-in Entities** section and examples.

### Fixed
- Corrected line numbering in `UndefinedEntity` error reporting.
- Removed unreachable code from `DSLSyntaxError`.


## [0.0.2] - 2026-07-20

### Changed

- Improved the README with a complete Quick Start example.
- Expanded and refined the project documentation.
- Updated package metadata and project links.

---

## [0.0.1] - Initial Release - 2026-07-19

### Added

- Initial release of DocDSL.
- Declarative DSL for describing text extraction rules.
- Parser implemented using textX.
- DSL translator for generating regular expressions.
- Reusable `Entity` definitions.
- Support for `FIND`, `SKIP`, `CAPTURE`, and `IF` commands.
- Support for multi-line and bounded capture operations.
- Built-in helper tokens.
- Friendly syntax and semantic error reporting.
- README and language reference documentation.
- Published package on PyPI.

### Notes

- Initial public release.
- APIs and DSL syntax may evolve in future releases.
