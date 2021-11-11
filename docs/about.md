---
layout: default
title: About
nav_order: 1
---

# What

A simple cruncher for numbers derived from builds you run on [Bitrise CI](https://www.bitrise.io/). Useful if you are in charge of managing infrastructure capacity related to Bitrise, like detecting/reporting anomalies, evaluating queues impact and so on.

Main features:

- Backed by [Bitrise REST API](https://api-docs.bitrise.io/) under the hood
- Can compute timing (queued, running and total execution time) for all builds in the given time window
- Can compute build statuses (success, failure or aborted) for all builds in the given time window
- Results can be filtered by Git branch (eg **master** or **main**)
- Result are detailed per machine type and also per Workflow
- Supports emulation of consumed [Bitrise Velocity credits](https://www.bitrise.io/velocity-plan) (for Velocity customers)
- Report types : CLI (stdout), JSON and Excel spreadsheet

This tool is implemented with Python, being tested with versions `3.8.x`, `3.9.x` and `3.10.x`. It is distributed under [the MIT License](https://choosealicense.com/licenses/mit)
