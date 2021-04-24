# CHANGELOG
> https://keepachangelog.com

All notable changes to this project will be documented in this file.

## Version 0.0.2
**2021-04-24**

- Supporting machine types running over gen2 infrastructure
- Fixing a bug when calculating queued times
- Improves packaging

## Version 0.0.1
**2021-03-25**

### First release

- Backed by Bitrise REST API under the hood
- Validates if provided Bitrise PAT has access to the target app
- Handles automatically pagination over results
- Computes minutes for queued, building and total execution, for all builds in given a time frame
- Breakdown numbers per build machine type and also per Workflow
- Supports emulation of consumed Bitrise Velocity credits
- Report results as CLI (stdout), JSON or Excel spreadsheet
