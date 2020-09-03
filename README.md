# *Databricks Labs CI/CD Templates*: Automated Databricks CI/CD pipeline creation and deployment

[![asciicast](https://asciinema.org/a/yltp4nutLlqUSQJJF6NnzTq9s.svg)](https://asciinema.org/a/yltp4nutLlqUSQJJF6NnzTq9s)

Demo: https://www.youtube.com/watch?v=Gjns_Z0zxt8&feature=emb_logo

Short instructions: 
1) Create new conda environment and activate it
2) Install [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
3) `cookiecutter https://github.com/databrickslabs/cicd-template` and `cd <your_project_name>` 
4) Install all requirements from requirements.txt:  `pip install -r requirements.txt` 
5) Install CI/CD templates API:  `pip install deployment/databrickslabs_cicdtemplates-0.2.3-py3-none-any.whl` 
6) Create new GitHub repo and push created project files there
7) Add `DATABRICKS_HOST` and `DATABRICKS_TOKEN` as Github secrets to the newly created repo
8) Implement DEV tests in dev-tests folder. These pipelines will be run on every push
9) Implement Integration Test pipelines in folder integration-test. These pipelines will be used for testing of new release
10) Implement production pipelines in pipeline folder. 

Please note:
1)Python 3.8 is not supported yet

Project Organization
------------
```bash
.
├── cicd1
│   └── model.py
├── create_cluster
├── deployment
│   └── databrickslabs_cicdtemplates-0.2.3-py3-none-any.whl
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
├── integration-tests
│   ├── pipeline1
│   │   ├── job_spec_aws.json
│   │   ├── job_spec_azure.json
│   │   └── pipeline_runner.py
│   └── pipeline2
│       ├── job_spec_aws.json
│       ├── job_spec_azure.json
│       └── pipeline_runner.py
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
├── run_now
├── run_pipeline
├── runtime_requirements.txt
├── setup.py
└── tests
    └── test_example.py
```
--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

## Azure Devops Cookiecutter instructions

Once you have created your project/repo for Azure Devops, you should do the following:

- Create a new Azure Devops Project/pipeline and link it to the "az_dev_ops/azure-pipelines.yml" file in your repo.
- Create a variable group named "Databricks-environment" that will be used in your az_dev_ops/azure-pipelines.yml pipeline definition. 
- Under that new variable group, create the following variables:
    - DATABRICKS_HOST: Databricks Host without orgid. Example "https://uksouth.azuredatabricks.net".
    - DATABRICKS_TOKEN: Databricks Personal Access Token of the user that will be used to run the automated pipelines.
    - MLFLOW_TRACKING_URI: Normally databricks.
    - CURRENT_CLOUD: Optional. Use the "CURRENT_CLOUD" environment variable to overwrite the cloud where the data pipelines will run. It takes precedence over the "cloud" parameter in the deployment.yaml file.

- If you want to change the name of the variable group, you should do it in Azure Devops first and then reflect that name in the variables/group section of your az_dev_ops/azure-pipelines.yml file. 


## Additional

- Use the "CURRENT_CLOUD" environment variable to overwrite the cloud where the data pipelines will run. It takes precedence over the "cloud" parameter in the deployment.yaml file.
