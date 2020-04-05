#!/usr/bin/env python

import sys
from os.path import isdir

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Directory")
parser.add_argument("pipeline", help="Pipeline Name")
parser.add_argument("--cluster-id", help="Cluster ID")
parser.add_argument("--new-cluster", help="Create new cluster", action="store_true")
args = parser.parse_args()
print(args)

if not isdir(args.dir):
    print('Please specify existing directory with pipelines! ', args.dir, ' directory does not exist.')
    sys.exit(-100)

if not isdir(args.dir+'/'+args.pipeline):
    print('Please specify existing pipeline name as --pipeline-name ',args.dir+'/'+args.pipeline,' drectory does not exist.')
    sys.exit(-100)

if args.cluster_id and args.new_cluster:
    print('create_cluster parameter is set to True and cluster_id is specified. Exiting...')
    sys.exit(-100)

if not (args.cluster_id) and not (args.new_cluster):
    print('create_cluster parameter is set to False and cluster_id is not specified. Exiting...')
    sys.exit(-100)

import mlflow
mlflow.set_tracking_uri("databricks")

from setuptools import sandbox
sandbox.run_setup('setup.py', ['clean', 'bdist_wheel'])

from databrickslabs_mlflowdepl import cluster_and_libraries
cluster_and_libraries.main(args.dir, args.pipeline, args.cluster_id)