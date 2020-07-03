# *Databricks Labs CI/CD Templates* Tutorial

## Introduction
In this tutorial we will build a project that will help us predict if the loans in our dataset are going to be fully repaid. 
We will rely on lending club dataset, which is available on Databricks out of the box. 
You can review the result project in the following GitHub repo: https://github.com/mshtelma/lendingclubsscoringdemo

## Installation

At first we are going to create a new conda environment and install cookiecutter package there: 
```bash
conda create -n lendingclub_scoring  python=3.7
conda activate lendingclub_scoring
pip install cookiecutter databricks_cli
```
As a next step we will set up Databricks CLI, because it will make it easier for us to interact with Databricks clusters:
```bash
pip install databricks_cli
databricks configure --token
```
After that we will have to enter the URL of our Databricks workspace followed by the token. 
You can find more information about setting up Databricks CLI here: https://docs.databricks.com/dev-tools/cli/index.html

##Project creation
Now we can create our new project using cookiecutter template:

```bash
cookiecutter https://github.com/databrickslabs/cicd-templates
```
The wizard will ask you a couple of simple questions about your new project. 
Let's assume that we will name it lendingclub_scoring. 
Now we can go inside our project directory: 
```bash
cd lendingclub_scoring
```
In this directory we can find project template filled out with sample pipelines and tests. 
We will have to implement them. 

## Setting up GitHub repo for our project
Let's add all files to git and commit our changes using the following commands:
```bash
git init
git add .
git commit -m "first commit"
```
Now is the time to set up our GitHub repo. 
In order to integrate GitHub repository with the Databricks workspace, workspace URL and Personal Authentication token (PAT) must be configured as GitHub secrets. 
Workspace URL must be configured as DATABRICKS_HOST secret and token as DATABRICKS_TOKEN.
Now we are ready to make a first push: 

```bash
git remote add origin <your git url>
git push -u origin master
```
After the push GitHub Actions will see our push and run our test pipelines defined in dev-tests directory. 

## Implementing logic
In this project we will have three pipelines: 
* Training Pipeline: This pipeline  trains a new model version using the latest data and logs it to MLflow as candidate model
* Evaluation Pipeline: This pipeline will find the best candidate model (assuming we can have more than one training pipeline that might train different models) and compare it with the production model, which is currently deployed. If the new model is better that the existing production model, it will deploy the candiate model to production using MLflow Model Registry
* Consumer Pipeline: This pipeline uses MLFlow Model Registry to get the latest production version of the model and uses it to predict which loans will be fully repaid.  

## Training
The training pipeline is implemented in the following class: https://github.com/mshtelma/lendingclubsscoringdemo/blob/master/lendingclub_scoring/pipelines/LendingClubTrainingPipeline.py


## WIP: More to come



