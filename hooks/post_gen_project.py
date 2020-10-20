import os
import shutil
import pathlib
import json
import pip

cicd_tool = '{{cookiecutter.cicd_tool}}'
cloud = '{{cookiecutter.cloud}}'
project = '{{cookiecutter.project_slug}}'
environment = '{{cookiecutter.environment}}'
workspace_dir = '{{cookiecutter.workspace_dir}}'

DEPLOYMENT = {
    "AWS": {
        environment: {
            "jobs": [
                {
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
                    "libraries": [],
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
                },
                {
                    "name": "%s-sample-integration-test" % project,
                    "new_cluster": {
                        "spark_version": "7.2.x-cpu-ml-scala2.12",
                        "node_type_id": "i3.xlarge",
                        "aws_attributes": {
                            "first_on_demand": 0,
                            "availability": "SPOT"
                        },
                        "num_workers": 1
                    },
                    "libraries": [],
                    "email_notifications": {
                        "on_start": [],
                        "on_success": [],
                        "on_failure": []
                    },
                    "max_retries": 0,
                    "spark_python_task": {
                        "python_file": "tests/integration/sample_test.py"
                    }
                }
            ]
        }
    },
    "Azure": {
        environment: {
            "jobs": [
                {
                    "name": "%s-sample" % project,
                    "new_cluster": {
                        "spark_version": "7.2.x-cpu-ml-scala2.12",
                        "node_type_id": "Standard_F4s",
                        "num_workers": 2
                    },
                    "libraries": [],
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
                },
                {
                    "name": "%s-sample-integration-test" % project,
                    "new_cluster": {
                        "spark_version": "7.2.x-cpu-ml-scala2.12",
                        "node_type_id": "Standard_F4s",
                        "num_workers": 1
                    },
                    "libraries": [],
                    "email_notifications": {
                        "on_start": [],
                        "on_success": [],
                        "on_failure": []
                    },
                    "max_retries": 0,
                    "spark_python_task": {
                        "python_file": "tests/integration/sample_test.py"
                    }
                }
            ]
        }
    }
}


def replace_vars(fpath: str):
    _path = pathlib.Path(fpath)
    content = _path.read_text().format(project_name=project, environment=environment)
    _path.write_text(content)


class PostProcessor:
    @staticmethod
    def process():

        if cicd_tool == 'GitHub Actions':
            os.remove("azure-pipelines.yml")

            replace_vars(".github/workflows/onpush.yml")
            replace_vars(".github/workflows/onrelease.yml")

        if cicd_tool == 'Azure DevOps':
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
        deployment_file = pathlib.Path("conf/deployment.json")
        deployment_file.parent.mkdir(exist_ok=True)
        deployment_file.write_text(deployment)

        pip.main(["install", "-U", "tools/dbx-0.7.0-py3-none-any.whl"])
        os.system("git init")
        os.system(f"dbx configure --environment={environment} --profile={environment} --workspace-dir={workspace_dir}")


if __name__ == '__main__':
    post_processor = PostProcessor()
    post_processor.process()
