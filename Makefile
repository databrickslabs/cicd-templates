VERSION = 1.0.10

release:
	git add .
	git tag -a v$(VERSION) -m "Release tag for version $(VERSION)"
	git push origin --tags