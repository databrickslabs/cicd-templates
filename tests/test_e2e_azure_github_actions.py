import json
import logging
import pathlib
import unittest
from github import Github, Workflow
from path import Path
import os
from dotenv import load_dotenv
from nacl import encoding, public
import typing as t
import requests as r
import base64
import time
import shutil
from .utils import CicdTemplatesTest

if "GH_ACCESS_TOKEN" not in os.environ:
    load_dotenv(".env")


def validate_json(file_path):
    content = pathlib.Path(file_path).read_text()
    json.loads(content)


def get_encryption_key(
        gh_repo: str,
        gh_token: str) -> t.Tuple[str, str]:
    # GET /repos/:owner/:repo/actions/secrets/public-key
    public_key = r.get(
        f'https://api.github.com/repos/{gh_repo}/actions/secrets/public-key',
        headers={
            'Authorization': f'token {gh_token}',
            'Content-Type': 'application/json',
        },
    ).json()
    return public_key['key'], public_key['key_id']


def upload_secret(
        gh_repository: str,
        gh_token: str,
        secret_name: str,
        secret_value: str) -> None:
    # PUT /repos/:owner/:repo/actions/secrets/:name
    encryption_key, encryption_key_id = get_encryption_key(gh_repository, gh_token)
    r.put(
        (
            f'https://api.github.com/repos/{gh_repository}/'
            f'actions/secrets/{secret_name}'
        ),
        headers={
            'Authorization': f'token {gh_token}',
        },
        json={
            'key_id': encryption_key_id,
            'encrypted_value': encrypt_using_key(secret_value, encryption_key),
        },
    )


def encrypt_using_key(
        value: str,
        key: str) -> str:
    sealed_box = public.SealedBox(
        public.PublicKey(
            key.encode('utf-8'),
            encoding.Base64Encoder(),
        ),
    )
    encrypted = sealed_box.encrypt(value.encode('utf-8'))

    return base64.b64encode(encrypted).decode('utf-8')


class TemplateTest(CicdTemplatesTest):

    def tearDown(self) -> None:
        logging.info(f"Deleting test directory: {self.test_dir}")
        shutil.rmtree(self.test_dir)
        logging.info(f"Deleting repository: {self.gh_repo.full_name}")
        self.gh_repo.delete()

    def get_workflow(self, name: str) -> Workflow:
        workflow_iterator = self.gh_repo.get_workflows()
        for w in workflow_iterator:
            if w.name == name:
                return w

    def trace_workflow(self, name: str):
        finished = False
        _workflow = self.get_workflow(name)
        while not finished:
            single_run = list(_workflow.get_runs())[0]
            if single_run.status == "queued":
                logging.info("Run queued")
            elif single_run.status == "in_progress":
                logging.info(f"Waiting for run in {name} to finish")
                time.sleep(5)
            else:
                return single_run.status, single_run.conclusion

    def test_template_azure_github(self):
        access_token = os.environ["GH_ACCESS_TOKEN"]
        self.gh = Github(access_token)
        self.gh_user = self.gh.get_user()
        self.gh_repo = self.gh_user.create_repo(self.project_name)
        upload_secret(self.gh_repo.full_name, access_token, "DATABRICKS_HOST", os.environ["DBX_AZURE_HOST"])
        upload_secret(self.gh_repo.full_name, access_token, "DATABRICKS_TOKEN", os.environ["DBX_AZURE_TOKEN"])
        logging.info("Test directory: %s" % self.test_dir)

        with self.project_path:
            self.assertTrue(Path(".github").exists())
            self.assertFalse(Path("azure-pipelines.yml").exists())
            self.assertTrue(Path("conf/deployment.json").exists())

            validate_json("conf/deployment.json")

            self.execute_command(f"git config user.name cicd-templates-test")
            self.execute_command(f"git config user.email polarpersonal@gmail.com")
            self.execute_command("git add .")
            self.execute_command('git commit -m "init commit"')

            auth_url = f"cicd-templates-test:{os.environ['GH_PWD']}@github.com"
            fixed_url = self.gh_repo.clone_url.replace("github.com", auth_url)
            self.execute_command(f"git remote add origin {fixed_url}")
            self.execute_command("git branch -M main")
            self.execute_command("git push -u origin main")

            logging.info("Waiting for a test workflow launch")
            time.sleep(20)
            test_workflow_status, test_workflow_conclusion = self.trace_workflow("Test pipeline")

            self.assertTrue(test_workflow_status, "completed")
            self.assertTrue(test_workflow_conclusion, "success")

            self.execute_command("git tag -a v0.0.1 -m 'release'")
            self.execute_command("git push origin --tags")

            logging.info("Waiting for a release workflow launch")
            time.sleep(20)
            logging.info("Tracing workflow status for release pipeline")
            release_workflow_status, release_workflow_conclusion = self.trace_workflow("Release pipeline")
            self.assertTrue(release_workflow_status, "completed")
            self.assertTrue(release_workflow_conclusion, "success")


if __name__ == '__main__':
    unittest.main()
