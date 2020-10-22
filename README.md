# Databricks Labs CI/CD Templates

This repository provides a template for automated Databricks CI/CD pipeline creation and deployment.

## Table of Contents
* [Databricks Labs CI/CD Templates](#databricks-labs-cicd-templates)
  * [Sample project structure (with GitHub Actions)](#sample-project-structure-with-github-actions)
  * [Sample project structure (with Azure DevOps)](#sample-project-structure-with-azure-devops)
  * [Quickstart](#quickstart)
     * [Local steps](#local-steps)
     * [Setting up CI/CD pipeline on GitHub Actions](#setting-up-cicd-pipeline-on-github-actions)
     * [Setting up CI/CD pipeline on Azure DevOps](#setting-up-cicd-pipeline-on-azure-devops)
  * [Deployment file structure](#deployment-file-structure)
  * [FAQ](#faq)
  * [Legal Information](#legal-information)
  * [Feedback](#feedback)
  * [Contributing](#contributing)
  * [Kudos](#kudos)



## Sample project structure (with GitHub Actions)
```
.
├── .github
│   └── workflows
│       ├── onpush.yml
│       └── onrelease.yml
├── .gitignore
├── README.md
├── conf
│   ├── deployment.json
│   └── test
│       └── sample.json
├── pytest.ini
├── sample_project
│   ├── __init__.py
│   ├── common.py
│   └── jobs
│       ├── __init__.py
│       └── sample
│           ├── __init__.py
│           └── entrypoint.py
├── setup.py
├── tests
│   ├── integration
│   │   └── sample_test.py
│   └── unit
│       └── sample_test.py
├── tools
│   └── dbx-0.7.0-py3-none-any.whl
└── unit-requirements.txt
```

Some explanations regarding structure:
- `.dbx` folder is a auxiliary folder, where metadata about environments and execution context is located.
- `sample_project` - Python package with your code
- `tests` - directory with your package tests
- `conf/deployment.json` - deployment configuration file. Please read the [following section](#deployment-file-structure) for a full reference.
- `.github/workflows/` - workflow definitions for GitHub Actions

## Sample project structure (with Azure DevOps)
```
.
├── .dbx
│   └── project.json
├── .gitignore
├── README.md
├── azure-pipelines.yml
├── conf
│   ├── deployment.json
│   └── test
│       └── sample.json
├── pytest.ini
├── sample_project_azure_dev_ops
│   ├── __init__.py
│   ├── common.py
│   └── jobs
│       ├── __init__.py
│       └── sample
│           ├── __init__.py
│           └── entrypoint.py
├── setup.py
├── tests
│   ├── integration
│   │   └── sample_test.py
│   └── unit
│       └── sample_test.py
├── tools
│   └── dbx-0.7.0-py3-none-any.whl
└── unit-requirements.txt
```

Some explanations regarding structure:
- `.dbx` folder is a auxiliary folder, where metadata about environments and execution context is located.
- `sample_project` - Python package with your code
- `tests` - directory with your package tests
- `conf/deployment.json` - deployment configuration file. Please read the [following section](#deployment-file-structure) for a full reference.
- `azure-pipelines.yml` - Azure DevOps Pipelines workflow definition

## Quickstart

> **_NOTE:_**  
As a prerequisite, you need to install [databricks-cli](https://docs.databricks.com/dev-tools/cli/index.html) with a [configured profile](https://docs.databricks.com/dev-tools/cli/index.html#set-up-authentication).
In this instruction we're based on [Databricks Runtime 7.3 LTS ML](https://docs.databricks.com/release-notes/runtime/7.3ml.html). 
If you don't need to use ML libraries, we still recommend to use ML-based version due to [`%pip` magic support](https://docs.databricks.com/libraries/notebooks-python-libraries.html).

### Local steps
Perform the following actions in your development environment:
- Create new conda environment and activate it:
```bash
conda create -n <your-environment-name> python=3.7.5
conda activate <your-environment-name>
```
- Install cookiecutter and path:
```bash
pip install cookiecutter path
```
- Create new project using cookiecutter template. Please note that the profile should exist in your `~/.databrickscfg`:
```
cookiecutter https://github.com/databrickslabs/cicd-templates
```
- Switch to the project directory and install `dbx`:
```bash
pip install -U tools/dbx-0.7.0-py3-none-any.whl
```
- In the generated directory you'll have a sample job with testing and launch configurations around it.
- Launch and debug your code on an interactive cluster via the following command. Job name could be found in `conf/deployment.json`:
```
dbx execute --cluster-name=<my-cluster> --job=<job-name>
```
- Make your first deployment from the local machine:
```
dbx deploy
```
- Launch your first pipeline as a new separate job, and trace the job status. Job name could be found in `conf/deployment.json`:
```
dbx launch --job <your-job-name> --trace
```
- For an in-depth local development and unit testing guidance, please refer to a generated `README.md` in the root of the project.

### Setting up CI/CD pipeline on GitHub Actions

- Create a new repository on GitHub
- Configure `DATABRICKS_HOST` and `DATABRICKS_TOKEN` secrets for your project in [GitHub UI](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets)
- Add a remote origin to the local repo
- Push the code 
- Open the GitHub Actions for your project to verify the state of the deployment pipeline

### Setting up CI/CD pipeline on Azure DevOps

- Create a new repository on GitHub
- Connect the repository to Azure DevOps
- Configure `DATABRICKS_HOST` and `DATABRICKS_TOKEN` secrets for your project in [Azure DevOps](https://docs.microsoft.com/en-us/azure/devops/pipelines/release/azure-key-vault?view=azure-devops)
- Add a remote origin to the local repo
- Push the code 
- Open the Azure DevOps UI to check the deployment status 
 
## Deployment file structure
A sample deployment file could be found in a generated project.

General file structure could look like this:
```json
{
    "<environment-name>": {
        "jobs": [
            {
                "name": "sample_project-sample",
                "existing_cluster_id": "some-cluster-id", 
                "libraries": [],
                "max_retries": 0,
                "spark_python_task": {
                    "python_file": "sample_project/jobs/sample/entrypoint.py",
                    "parameters": [
                        "--conf-file",
                        "conf/test/sample.json"
                    ]
                }
            }
        ]
    }
}
```
Per each environment you could describe any amount of jobs. Job description should follow the [Databricks Jobs API](https://docs.databricks.com/dev-tools/api/latest/jobs.html#create). 

However, there is some advanced behaviour for a `dbx deploy`.

When you run `dbx deploy` with a given deployment file (by default it takes the deployment file from `conf/deployment.json`), it will do te following:
- Find the deployment configuration in `--deployment-file` (default: `conf/deployment.json`) 
- Build .whl package in a given project directory
- Add this .whl package to a job definition
- Add all requirements from `--requirements-file` (default: `requirements.txt`)
- Create a new job or adjust existing job if the given job name exists.

Important thing about referencing is that you can also reference arbitrary local files. This is very handy for `python_file` section.
In the example above, the entrypoint file and the job configuration will be added to the job definition and uploaded to `dbfs` automatically. No explicit file upload is needed.

## FAQ

###
*Q*: I'm using [poetry](https://python-poetry.org/) for package management. Is it possible to use poetry together with this template?

*A*:  
    Yes, it's also possible, but the library management during cluster execution should be performed via `libraries` section of job description. 
    You also might need to disable the automatic rebuild for `dbx deploy` and `dbx execute` via `--no-rebuild` option. Finally, the built package should be in wheel format and located in `/dist/` directory.

###
*Q*: How can I add my Databricks Notebook to the `deployment.json`, so I can create a job out of it?
 
*A*:  
    Please follow [this](https://docs.databricks.com/dev-tools/api/latest/jobs.html#notebooktask) documentation section and add a notebook task definition into the deployment file.

###
*Q*: Is it possible to use `dbx` for non-Python based projects, for example Scala-based projects?

*A*:  
    Yes, it's possible, but the interactive mode `dbx execute` is not yet supported. However, you can just take the `dbx` wheel to your Scala-based project and reference your jar files in the deployment file, so the `dbx deploy` and `dbx launch` commands be available for you.

###
*Q*: I have a lot of interdependent jobs, and using solely JSON seems like a giant code duplication. What could solve this problem?

*A*:  
    You can implement any configuration logic and simply write the output into a custom `deployment.json` file and then pass it via `--deployment-file` option. 
    As an example, you can generate your configuration using Python script, or [Jsonnet](https://jsonnet.org/).

## Legal Information
This software is provided as-is and is not officially supported by Databricks through customer technical support channels. 
Support, questions, and feature requests can be communicated through the Issues page of this repo. 
Please see the legal agreement and understand that issues with the use of this code will not be answered or investigated by Databricks Support.

## Feedback
Issues with template? Found a bug? Have a great idea for an addition? Feel free to file an issue.

## Contributing
Have a great idea that you want to add? Fork the repo and submit a PR!

## Kudos
Project based on the [cookiecutter datascience project](https://drivendata.github.io/cookiecutter-data-science).
