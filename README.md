# Databricks Labs CI/CD Templates

This repository provides a template for automated Databricks CI/CD pipeline creation and deployment.

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
- `.dbx` folder is a system folder, where metadata about environments and execution context is located.
- `sample_project` - Python package with your code
- `tests` - directory with your package tests
- `conf/deployment.json` - deployment configuration file. Please read the [following section](#deployment-file-structure) for a full reference.

## Quickstart

> **_NOTE:_**  
As a prerequisite, you should have installed [databricks-cli](https://docs.databricks.com/dev-tools/cli/index.html) with a [configured profile](https://docs.databricks.com/dev-tools/cli/index.html#set-up-authentication).
In this instruction we're based on [Databricks Runtime 7.3 LTS ML](https://docs.databricks.com/release-notes/runtime/7.3ml.html). 
If you don't need to use ML libraries, we still recommend to use ML-based version due to [`%pip` magic support](https://docs.databricks.com/libraries/notebooks-python-libraries.html).

### Local steps
Perform the following actions in your development environment:
- Create new conda environment and activate it:
```bash
conda create -n <your-environment-name> python=3.7.5
conda activate <your-environment-name>
```
- Install cookiecutter:
```bash
pip install cookiecutter
```
- Create new project using cookiecutter template. Notice the environment name and profile name:
```
cookiecutter https://github.com/databrickslabs/cicd-templates --checkout dbx
```
- Switch to the project directory and install `dbx`:
```bash
pip install -U tools/dbx-0.7.0-py3-none-any.whl
```
- Configure your first environment:
```
dbx configure -e <your-environment-name> --profile <your-profile-name>
```
- Check the content of `conf/deployment.json` file for a proper deployment configuration. You can find a detailed doc on the `deployment.json` file [here](#deployment-file-structure).
- Launch and debug your code on an interactive cluster via:
```
dbx execute -e <your-environment-name> --cluster-name=<my-cluster> --job=<job-name>
```
- Make your first deployment:
```
dbx deploy -e <your-environment-name> 
```
- Launch your first pipeline as a new separate job:
```
dbx launch -e <your-environment-name> --job <your-job-name> --trace
```

### Setting up CI/CD pipeline on GitHub Actions

- Create a new repository on GitHub
- Add a remote origin to the local repo
- Push the code 
- Configure `DATABRICKS_HOST` and `DATABRICKS_TOKEN` secrets for your project in [GitHub UI](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets).
- Open the GitHub Actions for your project to verify the state of the deployment pipeline
 
 
## Deployment file structure
A sample deployment file could be found in a generated project.

General file structure looks like this:
```json
{
    "<environment-name>": {
        "jobs": [
            {
                "name": "sample_project-sample",
                "new_cluster": {}, 
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
At the top-level, you have different environments. 
Per each environment you could describe any amount of jobs. Job description should follow the [Databricks Jobs API](https://docs.databricks.com/dev-tools/api/latest/jobs.html#create). 

However, there is some advanced behaviour for a `dbx launch`.

When you run `dbx launch` with a given deployment file (by default it takes the deployment file from `conf/deployment.json`), it will do te following:
- Find the deployment conf in deployment-file
- Build .whl package in a given project directory
- Add this .whl package to a job definition
- Add all requirements from `--requirements-file` (default: `requirements.txt`)
- Create a new job or adjust existing job if the given job name exists.

Important thing about referencing local files is that you can also reference arbitrary local files. This is very handy for `python_file` section.
In the example above, the entrypoint file and the job configuration will be added to the job definition and uploaded to `dbfs` automatically. No explicit file upload is needed.
 
## Kudos
Project based on the [cookiecutter datascience project](https://drivendata.github.io/cookiecutter-data-science).
