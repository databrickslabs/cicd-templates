# *Databricks Labs CI/CD Templates*: Automated Databricks CI/CD pipeline creation and deployment

[![asciicast](https://asciinema.org/a/yltp4nutLlqUSQJJF6NnzTq9s.svg)](https://asciinema.org/a/yltp4nutLlqUSQJJF6NnzTq9s)


Short instructions: 
1) Install [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and dependencies from requirements.txt
2) `cookiecutter git@github.com:databricks/mlflow-deployments.git` (or the HTTPS equivalent)
3) Create new GitHub repo and push created project files there
4) Add `DATABRICKS_HOST` and `DATABRICKS_TOKEN` as Github secrets to the newly created repo
5) Implement DEV tests in dev-tests folder. These pipelines will be run on every push
6) Implement Integration Test pipelines in folder integration-test. These pipelines will be used for testing of new release
7) Implement production pipelines in pipeline folder. 

Please note:
1)Python 3.8 is not supported yet

Project Organization
------------
```bash
├── deployment
│   ├── __init__.py
│   ├── deployment.py
│   ├── dev_cicd_pipeline.py
│   └── release_cicd_pipeline.py
├── deployment.yaml
├── dev-tests
│   ├── pipeline1
│   │   ├── job_spec_aws.json
│   │   ├── job_spec_azure.json
│   │   └── pipeline_runner.py
│   └── pipeline2
│       ├── job_spec_aws.json
│       ├── job_spec_azure.json
│       └── pipeline_runner.py
├── docs
│   ├── Makefile
│   ├── commands.rst
│   ├── conf.py
│   ├── getting-started.rst
│   ├── index.rst
│   └── make.bat
├── integration-tests
│   ├── pipeline1
│   │   ├── job_spec_aws.json
│   │   ├── job_spec_azure.json
│   │   └── pipeline_runner.py
│   └── pipeline2
│       ├── job_spec_aws.json
│       ├── job_spec_azure.json
│       └── pipeline_runner.py
├── mlflow_deployments_sample_project
│   ├── __init__.py
│   ├── data
│   │   ├── __init__.py
│   │   └── make_dataset.py
│   ├── features
│   │   ├── __init__.py
│   │   └── build_features.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── predict_model.py
│   │   └── train_model.py
│   └── visualization
│       ├── __init__.py
│       └── visualize.py
├── notebooks
├── pipelines
│   ├── pipeline1
│   │   ├── job_spec_aws.json
│   │   ├── job_spec_azure.json
│   │   └── pipeline_runner.py
│   └── pipeline2
│       ├── job_spec_aws.json
│       ├── job_spec_azure.json
│       └── pipeline_runner.py
├── requirements.txt
├── runtime_requirements.txt
├── setup.py
└── tests
    └── test_smth.py

18 directories, 43 files
```
--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

## Azure Devops Cookie-cutter instructions

Once you have created your project/repo for Azure Devops, you should do the following:

- Create a new Azure Devops Project/pipeline and link it to the "az_dev_ops/azure-pipelines.yml" file in your repo.
- Create a variable group named "Databricks-environment" that will be used in your az_dev_ops/azure-pipelines.yml pipeline definition. 
- Under that new variable group, create the following variables:
    - DATABRICKS_HOST: Databricks Host without orgid. Example "https://uksouth.azuredatabricks.net".
    - DATABRICKS_TOKEN: Databricks Personal Access Token of the user that will be used to run the automated pipelines.
    - MLFLOW_TRACKING_URI: Normally databricks.
    - DATABRICKS_USERNAME: Username of the system user in the Databricks environment under which the artifacts will be registered.
    - CURRENT_CLOUD: Optional. Use the "CURRENT_CLOUD" environment variable to overwrite the cloud where the data pipelines will run. It takes precedence over the "cloud" parameter in the deployment.yaml file.

- If you want to change the name of the variable group, you should do it in Azure Devops first and then reflect that name in the variables/group section of your az_dev_ops/azure-pipelines.yml file. 


## Additional

- Use the "CURRENT_CLOUD" environment variable to overwrite the cloud where the data pipelines will run. It takes precedence over the "cloud" parameter in the deployment.yaml file.
