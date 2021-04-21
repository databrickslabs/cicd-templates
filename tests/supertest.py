# Databricks notebook source
# MAGIC %python
# MAGIC diamonds = spark.read.csv("/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv", header="true", inferSchema="true")
# MAGIC diamonds.write.format("delta").save("/delta/diamonds")
