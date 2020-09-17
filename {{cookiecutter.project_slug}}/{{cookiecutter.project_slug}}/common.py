import json
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from logging import Logger
from typing import Dict, Any

from pyspark.sql import SparkSession


# abstract class for jobs
class Job(ABC):
    def __init__(self, spark=None, conf=None):
        self.spark = self._prepare_spark(spark)
        self._prepare_logger()
        self._prepare_conf(conf)
        self._log_conf()

    def _prepare_conf(self, conf):
        if conf is not None:
            self.conf = conf
        else:
            self.conf = self._provide_config()

    @staticmethod
    def _prepare_spark(spark) -> SparkSession:
        if not spark:
            return SparkSession.builder.getOrCreate()
        else:
            return spark

    def _provide_config(self):
        self.logger.info("Reading configuration from --conf-file job option")
        conf_file = self._get_conf_file()
        return self._read_config(conf_file)

    @property
    def conf(self):
        return self._conf

    @conf.setter
    def conf(self, value):
        self._conf = value

    @staticmethod
    def _get_conf_file():
        p = ArgumentParser()
        p.add_argument("--conf-file", required=True, type=str)
        namespace = p.parse_args()
        return namespace.conf_file

    def _read_config(self, conf_file) -> Dict[str, Any]:
        raw_content = "".join(self.spark.read.format("text").load(conf_file).toPandas()["value"].tolist())
        config = json.loads(raw_content)
        return config

    def _prepare_logger(self) -> Logger:
        log4j_logger = self.spark._jvm.org.apache.log4j
        self.logger = log4j_logger.LogManager.getLogger(self.__class__.__name__)

    def _log_conf(self):
        # log parameters
        self.logger.info("Launching job with configuration parameters:")
        for key, item in self.conf.items():
            self.logger.info("\t Parameter: %-30s with value => %-30s" % (key, item))

    @abstractmethod
    def launch(self):
        pass
