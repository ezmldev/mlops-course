# mlops-course

## Setting up the Python dev environment
* `pip install -r dev-requirements.txt`
* VSCode extensions: black, flake8, mypy, isort


## Setting env var for GH action

First create a [classic token](https://github.com/settings/tokens/new)
- with the sinle `repo/public_repo` scope

```
echo $CODESPACE_NAME | GITHUB_TOKEN=ghp_xxxxxxxxxxxx gh variable set CODESPACE_NAME
```