# Bitrise Reports

[![Flake8](https://img.shields.io/badge/codestyle-flake8-yellow)](https://flake8.pycqa.org/en/latest/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Quality](https://api.codeclimate.com/v1/badges/a9fe25bd995710be45d2/maintainability)](https://codeclimate.com/github/dotanuki-labs/bitrise-reports/maintainability)
[![Coverage](https://codecov.io/gh/dotanuki-labs/bitrise-reports/branch/main/graph/badge.svg)](https://codecov.io/gh/dotanuki-labs/bitrise-reports)
[![PyPI](https://img.shields.io/pypi/v/bitrise-reports)](https://pypi.org/project/bitrise-reports/)
[![Main](https://github.com/dotanuki-labs/bitrise-reports/workflows/Main/badge.svg)](https://github.com/dotanuki-labs/bitrise-reports/actions?query=workflow%3AMain)
[![License](https://img.shields.io/github/license/dotanuki-labs/bitrise-reports)](https://choosealicense.com/licenses/mit)

## What

A simple cruncher for numbers derived from builds you run on [Bitrise CI](https://www.bitrise.io/). Useful if you are in charge of managing infrastructure capacity related to Bitrise, like detecting/reporting anomalies, evaluating queues impact and so on.

Main features:

- Backed by [Bitrise REST API](https://api-docs.bitrise.io/) under the hood
- Can compute timing (queued, running and total execution time) for all builds in the given time window
- Can compute build statuses (success, failure or aborted) for all builds in the given time window
- Results can be filtered by Git branch (eg **master** or **main**)
- Result are detailed per machine type and also per Workflow
- Supports emulation of consumed [Bitrise Velocity credits](https://www.bitrise.io/velocity-plan) (for Enterprise customers)
- Report types : CLI (stdout), JSON and Excel spreadsheet

This tool is implemented with Python, being tested with versions `3.8.x`, `3.9.x` and `3.10.x`

## Installing


### With pip

Install `bitrise-reports` with [pip](https://pypi.org/project/pip/)

```bash
$> pip install bitrise-reports
```


### With Docker

```bash
$> docker pull ghcr.io/dotanuki-labs/bitrise-reports
```

## Using

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

## Contributing

If you want to contribute with this project

- Check the [contribution guidelines](https://github.com/dotanuki-labs/.github/blob/main/CONTRIBUTING.md)
- Ensure you have Python 3.8.+ installed. I recommend [Pyenv](https://github.com/pyenv/pyenv) for that.
- Ensure you have [Poetry](https://python-poetry.org/) installed
- Prepare your environment

```bash
$> make setup
```

- Code you changes
- Make sure you have a green build

```bash
$>  make inspect test
```

- Submit your PR 🔥

## Author

- Coded by Ubiratan Soares (follow me on [Twitter](https://twitter.com/ubiratanfsoares))

## License

```
The MIT License (MIT)

Copyright (c) 2021 Dotanuki Labs

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
