# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- some default settings

## [v0.1.0] -2019-05-23
### Changed
- `netwulf.tools.bind_positions_to_network` is now called `netwulf.bind_properties_to_network` and it now does exactly that -- write properties instead of just positions
- several visualization config options were renamed
- `netwulf.tools.draw_netwulf` now draws the canvas positions instead of the actual node positions (differences arise by zooming).

## [v0.0.18] - 2019-05-15
### Added
- added automated test functionality in ``/tests/`` and ``Makefile``

### Changed
- catch Python 3.5 error for emulated ``mkdir -p`` functionality

## [v0.0.17] - 2019-05-15
### Changed
- switched from usage of `os.path` to `pathlib` at the appropriate places

[Unreleased]: https://github.com/benmaier/netwulf/compare/v0.1.0...HEAD
[v0.0.18]: https://github.com/benmaier/netwulf/compare/v0.0.18...v0.1.0
[v0.0.18]: https://github.com/benmaier/netwulf/compare/v0.0.17...v0.0.18
[v0.0.17]: https://github.com/benmaier/netwulf/releases/tag/v0.0.17
