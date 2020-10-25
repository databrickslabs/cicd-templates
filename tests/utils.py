import logging
import os
import pathlib
import shutil
import tempfile
import unittest
from uuid import uuid4

from cookiecutter.main import cookiecutter
from path import Path


class CicdTemplatesTest(unittest.TestCase):
    TEMPLATE_PATH = str(pathlib.Path(".").absolute())

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.project_name = "cicd_templates_%s" % str(uuid4()).split("-")[0]
        logging.info(f"Launching test with project name {self.project_name} and test dir {self.test_dir}")
        self.prepare_repository()
        self.project_path = Path(self.test_dir).joinpath(self.project_name)

    def tearDown(self) -> None:
        logging.info(f"Deleting test directory: {self.test_dir}")
        shutil.rmtree(self.test_dir)

    def prepare_repository(self):
        cookiecutter(template=self.TEMPLATE_PATH, no_input=True, output_dir=self.test_dir, extra_context={
            "project_name": self.project_name,
            "cloud": "Azure",
            "cicd_tool": "GitHub Actions",
            "profile": "dbx-dev-azure"
        })

    def execute_command(self, cmd):
        exit_code = os.system(cmd)
        self.assertEqual(exit_code, 0)
