import json
import os
import shutil

from path import Path

cicd_tool = '{{cookiecutter.cicd_tool}}'
cloud = '{{cookiecutter.cloud}}'
project = '{{cookiecutter.project_slug}}'
environment = 'default'
profile = '{{cookiecutter.profile}}'
workspace_dir = '{{cookiecutter.workspace_dir}}'
artifact_location = '{{cookiecutter.artifact_location}}'

PROJECT_FILE_CONTENT = {
    "environments": {
        environment: {
            "profile": profile,
            "workspace_dir": workspace_dir,
            "artifact_location": artifact_location
        }
    }
}

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


def replace_vars(file_path: str):
    _path = Path(file_path)
    content = (
        _path
            .read_text()
            .format(project_name=project, environment=environment, profile=profile)
    )
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

        deployment = json.dumps(DEPLOYMENT[cloud], indent=4)
        deployment_file = Path("conf/deployment.json")
        if not deployment_file.parent.exists():
            deployment_file.parent.mkdir()
        deployment_file.write_text(deployment)
        project_file = Path(".dbx/project.json")
        if not project_file.parent.exists():
            project_file.parent.mkdir()
        deployment_file.write_text(deployment)
        project_file.write_text(json.dumps(PROJECT_FILE_CONTENT, indent=2))
        Path(".dbx/lock.json").write_text("{}")
        os.system("git init")


if __name__ == '__main__':
    post_processor = PostProcessor()
    post_processor.process()
