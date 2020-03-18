

ML deploy CICD pipeline

Short instructions: 
1) Install [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
2) `cookiecutter git@github.com:databricks/mlflow-deployments.git` (or the HTTPS equivalent)
3) Create new GitHub repo and push created project files there
4) Add `DATABRICKS_HOST` and `DATABRICKS_TOKEN` as Github secrets to the newly created repo
5) Implement DEV tests in dev-tests folder. These pipelines will be run on every push
6) Implement Integration Test pipelines in folder integration-test. These pipelines will be used for testing of new release
7) Implement production pipelines in pipeline folder. 

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
