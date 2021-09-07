# Changelog

## Release 1.0.1

This release provides `init_adapter` method to make `dbx execute` method more user-friendly.

## Release 1.0.2

This release provides hotfix for incorrect reference of `init_conf` and adds proper testing checks for github workflows.

## Release 1.0.3

This release adds more compatibility with win-based development environments, as well as extensive tests for win-based launches.

## Release 1.0.4

Added support for picking configuration properties from environment variable. 
Fixed issue with non-existent lockfile. 

## Release 1.0.5

Minor fixes in the dbx behaviour.

## Release 1.0.6

Fixed multiple issues with run status checks:
- status check code is now unified int one method
- `--existing-runs=cancel` instabilities fixed
- `--trace` stucks in case of skipped status fixed
- proper exit code for failed integration tests

## Release 1.0.7

- Since dbx is moved to public, no more whl file is needed. whl file is deleted from the repository, as well as all references to it.

## Release 1.0.8

- Introduced support for Google Cloud
- project template code is formatted with black for better readability

## Release 1.0.9

- Add installation of `dbx` to the `unit-requirements.txt` file
- Switch generated top-level folder name to project_name variable, not project_slug.
- Add `.coveragerc` to the generated project
- Explicitly include support for `dbutils` in the `common.py` file

## Release 1.0.10

- Remove `init_adapter` logic, now all parameters are directly passed from the `deployment.json` file.

## Release 1.0.11

- Fixed issue with project name in Gitlab CI.