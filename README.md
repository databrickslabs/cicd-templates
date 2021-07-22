# Databricks Labs CI/CD Templates

This repository provides a template for automated Databricks CI/CD pipeline creation and deployment.

Table of Contents
=================

   * [Databricks Labs CI/CD Templates](#databricks-labs-cicd-templates)
      * [Table of Contents](#table-of-contents)
      * [Sample project structure (with GitHub Actions)](#sample-project-structure-with-github-actions)
      * [Sample project structure (with Azure DevOps)](#sample-project-structure-with-azure-devops)
      * [Sample project structure (with GitLab)](#sample-project-structure-with-gitlab)
      * [Note on dbx](#note-on-dbx)
      * [Quickstart](#quickstart)
         * [Local steps](#local-steps)
         * [Setting up CI/CD pipeline on GitHub Actions](#setting-up-cicd-pipeline-on-github-actions)
         * [Setting up CI/CD pipeline on Azure DevOps](#setting-up-cicd-pipeline-on-azure-devops)
         * [Setting up CI/CD pipeline on Gitlab](#setting-up-cicd-pipeline-on-gitlab)
      * [Deployment file structure](#deployment-file-structure)
      * [Different deployment types](#different-deployment-types)
         * [Deployment for Run Submit API](#deployment-for-run-submit-api)
         * [Deployment for Run Now API](#deployment-for-run-now-api)
      * [Troubleshooting](#troubleshooting)
      * [FAQ](#faq)
      * [Legal Information](#legal-information)
      * [Feedback](#feedback)
      * [Contributing](#contributing)
      * [Kudos](#kudos)
    
## Sample project structure (with GitHub Actions)
```
.
├── .dbx
│   └── project.json
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
└── unit-requirements.txt
```

Some explanations regarding structure:
- `.dbx` folder is an auxiliary folder, where metadata about environments and execution context is located.
- `sample_project` - Python package with your code (the directory name will follow your project name)
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
└── unit-requirements.txt
```

Some explanations regarding structure:
- `.dbx` folder is an auxiliary folder, where metadata about environments and execution context is located.
- `sample_project_azure_dev_ops` - Python package with your code (the directory name will follow your project name)
- `tests` - directory with your package tests
- `conf/deployment.json` - deployment configuration file. Please read the [following section](#deployment-file-structure) for a full reference.
- `azure-pipelines.yml` - Azure DevOps Pipelines workflow definition

## Sample project structure (with GitLab)
```
.
├── .dbx
│   └── project.json
├── .gitignore
├── README.md
├── .gitlab-ci.yml
├── conf
│   ├── deployment.json
│   └── test
│       └── sample.json
├── pytest.ini
├── sample_project_gitlab
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
└── unit-requirements.txt
```

Some explanations regarding structure:
- `.dbx` folder is an auxiliary folder, where metadata about environments and execution context is located.
- `sample_project_gitlab` - Python package with your code (the directory name will follow your project name)
- `tests` - directory with your package tests
- `conf/deployment.json` - deployment configuration file. Please read the [following section](#deployment-file-structure) for a full reference.
- `.gitlab-ci.yml` - GitLab CI/CD workflow definition

## Note on dbx

> **_NOTE:_**  
[dbx](https://github.com/databrickslabs/dbx) is a CLI tool for advanced Databricks jobs management. 
It can be used separately from cicd-templates, and if you would like to preserve your project structure, please refer to dbx documentation on how to use it with customized project structure.


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
- If you would like to be able to run local unit tests, you'll need JDK. If you don't have one, It can be installed via:
```
conda install -c anaconda "openjdk=8.0.152"
```
- Install cookiecutter and path:
```bash
pip install cookiecutter path
```
- Create new project using cookiecutter template:
```
cookiecutter https://github.com/databrickslabs/cicd-templates
```
- Install development dependencies:
```bash
pip install -r unit-requirements.txt
```
- Install generated package in development mode:
```
pip install -e .
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
- Configure `DATABRICKS_HOST` and `DATABRICKS_TOKEN` secrets for your project in [Azure DevOps](https://docs.microsoft.com/en-us/azure/devops/pipelines/release/azure-key-vault?view=azure-devops). Note that secret variables must be mapped to env as mentioned [here](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch#secret-variables) using the syntax `env:` for example:
```
variables:
- group: Databricks-environment
stages:
...
...
    - script: |
        dbx deploy
      env:
        DATABRICKS_TOKEN: $(DATABRICKS_TOKEN)
```
- Add a remote origin to the local repo
- Push the code 
- Open the Azure DevOps UI to check the deployment status 

### Setting up CI/CD pipeline on Gitlab

- Create a new repository on Gitlab
- Configure `DATABRICKS_HOST` and `DATABRICKS_TOKEN` secrets for your project in [GitLab UI](https://docs.gitlab.com/ee/ci/variables/#create-a-custom-variable-in-the-ui)
- Add a remote origin to the local repo
- Push the code 
- Open the GitLab CI/CD UI to check the deployment status 

 
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

When you run `dbx deploy` with a given deployment file (by default it takes the deployment file from `conf/deployment.json`), the following actions will be performed:
- Find the deployment configuration in `--deployment-file` (default: `conf/deployment.json`) 
- Build .whl package in a given project directory (could be disabled via `--no-rebuild` option)
- Add this .whl package to a job definition
- Add all requirements from `--requirements-file` (default: `requirements.txt`). Step will be skipped if requirements file is non-existent.
- Create a new job or adjust existing job if the given job name exists. Job will be found by it's name.

Important thing about referencing is that you can also reference arbitrary local files. This is very handy for `python_file` section.
In the example above, the entrypoint file and the job configuration will be added to the job definition and uploaded to `dbfs` automatically. No explicit file upload is needed.

## Different deployment types

Databricks Jobs API provides two methods for launching a particular workload:
- [Run Submit API](https://docs.databricks.com/dev-tools/api/latest/jobs.html#runs-submit)
- [Run Now API](https://docs.databricks.com/dev-tools/api/latest/jobs.html#run-now)

Main logical difference between these methods is that Run Submit API allows to submit a workload directly without creating a job.
Therefore, we have two deployment types - one for Run Submit API, and one for Run Now API. 

### Deployment for Run Submit API

To deploy only the files and not to override the job definitions, do the following:

```bash
dbx deploy --files-only
```

To launch the file-based deployment:
```
dbx launch --as-run-submit --trace
```

This type of deployment is handy for working in different branches, and it won't affect the job definition.

### Deployment for Run Now API

To deploy files and update the job definitions:

```bash
dbx deploy
```

To launch the file-based deployment:
```
dbx launch --job=<job-name>
```

This type of deployment shall be mainly used in automated way during new release. 
`dbx deploy` will change the job definition (unless `--files-only` option is provided).

## Troubleshooting

###
*Q*: When running ```dbx deploy``` I'm getting the following exception ```json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)``` and stack trace:
```
...
  File ".../lib/python3.7/site-packages/dbx/utils/common.py", line 215, in prepare_environment
    experiment = mlflow.get_experiment_by_name(environment_data["workspace_dir"])
...

json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

What could be causing it and what is the potential fix?

*A*:  
We've seen this exception when in the profile the ```host=https://{domain}/?o={orgid}``` format is used for Azure. It is valid for the databricks cli, but not for the API. If that's the cause, once the "?o={orgid}" suffix is removed, the problem should be gone.

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

###
*Q*: How can I secure the project environment?

*A*:  
From the state serialization perspective, your code and deployments are stored in two separate storages:
- workspace directory -this directory is stored in your workspace, described per-environment and defined in `.dbx/project.json`, in `workspace_dir` field.
        To control access to this directory, please use [Workspace ACLs](https://docs.databricks.com/security/access-control/workspace-acl.html).  
- artifact location - this location is stored in DBFS, described per-environment and defined in `.dbx/project.json`, in `artifact_location` field.
        To control access this location, please use credentials passthrough (docs for [ADLS](https://docs.microsoft.com/en-us/azure/databricks/security/credential-passthrough/adls-passthrough) and for [S3](https://docs.databricks.com/security/credential-passthrough/index.html)).

###
*Q*: I would like to use self-hosted (private) pypi repository. How can I configure my deployment and CI/CD pipeline?

*A*:  
To set up this scenario, there are some settings to be applied:
- Databricks driver should have network access to your pypi repository
- Additional step to deploy your package to pypi repo should be configured in CI/CD pipeline
- Package re-build and generation should be disabled via `--no-rebuild --no-package` arguments for `dbx execute`
- Package reference should be configured in job description

Here is a sample for `dbx deploy` command:
```
dbx deploy --no-rebuild --no-package
```

Sample section to `libraries` configuration:
```json
{
    "pypi": {"package": "my-package-name==1.0.0", "repo": "my-repo.com"}
}
```

###
*Q*: What is the purpose of `init_adapter` method in SampleJob?

*A*: 
This method should be primarily used for adapting configuration for `dbx execute` based run. 
By using this method, you can provide an initial configuration in case if `--conf-file` option is not provided.  

###
*Q*: I don't like the idea of hosting the host and token variables into `~/.databrickscfg` file inside the CI pipeline. How can I make this setup more secure?

*A*:  
`dbx` now supports environment variables, provided via `DATABRICKS_HOST` and `DATABRICKS_TOKEN`. 
If these variables are defined in env, no `~/.databrickscfg` file needed.

## Legal Information
This software is provided as-is and is not officially supported by Databricks through customer technical support channels. 
Support, questions, and feature requests can be communicated through the Issues page of this repo. 
Please see the legal agreement and understand that issues with the use of this code will not be answered or investigated by Databricks Support.

## Feedback
Issues with template? Found a bug? Have a great idea for an addition? Feel free to file an issue.

## Contributing
Have a great idea that you want to add? Fork the repo and submit a PR!

## Kudos
- Project based on the [cookiecutter datascience project](https://drivendata.github.io/cookiecutter-data-science)
- README.md ToC generated via [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)
