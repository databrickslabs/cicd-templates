import os
import shutil
import pathlib

cicd_tool = '{{cookiecutter.cicd_tool}}'
cloud = '{{cookiecutter.cloud}}'


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


if __name__ == '__main__':
    post_processor = PostProcessor()
    post_processor.process()
