# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [v0.1.4] - 2019-09-09
### Fixed
- having graph properties with numpy types raised an error when dumping to JSON,
  so these types are now converted to Python types prior to dumping

### Changed
- nodes with strength 0 are now rescaled to strength 1 if node size is scaled by strength
- when changing node and link properties in a frozen simulation, the simulation is not restarted anymore
- The server is stopped as soon as the Browser window is closed

## [v0.1.3] - 2019-06-18
### Added
- module `netwulf.io`, which contains functions to save and load stylized networks
- appropriate tests for this module's functionality
- sections in the docs
- a label and link drawing cookbook example

### Changed
- `zorder`-behavior in matplotlib drawing (`netwulf.draw_netwulf`)

## [v0.1.2] - 2019-06-17
### Added
- function `netwulf.tools.node_pos` to get a node's position on the matplotlib axis
- function `netwulf.tools.add_node_label` to add a node label to the matplotlib axis
- function `netwulf.tools.add_edge_label` to add an edge label to the matplotlib axis

### Changed
- The corresponding docs for node labels was changed to use the new functions.
- The matplotlib test now contains additional tests for the edge label and node label positioning

## [v0.1.1] - 2019-05-24
### Changed
- some default settings
- set constant `dpi = 72` for unit conversions in matplotlib redrawing because apparently matplotlib only uses this value for conversions, see https://stackoverflow.com/a/35501485/4177832.

## [v0.1.0] - 2019-05-23
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

[Unreleased]: https://github.com/benmaier/netwulf/compare/v0.1.4...HEAD
[v0.1.4]: https://github.com/benmaier/netwulf/compare/v0.1.3...v0.1.4
[v0.1.3]: https://github.com/benmaier/netwulf/compare/v0.1.2...v0.1.3
[v0.1.2]: https://github.com/benmaier/netwulf/compare/v0.1.1...v0.1.2
[v0.1.1]: https://github.com/benmaier/netwulf/compare/v0.1.0...v0.1.1
[v0.1.0]: https://github.com/benmaier/netwulf/compare/v0.0.18...v0.1.0
[v0.0.18]: https://github.com/benmaier/netwulf/compare/v0.0.17...v0.0.18
[v0.0.17]: https://github.com/benmaier/netwulf/releases/tag/v0.0.17
