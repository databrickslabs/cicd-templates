from setuptools import find_packages, setup

setup(
    name='{{cookiecutter.project_slug}}',
    packages=find_packages(),
    version='{{cookiecutter.version}}',
    description='{{cookiecutter.description}}',
    author='{{cookiecutter.author}}',
    license='{{cookiecutter.license}}',
)
