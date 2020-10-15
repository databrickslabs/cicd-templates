# Databricks Labs CI/CD Templates

This repository provides a template for automated Databricks CI/CD pipeline creation and deployment.

Short instructions: 
- Create new conda environment and activate it
- Install requirements for cookiecutter project generation:
```bash
pip install \
    -r https://raw.githubusercontent.com/databrickslabs/cicd-templates/dbx/requirements.txt
```
- Create new project using cookiecutter template:
```
cookiecutter https://github.com/databrickslabs/cicd-templates --checkout dbx
```
- Follow the documentation in generated `<project-name>/README.md` file.


Project based on the [cookiecutter datascience project](https://drivendata.github.io/cookiecutter-data-science).
