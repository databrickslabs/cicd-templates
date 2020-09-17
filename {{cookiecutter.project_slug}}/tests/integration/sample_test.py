import unittest
from {{cookiecutter.project_name}}.jobs.sample.entrypoint import SampleJob
from uuid import uuid4
from pyspark.dbutils import DBUtils

class SampleJobIntegrationTest(unittest.TestCase):
    def setUp(self):

        self.test_dir = "dbfs:/tmp/tests/sample/%s" % str(uuid4())
        self.test_config = {
            "output_format": "delta",
            "output_path": self.test_dir
        }

        self.job = SampleJob(conf=self.test_config)
        self.dbutils = DBUtils(self.job.spark.sparkContext)
        self.spark = self.job.spark

    def test_sample(self):

        self.job.launch()

        output_count = (
            self.spark
                .read
                .format(self.test_config["output_format"])
                .load(self.test_config["output_path"])
                .count()
        )

        self.assertGreater(output_count, 0)

    def tearDown(self):
        self.dbutils.fs.rm(self.test_dir, True)

if __name__ == "__main__":
    unittest.main()
