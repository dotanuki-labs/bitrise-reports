# Bitrise Reports

[![Flake8](https://img.shields.io/badge/codestyle-flake8-yellow)](https://flake8.pycqa.org/en/latest/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Quality](https://api.codeclimate.com/v1/badges/a9fe25bd995710be45d2/maintainability)](https://codeclimate.com/github/dotanuki-labs/bitrise-reports/maintainability)
[![Coverage](https://codecov.io/gh/dotanuki-labs/bitrise-reports/branch/main/graph/badge.svg)](https://codecov.io/gh/dotanuki-labs/bitrise-reports)
[![PyPI](https://img.shields.io/pypi/v/bitrise-reports)](https://pypi.org/project/bitrise-reports/)
[![Main](https://github.com/dotanuki-labs/bitrise-reports/workflows/Main/badge.svg)](https://github.com/dotanuki-labs/bitrise-reports/actions?query=workflow%3AMain)
[![License](https://img.shields.io/github/license/dotanuki-labs/bitrise-reports)](https://choosealicense.com/licenses/mit)

## What

> _Complete blog post to come. Stay tuned!_

A simple cruncher for numbers derived from builds you run on [Bitrise CI](https://www.bitrise.io/). Useful if you are in charge of managing infrastructure capacity related to Bitrise, detecting/reporting anomalies, evaluating queues impact and so on.

Main features:

- Backed by [Bitrise REST API](https://api-docs.bitrise.io/) under the hood
- Computes time for queued, running and total execution, for all builds found in a given a time frame
- Breakdown numbers per machine type and also per Workflow
- Supports emulation of consumed [Bitrise Velocity credits](https://www.bitrise.io/velocity-plan) (for Enterprise customers)
- Report types : CLI (stdout), JSON and Excel spreadsheet

## Installing

This tool requires Python, supporting versions 3.8.x and 3.9.x.

Install `bitrise-reports` with [pip](https://pypi.org/project/pip/)

```bash
→ pip install bitrise-reports
```

## Using

Let's say you want analyse numbers for the project `my-app`, learning from
builds that ran during February of 2021. You'll firstly need a
[Bitrise Personal Access Token](https://devcenter.bitrise.io/api/authentication/) for
that. Note you must be a member in the project you want to analyse.

By running

```bash
→ bitrise-reports \
    --token=$BITRISE_PAT_TOKEN \
    --app=my-app \
    --starting=2021-02-01 \
    --ending=2021-02-28
```
you should get something like that on your CLI

![](.github/assets/showcase-cli.png)

The complete list CLI options:

| Option   | Details                                    | Required  |
|----------|--------------------------------------------|-----------|
| token    | Personal access token for Bitrise API      | Yes       |
| app      | The title of your app in Bitrise           | Yes       |
| starting | Starting date in the target time frame     | Yes       |
| ending   | Ending date in the target time frame       | Yes       |
| report   | The style of report you want               | No        |
| velocity | Estimate Bitrise Velocity credits consumed | No        |

where

- `starting` and `ending` follows **YYYY-MM-DD** convention
- `report` accepts **stdout** (default), **json** and **excel**
- `velocity` is a CLI flag

For instance, if you want an Excel spreadsheet instead of the fancy CLI UI from the previous example
while also estimating Velocity usage for the builds, you can run

```bash
→ bitrise-reports \
    --token=$BITRISE_PAT_TOKEN \
    --app=my-app \
    --starting=2021-02-01 \
    --ending=2021-02-28 \
    --report=excel \
    --velocity
```

and the output file `bitrise-metrics.xlsx` will be available in the same folder.

![](.github/assets/showcase-excel.png)

## Contributing

If you want to contribute with this project

- Check the [contribution guidelines](https://github.com/dotanuki-labs/.github/blob/main/CONTRIBUTING.md)
- Ensure you have Python 3.8.+ installed. I recommend [Pyenv](https://github.com/pyenv/pyenv) for that.
- Ensure you have [Poetry](https://python-poetry.org/) installed
- Prepare your environment with [Flake8](https://pypi.org/project/flake8/), [Black](https://pypi.org/project/black/) and [Bandit](https://pypi.org/project/bandit/)

```bash
→ make setup
```

- Code you changes
- Make sure you have a green build

```bash
→  make inspect test
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
