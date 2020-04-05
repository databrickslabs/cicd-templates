#!/usr/bin/env python


import argparse
import sys
from os.path import isdir

parser = argparse.ArgumentParser()
parser.add_argument("dirname", help="Directory")
parser.add_argument("--pipeline-name", help="Pipeline Name")

args = parser.parse_args()
print(args)

if not isdir(args.dirname):
    print('Please specify existing directory with pipelines! ', args.dirname, ' directory does not exist.')
    print('Usage: ./run_pipeline.py directory_with_pipelines --pipeline-name my_pipeline')
    print('--pipeline-name parameter is optional')
    sys.exit(-100)

if args.pipeline_name:
    if not isdir(args.dirname+'/'+args.pipeline_name):
        print('Please specify existing pipeline name as --pipeline-name ',args.dirname+'/'+args.pipeline_name,' drectory does not exist.')
        print('Usage: ./run_pipeline.py directory_with_pipelines --pipeline-name my_pipeline')
        print('--pipeline-name parameter is optional')
        sys.exit(-100)

import mlflow
mlflow.set_tracking_uri("databricks")


from setuptools import sandbox
sandbox.run_setup('setup.py', ['clean', 'bdist_wheel'])

from databrickslabs_mlflowdepl import dev_cicd_pipeline
dev_cicd_pipeline.main(args.dirname, args.pipeline_name)