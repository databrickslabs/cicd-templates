# cat post_gen_project.py
import os
import shutil

print(os.getcwd())  # prints /absolute/path/to/{{cookiecutter.project_slug}}

def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)

cicd_tool = '{{cookiecutter.cicd_tool}}'

if cicd_tool == 'git':
    # remove top-level file inside the generated folder
    remove('az_dev_ops')
if cicd_tool == 'az_dev_ops':
    # remove top-level file inside the generated folder
    remove('.github')
	
