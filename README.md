# Bitrise Reports

[![Flake8](https://img.shields.io/badge/codestyle-flake8-yellow)](https://flake8.pycqa.org/en/latest/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Quality](https://api.codeclimate.com/v1/badges/a9fe25bd995710be45d2/maintainability)](https://codeclimate.com/github/dotanuki-labs/bitrise-reports/maintainability)
[![Coverage](https://codecov.io/gh/dotanuki-labs/bitrise-reports/branch/main/graph/badge.svg)](https://codecov.io/gh/dotanuki-labs/bitrise-reports)
[![PyPI](https://img.shields.io/pypi/v/bitrise-reports)](https://pypi.org/project/bitrise-reports/)
[![Main](https://github.com/dotanuki-labs/bitrise-reports/workflows/Main/badge.svg)](https://github.com/dotanuki-labs/bitrise-reports/actions?query=workflow%3AMain)
[![License](https://img.shields.io/github/license/dotanuki-labs/bitrise-reports)](https://choosealicense.com/licenses/mit)

## What

A simple cruncher for numbers derived from builds you run on [Bitrise CI](https://www.bitrise.io/).

Main features:

- Backed by [Bitrise REST API](https://api-docs.bitrise.io/) under the hood
- Can compute timing (queued, running and total execution time) for all builds in the given time window
- Can compute build statuses (success, failure or aborted) for all builds in the given time window
- Result are detailed per machine type and also per Workflow
- Report types : CLI (stdout), JSON and Excel spreadsheet

Please check out [documentation](https://dotanuki-labs.github.io/bitrise-reports) to learn more about 🔥

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
