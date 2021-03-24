VERSION = 1.0.8

release:
	git add .
	git tag -a v$(VERSION) -m "Release tag for version $(VERSION)"
	git push origin --tags