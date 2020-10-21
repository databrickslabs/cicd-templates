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

## Instructions
In this instruction we're based on [Databricks Runtime 7.3 LTS ML](https://docs.databricks.com/release-notes/runtime/7.3ml.html). 
If you don't need to use ML libraries, we still recommend to use ML-based version due to `%pip` magic support.
- Create new conda environment and activate it:
```bash
conda create -n <your-environment-name> python=3.7.5
conda activate <your-environment-name>
```
- Install cookiecutter:
```bash
pip install cookiecutter
```
- Create new project using cookiecutter template:
```
cookiecutter https://github.com/databrickslabs/cicd-templates --checkout dbx
```
- Follow the documentation in generated `<project-name>/README.md` file.

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

However, there is some advanced behaviour for a `dbx launch command`.

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
