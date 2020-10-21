import unittest
from cookiecutter.main import cookiecutter
import tempfile
from path import Path
import pathlib
import logging
from uuid import uuid4
import shutil
import json
import yaml

TEMPLATE_PATH = str(pathlib.Path(".").absolute())


def validate_json(file_path):
    content = pathlib.Path(file_path).read_text()
    json.loads(content)


def validate_yaml(file_path):
    content = pathlib.Path(file_path).read_text()
    yaml.load(content, Loader=yaml.FullLoader)


class TemplateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.project_name = "cicd_templates_%s" % str(uuid4()).split("-")[0]
        logging.info("Test directory: %s" % self.test_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def test_template_aws_github(self):
        cookiecutter(template=TEMPLATE_PATH, no_input=True, output_dir=self.test_dir, extra_context={
            "project_name": self.project_name,
            "cloud": "AWS",
            "cicd_tool": "GitHub Actions"
        })

        full_path = Path(self.test_dir).joinpath(self.project_name)

        with full_path:
            all_json_files = pathlib.Path(".").rglob("*.json")
            for f in all_json_files:
                self.assertTrue("azure" not in str(f))

            self.assertTrue(Path(".github").exists())
            self.assertFalse(Path("azure-pipelines.yml").exists())

            validate_json("conf/deployment.json")
            #validate_yaml(".github/workflows/onpush.yml")
            #validate_yaml(".github/workflows/onrelease.yml")

    def test_template_azure_github(self):
        cookiecutter(template=TEMPLATE_PATH, no_input=True, output_dir=self.test_dir, extra_context={
            "project_name": self.project_name,
            "cloud": "Azure",
            "cicd_tool": "GitHub Actions"
        })

        full_path = Path(self.test_dir).joinpath(self.project_name)

        with full_path:
            all_json_files = pathlib.Path(".").rglob("*.json")
            for f in all_json_files:
                self.assertTrue("aws" not in str(f))

            self.assertTrue(Path(".github").exists())
            self.assertFalse(Path("azure-pipelines.yml").exists())
            self.assertTrue(Path("conf/deployment.json").exists())

            validate_json("conf/deployment.json")
            #validate_yaml(".github/workflows/onpush.yml")
            #validate_yaml(".github/workflows/onrelease.yml")

    def test_template_azure_azure_dev_ops(self):
        cookiecutter(template=TEMPLATE_PATH, no_input=True, output_dir=self.test_dir, extra_context={
            "project_name": self.project_name,
            "cloud": "Azure",
            "cicd_tool": "Azure DevOps"
        })

        full_path = Path(self.test_dir).joinpath(self.project_name)

        with full_path:
            all_json_files = pathlib.Path(".").rglob("*.json")
            for f in all_json_files:
                self.assertTrue("aws" not in str(f))

            self.assertTrue(Path("azure-pipelines.yml").exists())
            self.assertFalse(Path(".github").exists())
            self.assertTrue(Path("conf/deployment.json").exists())

            validate_json("conf/deployment.json")


if __name__ == '__main__':
    unittest.main()
