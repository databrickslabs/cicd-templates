from setuptools import find_packages, setup
from {{cookiecutter.project_name}} import __version__

setup(
    name='{{cookiecutter.project_name}}',
    packages=find_packages(),
    version=__version__
)

setup(
    name='{{cookiecutter.project_slug}}',
    packages=find_packages(),
    version='{{cookiecutter.version}}',
    description='{{cookiecutter.description}}',
    author='{{cookiecutter.author}}',
    license='{{cookiecutter.license}}',
)
