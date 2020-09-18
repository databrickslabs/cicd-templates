# {{cookiecutter.project_name}}

This is a sample project for Databricks, generated via cookiecutter.

While using this project, you need Python 3.X and `pip` or `conda` for package management.

## Installing dbx

```bash
pip install tools/dbx.whl
```

`dbx` is developed on MacOS and tested on Linux with Python 3.+. If you run into a problem running `dbx` on Windows, please raise an issue on GitHub.

## Configuring environments

1. `dbx` heavily relies on [databricks-cli](https://docs.databricks.com/dev-tools/cli/index.html) and uses the same set of profiles.
Please configure your profiles in advance using `databricks configure` command as described [here](https://docs.databricks.com/dev-tools/cli/index.html#set-up-authentication).

2. Create a new environment via given command:
```bash
dbx configure \
    --environment="test" \
    --profile="<profile-name>" \
    --workspace-dir="/dbx/projects/sample"
```

This command will configure environment by given profile and store project in a given `workspace-dir` as an MLflow experiment.

## Interactive execution

1. `dbx` expects that cluster for interactive execution supports `%pip` and `%conda` magic [commands](https://docs.databricks.com/libraries/notebooks-python-libraries.html) in case if you use additional options (requirements, package or conda-environment).

2. To execute the code in an interactive fashion, provide either `--cluster-id` or `--cluster-name`, and a `--source-file` parameter.
```bash
dbx execute \
    --cluster-id="<some-cluster-id>" \
    --source-file="some/entrypoint.py"
```

You can also provide parameters to install .whl packages before launching code from the source file, as well as installing dependencies from pip-formatted requirements file or conda environment yml config.
Please check `dbx execute -h` for a list of available options.

## Preparing deployment file

Next step would be to configure your deployment objects. To make this process easy and flexible, we're using JSON for configuration.

By default, deployment configuration is stored in `.dbx/deployment.json`.
The main idea of is to provide a flexible way to configure job with it's dependencies.

## Deployment

To start new deployment, launch the following command:  

```bash
dbx deploy --environment=test
```

You can optionally provide requirements.txt via `--requirements` option, all requirements will be automatically added to the job definition.

## Launch

Finally, after deploying all your job-related files, you launch the job via the following command:

```
dbx launch --environment=test --job=sample
```

## CICD pipeline settings

Please set the following secrets or environment variables:
- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`

Also, please set the environment variable `PROFILE_NAME` to a proper name (same as local one). 
