Automatic documentation
===

The documentation in this repo was setup using this guide:
https://redandgreen.co.uk/sphinx-to-github-pages-via-github-actions/


Key commands
===

Setup from scratch: 

`cd /docs`
`sphinx-quickstart`

Generate .rst's automatically (from root directory)
`sphinx-apidoc -o docs .`

Manually generate html (already done in Github Action):
`cd docs && make html`

Clean html

`cd docs && make clean`