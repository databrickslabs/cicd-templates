import os
import shutil
import pathlib
import json
import yaml

cicd_tool = '{{cookiecutter.cicd_tool}}'
cloud = '{{cookiecutter.cloud}}'
project = '{{cookiecutter.project_slug}}'

DEPLOYMENT = {
    "AWS": {
        "test": {
            "dbfs": {
                "package": "dist/%s-0.0.1-py3-none-any.whl" % project
            },
            "jobs": {
                "name": "%s-sample" % project,
                "new_cluster": {
                    "spark_version": "7.2.x-cpu-ml-scala2.12",
                    "node_type_id": "i3.xlarge",
                    "aws_attributes": {
                        "first_on_demand": 0,
                        "availability": "SPOT"
                    },
                    "num_workers": 2
                },
                "libraries": [
                    {
                        "whl": "dist/%s-0.0.1-py3-none-any.whl" % project
                    }
                ],
                "email_notifications": {
                    "on_start": [],
                    "on_success": [],
                    "on_failure": []
                },
                "max_retries": 0,
                "spark_python_task": {
                    "python_file": "%s/jobs/sample/entrypoint.py" % project,
                    "parameters": [
                        "--conf-file",
                        "conf/test/sample.json"
                    ]
                }
            }
        }
    },
    "Azure": {
        "test": {
            "dbfs": {
                "package": "dist/%s-0.0.1-py3-none-any.whl" % project
            },
            "jobs": {
                "name": "%s-sample" % project,
                "new_cluster": {
                    "spark_version": "7.2.x-cpu-ml-scala2.12",
                    "node_type_id": "Standard_F4s",
                    "num_workers": 2
                },
                "libraries": [
                    {
                        "whl": "dist/%s-0.0.1-py3-none-any.whl" % project
                    }
                ],
                "email_notifications": {
                    "on_start": [],
                    "on_success": [],
                    "on_failure": []
                },
                "max_retries": 0,
                "spark_python_task": {
                    "python_file": "%s/jobs/sample/entrypoint.py" % project,
                    "parameters": [
                        "--conf-file",
                        "conf/test/sample.json"
                    ]
                }
            }
        }
    }
}


class PostProcessor:
    @staticmethod
    def process():

        shutil.rmtree("tests")

        if cicd_tool == 'GitHub Actions':
            os.remove("azure-pipelines.yml")

        if cicd_tool == 'Azure DevOps':
            # remove top-level file inside the generated folder
            shutil.rmtree(".github")

        if cloud == "Azure":
            aws_files = pathlib.Path(".").rglob("*aws.json")
            for _f in aws_files:
                _f.unlink()

        if cloud == "AWS":
            azure_files = pathlib.Path(".").rglob("*azure.json")
            for _f in azure_files:
                _f.unlink()

        deployment = json.dumps(DEPLOYMENT[cloud], indent=4)
        deployment_file = pathlib.Path(".dbx/deployment.json")
        deployment_file.parent.mkdir(exist_ok=True)
        deployment_file.write_text(deployment)


if __name__ == '__main__':
    post_processor = PostProcessor()
    post_processor.process()
