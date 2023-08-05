# SDC Global Helpers
![Test Datalake Event Ingester](https://github.com/RingierIMU/sdc-global-all-helpers/workflows/Test%20Datalake%20Event%20Ingester/badge.svg)
![Test Datalake Logs Propagator](https://github.com/RingierIMU/sdc-global-all-helpers/workflows/Test%20Datalake%20Logs%20Propagator/badge.svg)
![Test Recommend Engine Helpers](https://github.com/RingierIMU/sdc-global-all-helpers/workflows/Test%20Recommend%20Engine%20Helpers/badge.svg)
![Tests](https://github.com/RingierIMU/sdc-global-all-helpers/workflows/Tests/badge.svg)

A package of helpers and utilities for sdc repos. Mainly consisting of :
1. `QueryHelper` helpers for mysql db querys using sqlalcamy as the ORM.
2. `RedisHelper` re-usable redis methods. 
3. `SlackHelper` for loggin errors to slack.

## Getting Started
### Installation
To use the package, add the following to your `requirements.txt`. Note: use the latest version here
```
sdc_helpers==1.2.0
```

Then run `make install-requirements` and the version of `sdc helpers` will be included in your project and bob is your father's brother.

## Testing
This repo has a minimum og 90% test coverage and tests are run on all PRs to master.
To run tests just use `make test` which will run all tests and check current coverage.
