from {{cookiecutter.project_slug}}.common import Job


class SampleJob(Job):

    def default_conf(self):
        return {
            "output_format": "delta",
            "output_path": "dbfs:/dbx/tmp/test/{{cookiecutter.project_slug}}"
        }

    def launch(self):
        self.logger.info("Launching bootstrap job")

        df = self.spark.range(0, 1000)

        df.write.format(self.conf["output_format"]).mode("overwrite").save(self.conf["output_path"])

        self.logger.info("Bootstrap job finished!")

if __name__ == "__main__":
    job = SampleJob()
    job.launch()
