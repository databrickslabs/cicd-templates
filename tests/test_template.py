import json
import logging
import pathlib
import shutil
import tempfile
import unittest
from uuid import uuid4

from cookiecutter.main import cookiecutter
from path import Path
import os

TEMPLATE_PATH = str(pathlib.Path(".").absolute())


def validate_json(file_path):
    content = pathlib.Path(file_path).read_text()
    json.loads(content)


class TemplateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.project_name = "cicd_templates_%s" % str(uuid4()).split("-")[0]
        logging.info("Test directory: %s" % self.test_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def test_template_azure_github(self):
        cookiecutter(template=TEMPLATE_PATH, no_input=True, output_dir=self.test_dir, extra_context={
            "project_name": self.project_name,
            "cloud": "Azure",
            "cicd_tool": "GitHub Actions"
        })

        project_path = Path(self.test_dir).joinpath(self.project_name)

        with project_path:
            self.assertTrue(Path(".github").exists())
            self.assertFalse(Path("azure-pipelines.yml").exists())
            self.assertTrue(Path("conf/deployment.json").exists())

            validate_json("conf/deployment.json")
            os.system("pip install -U tools/dbx-0.7.0-py3-none-any.whl")


if __name__ == '__main__':
    unittest.main()
