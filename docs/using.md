---
layout: default
title: Using
nav_order: 3
---

# Using Bitrise Reports

## Getting started

Let's say you want analyse numbers for the project `android-flagship`, learning from
builds that ran during April of 2021. You'll firstly need a
[Bitrise Personal Access Token](https://devcenter.bitrise.io/api/authentication/) for
that. Note you must be a member in the project you want to analyse.

By running

```bash
$> bitrise-reports \
    --token=$BITRISE_PAT_TOKEN \
    --app=android-flagship \
    --starting=2021-04-01 \
    --ending=2021-04-30
```

you should get something like that on your CLI

![](https://raw.githubusercontent.com/dotanuki-labs/bitrise-reports/main/.github/assets/showcase-cli-simple.png)

which is a simple overview of what happened.

Let's say now that you want to learn about how much time you are spending with queued builds.

You can run then

```bash
$> bitrise-reports \
    --token=$BITRISE_PAT_TOKEN \
    --app=android-flagship \
    --starting=2021-04-01 \
    --ending=2021-04-30 \
    --detailed-timing
```

and get a report like this one

![](https://raw.githubusercontent.com/dotanuki-labs/bitrise-reports/main/.github/assets/showcase-cli-timing.png)

Last but not least, suppose you want to learn about execution status for all your Workflows that you run for events in your `master` branch (eg, push or a scheduled build).

You can run

```bash
$> bitrise-reports \
    --token=$BITRISE_PAT_TOKEN \
    --app=android-flagship \
    --starting=2021-04-01 \
    --ending=2021-04-30 \
    --target-branch=master \
    --detailed-builds
```

and get a report like about that too

![](https://raw.githubusercontent.com/dotanuki-labs/bitrise-reports/main/.github/assets/showcase-cli-statuses.png)

## Command line interface

The complete list of CLI options:

| Option           | Details                                                         | Required  |
|------------------|-----------------------------------------------------------------|-----------|
| token            | Personal access token for Bitrise API                           | Yes       |
| app              | The title of your app in Bitrise                                | Yes       |
| starting         | Starting date in the target time frame                          | Yes       |
| ending           | Ending date in the target time frame                            | Yes       |
| detailed-builds  | Details all statuses (success, failure and abortion) for builds | No        |
| detailed-timing  | Details timing (queued, running, total execution) for builds    | No        |
| emulate-velocity | Estimate Bitrise Velocity credits consumed                      | No        |
| target-branch    | Filters build by Git branch                                     | No        |
| report-style     | The style of report you want                                    | No        |

where

- `starting` and `ending` follow **YYYY-MM-DD** convention
- `report-style` accepts **stdout** (default), **json** or **excel**
- `detailed-timing` is a CLI flag
- `detailed-builds` is a CLI flag
- `emulate-velocity` is a CLI flag

If you opt-in for a specific report style, the corresponding file - **bitrise-metrics.json** or **bitrise-metrics.xlsx** - will be written in the same folder you are runnint `bitrise-reports`.

## Running with Docker

Given the current definition for the Container Image, all the previous examples are straitghtforward to run on top of Docker:


```bash
$> docker run --rm ghcr.io/dotanuki-labs/bitrise-reports \
    --token=$BITRISE_PAT_TOKEN \
    --app=android-flagship \
    --starting=2021-04-01 \
    --ending=2021-04-30 \
    --detailed-builds
```

When exporting reports (JSON or Excel) you should mount your current path upon Container's `workdir`

```bash
$> docker run --rm -v "${PWD}:/reports" ghcr.io/dotanuki-labs/bitrise-reports \
    --token=$BITRISE_PAT_TOKEN \
    --app=android-flagship \
    --starting=2021-04-01 \
    --ending=2021-04-30 \
    --report-style=excel
```
