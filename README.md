# prm-spine-exporter

This repo contains the spine exporter. It is responsible for retrieving data from Splunk that will be consumed as part of the data pipeline for the GP2GP Data Platform. It will put the retrieved data (Spine messaging logs related to GP2GP) into an S3 bucket.

## Running

The spine exporter can be installed via `python setup.py install`, or packaged into a docker container via `docker build`.
Alternatively, you can download one of the docker containers already published to ECR.

The main code entrypoint is via `python -m prmexporter.main`.


## Developing

Common development workflows are defined in the `tasks` script.

This project is written in Python 3.9.

### Recommended developer environment

- [pyenv](https://github.com/pyenv/pyenv) to easily switch Python versions.
- [Pipenv](https://pypi.org/project/pipenv/) to manage dependencies and virtual environments.
- [dojo](https://github.com/kudulab/dojo) and [Docker](https://www.docker.com/get-started)
  to run test suites in the same environment used by the CI/CD server.

#### Installing pyenv
```
brew install pyenv
```

#### Configure your shell's environment for Pyenv

```
For zsh:
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

#### Install new python and set as default

```
pyenv install 3.9.6
pyenv global 3.9.6
```

#### Installing pipenv and updating pip

In a new shell, run the following:
```
python -m pip install pipenv
python -m pip install -U "pip>=21.1”
```

#### Build a dev env

In a new shell, in the project directory run.

```
./tasks devenv
```

This will create a python virtual environment containing all required dependencies.
To find out the path of this new virtual environment (which can be useful for configuring IDEs) run:
```
pipenv --venv
```

### Running the unit tests

`./tasks test`

### Running tests, linting, and type checking

`./tasks validate`

### Running tests, linting, and type checking in a docker container

This will run the validation commands in the same container used by the GoCD pipeline.

`./tasks dojo-validate`

### Auto Formatting

This will format the code and the imports.

`./tasks format`

### Dependency Scanning

`./tasks check-deps`

- If this fails when running outside of Dojo, see [troubleshooting section](### Troubleshooting)

### Configuration

Configuration is achieved via the following environment variables:

| Environment variable        | Description                                                           | 
|-----------------------------|-----------------------------------------------------------------------|
| SPLUNK_URL                  | URL of the Splunk API                                                 |
| SPLUNK_API_TOKEN_PARAM_NAME | AWS Parameter store name which contains the Splunk API token          |
| OUTPUT_SPINE_DATA_BUCKET    | Output S3 Bucket to write the Spine logs                              |
| BUILD_TAG                   | Unique identifier for version of code build tag (e.g. short git hash) |
| SEARCH_NUMBER_OF_DAYS       | Number of days of search results from Splunk API                      |


### Troubleshooting

#### Checking dependencies fails locally due to pip

If running `./tasks check-deps` fails due to an outdated version of pip, yet works when running it in dojo (i.e. `./tasks dojo-deps`), then the local python environment containing pipenv may need to be updated (using pyenv instead of brew - to better control the pip version).
Ensure you have pyenv installed (use `brew install pyenv`).
Perform the following steps:

1. Run `brew uninstall pipenv`
2. Run the steps listed under [Installing correct version of pip and python](#installing-correct-version-of-pip-and-python)
3. Now running `./tasks check-deps` should pass.

#### Python virtual environments

If you see the below notice when trying to activate the python virtual environment, run `deactivate` before trying again.

> Courtesy Notice: Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project. You can set PIPENV_IGNORE_VIRTUALENVS=1 to force pipenv to ignore that environment and create its own instead. You can set PIPENV_VERBOSITY=-1 to suppress this warning.
