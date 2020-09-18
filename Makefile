
generate-test:
	rm -rf ~/tmp/cicd-templates/cicd_templates_test
	cookiecutter $(shell pwd) --no-input -f -o ~/tmp/cicd-templates project_name=cicd-templates-test cloud=AWS cicd_tool="GitHub Actions"
	cd ~/tmp/cicd-templates/cicd_templates_test && dbx configure --environment=test --profile=dbx-dev-aws
	cd ~/tmp/cicd-templates/cicd_templates_test && pytest tests/unit

get-latest-dbx:
	cd ~/IdeaProjects/cicd-templates-api && make artifact
	cp -r ~/IdeaProjects/cicd-templates-api/artifact/* {{cookiecutter.project_slug}}/tools
	rm {{cookiecutter.project_slug}}/tools/dbx.pdf