from {{cookiecutter.project_slug}}.common import Job


class SampleJob(Job):
    def init_adapter(self):
        if not self.conf:
            self.logger.info(
                "Init configuration was not provided, using configuration from default_init method"
            )
            self.conf = {
                "output_format": "delta",
                "output_path": "dbfs:/dbx/tmp/test/interactive/{{cookiecutter.project_slug}}",
            }
        else:
            self.logger.info("Init configuration is already provided")

    def launch(self):
        self.logger.info("Launching sample job")

        listing = self.dbutils.fs.ls("dbfs:/")

        for l in listing:
            self.logger.info(f"DBFS directory: {l}")

        df = self.spark.range(0, 1000)

        df.write.format(self.conf["output_format"]).mode("overwrite").save(
            self.conf["output_path"]
        )

        self.logger.info("Sample job finished!")


if __name__ == "__main__":
    job = SampleJob()
    job.launch()
