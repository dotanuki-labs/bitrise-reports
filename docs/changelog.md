---
layout: default
title: Changelog
nav_order: 5
---

# Changelog

This project follows the [Keep a Changelog](https://keepachangelog.com) convention. All notable changes will be documented here.

## Version 0.2.0
**2021-10-08**

### Added
- Official support to Python 3.10.x

### Fixed
- Docker image now packages with the snapshot built from the release tag

## Version 0.1.2
**2021-06-15**

### Fixed
- Deploys on ghcr.io only after deployed on Pypi

## Version 0.1.1
**2021-06-15**

### Added
- Docker support

## Version 0.1.0
**2021-05-28**

### Added
- Support to filter results by target branch
- Better output when application crashes on execution

### Changed
- CLI interface is now different and mostly incompatible with previous versions
- Default report now outputs only total number of builds and total execution time
- Reports can be enhanced at will accordingly provided CLI flags

### Fixed
- Fixed a bug when calculating total build times

## Version 0.0.3
**2021-05-04**

### Added
- Supporting build results (success and failures) for all analysed builds

## Version 0.0.2
**2021-04-24**

### Added
- Supporting machine types running over gen2 infrastructure
- Improves packaging

### Fixed
- Fixing a bug when calculating queued times

## Version 0.0.1
**2021-03-25**

### First release

- Backed by Bitrise REST API under the hood
- Validates if provided Bitrise PAT has access to the target app
- Handles automatically pagination over results
- Compute minutes for queued, building and total execution, for all builds in given a time frame
- Breakdown numbers per build machine type and also per Workflow
- Supports emulation of consumed Bitrise Velocity credits
- Report results as CLI (stdout), JSON or Excel spreadsheet
