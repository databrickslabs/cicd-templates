import unittest
from .utils import CicdTemplatesTest
import logging


class LocalExecuteTest(CicdTemplatesTest):
    def tearDown(self) -> None:
        logging.info(self.project_path)

    def test_local_execute_azure(self):
        with self.project_path:
            self.execute_command("pip install -U tools/dbx-0.7.0-py3-none-any.whl")
            self.execute_command("dbx deploy")
            self.execute_command(f"dbx execute --cluster-name=cicd-templates.testing --job={self.project_name}-sample")


if __name__ == '__main__':
    unittest.main()
