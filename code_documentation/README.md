To generate the .rst files run these commands:

```sh
cd code_documentation/docs
poetry run sphinx-apidoc -o source ../../customer_microservice
```

To build the HTML pages for the documentation run these commands:

```sh
cd code_documentation/docs
poetry run make html
```


To rebuild the HTML pages for the documenation run these commands:

```sh
cd code_documentation/docs
poetry run make clean
```

