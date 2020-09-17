import unittest
from cookiecutter.main import cookiecutter
import tempfile
from path import Path
import pathlib
import logging
from uuid import uuid4
import shutil
import os

TEMPLATE_PATH = str(pathlib.Path(".").absolute())


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
            self.assertFalse(Path("tests").exists())  # checking that we've removed the top-level directory with tests

            all_json_files = pathlib.Path(".").rglob("*.json")
            for f in all_json_files:
                self.assertTrue("azure" not in str(f))

            self.assertTrue(Path(".github").exists())
            self.assertFalse(Path("azure-pipelines.yml").exists())
            self.assertTrue(Path(".dbx/deployment.json").exists())

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
            self.assertTrue(Path(".dbx/deployment.json").exists())

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
            self.assertTrue(Path(".dbx/deployment.json").exists())


if __name__ == '__main__':
    unittest.main()
