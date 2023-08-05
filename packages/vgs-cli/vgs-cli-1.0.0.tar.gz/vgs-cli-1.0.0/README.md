# VGS CLI
[![CircleCI](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master.svg?style=svg&circle-token=dff66120c964e4fbf51dcf059b03746910d0449d)](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master)

Command Line Tool for programmatic configurations on VGS.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [PyPI](#pypi)
- [Run](#run)
- [Running in Docker](#running-in-docker)
- [Commands](#commands)
  - [Help](#help)
  - [Authentication](#authentication)
    - [Login](#login)
    - [Auto Login](#auto-login)  
    - [Logout](#logout)
  - [Routes](#routes)
    - [Get](#get)
    - [Apply](#apply)
- [Troubleshooting](#troubleshooting)
  - [Debug Mode](#debug-mode)
  - [Known Issues](#known-issues)
  - [Support](#support)
    
## Requirements
[Python 3](https://www.python.org/downloads/) or [Docker](https://docs.docker.com/get-docker/).

## Installation

### PyPI
Install the latest version from [PyPI](https://pypi.org/project/vgs-cli/):
```
pip install vgs-cli
```

## Run

Verify your installation by running:
```
vgs --version
```

## Running in Docker

In order to run in Docker we recommend to declare the following `docker-compose.yaml`:
```yaml
version: '3'
services:

  cli:
    image: quay.io/verygoodsecurity/vgs-cli:${VERSION:-latest}
    env_file:
      - .env
    ports:
      - "7745:7745"
      - "8390:8390"
      - "9056:9056"
    volumes:
      - ./.tmp:/tmp
```

To login from browser you need to pass `--service-ports` option:
```
docker-compose run --service-ports cli vgs login
```

To use auto login option you need to declare the following `.env` file:
```
VGS_CLIENT_ID=<YOUR-CLIENT-ID>
VGS_CLIENT_SECRET=<YOUR-CLIENT-SECRET>
VGS_USERNAME=<YOUR-VGS-USERNAME>
VGS_PASSWORD=<YOUR-VGS-PASSWORD>
``` 

Run the latest version with:
```
docker-compose run cli vgs --version
```

Run a specific version:
```
VERSION=[VERSION] docker-compose run cli vgs --version
```

## Commands

### Help

You can explore the CLI using the help command. Help option can be used on any command:

```
vgs --help
```

```
vgs [COMMAND] --help
```

### Authentication

#### Login

Log in via browser:

```
vgs login
```

You may be asked to allow storing data in your OS password management system (Mac OS Keychain, Linux Secret Service, Windows Credential Vault).

#### Auto Login

> If you'd like to use this option, please contact support@verygoodsecurity.com to get client credentials.

CLI supports [auto login](#auto-login) via environment variables:

- `VGS_CLIENT_ID` - Client ID 
- `VGS_CLIENT_SECRET` - Client secret
- `VGS_USERNAME` - VGS account username
- `VGS_PASSWORD` - VGS account password

With these environment variables set VGS CLI can be used without `vgs login` command.

We recommend to create a separate technical user and use it for `VGS_USERNAME` and `VGS_PASSWORD` values. 
Please note that auto login via environment variables for accounts with enabled OTP is not supported.


#### Logout

Sessions automatically expire after 30 minutes of inactivity. You can also logout manually:

```
vgs logout
```

### Routes

#### Get

Get details of your routes in YAML format:

```
vgs get routes --vault <VAULT_ID>
```

To write route details to file:
```
vgs get routes --vault <VAULT_ID> > routes.yaml
``` 

#### Apply

Create or update the route:
```
vgs apply routes --vault <VAULT_ID> -f routes.yaml
```

## Troubleshooting

### Debug Mode

If you're getting errors, you can turn on debug information with `-d`/`--debug` flag:
```
vgs -d get routes --vault <VAULT_ID>
```

### Known Issues

These are some known issues if you're using Python distribution:

- During login, you can receive the following error: `Authentication error occurred. Can't store password on keychain`. 
This is solved by signing your Python binary with the command `codesign -f -s - $(which python3)`.

- If you're receiving requirements conflicts, consider using [VirtualEnv](https://virtualenv.pypa.io/en/latest/).

- On Mac OS, you can see a prompt that will ask for Keychain access. Please make sure to allow `vgs-cli` to store passwords.

- After updates of Mac OS you can receive an error `keyring.backends._OS_X_API.Error: (-25293, "Can't fetch password from system")`. Make sure to update your Python version to latest and re-install VGS CLI if needed.

### Support

If you're experiencing any other issues please contact [support@verygoodsecurirty.com](mailto:support@verygoodsecurirty.com).