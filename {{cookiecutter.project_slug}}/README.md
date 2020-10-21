# {{cookiecutter.project_name}}

This is a sample project for Databricks, generated via cookiecutter.

While using this project, you need Python 3.X and `pip` or `conda` for package management.

## Installing project requirements

```bash
pip install -r unit-requirements.txt
```

## Install project package in a developer mode

```bash
pip install -e .
```

## Interactive execution

1. `dbx` expects that cluster for interactive execution supports `%pip` and `%conda` magic [commands](https://docs.databricks.com/libraries/notebooks-python-libraries.html).
2. Please configure your job in `conf/deployment.json` file. 
2. To execute the code interactively, provide either `--cluster-id` or `--cluster-name`.
```bash
dbx execute \
    --cluster-name="<some-cluster-name>" \
    --job=job-name
```

## Preparing deployment file

Next step would be to configure your deployment objects. To make this process easy and flexible, we're using JSON for configuration.

By default, deployment configuration is stored in `conf/deployment.json`.

## Deployment

To start new deployment, launch the following command:  

```bash
dbx deploy --environment={{cookiecutter.environment}}
```

You can optionally provide requirements.txt via `--requirements` option, all requirements will be automatically added to the job definition.

## Launch

Finally, after deploying all your job-related files, you launch the job via the following command:

```
dbx launch --environment={{cookiecutter.environment}} --job=sample
```

## CICD pipeline settings

Please set the following secrets or environment variables. 
Follow the documentation for [GitHub Actions](https://docs.github.com/en/actions/reference) or for [Azure DevOps Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch):
- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`