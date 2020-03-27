# Deployment manager

## Developing

### Prerequisites

* Python 3 (verified working: v3.7.3)
* pip3
* python3-dev
* virtualenv

#### Installing requirements (Debian/Ubuntu)

`bin/verify-requirements`

The script above verifies/downloads and installs:

* python3-dev
* pip for Python 3
* virtualenv

### Set-up virtualenv

Set-up and activate virtualenv and install requirements (`requirements.txt`).

`bin/setup-virtualenv`

Before running this script, ensure all requirements are installed on the system.

**Notice:** the virtualenv is only activated for the script, run `source .env/bin/activate` if you need to use the virtualenv.

### Build and/or install

Build only: `bin/build`

Build and install: `bin/install`

## Usage

### Deploy manifest

Place `deploy.yml` in the home directory of your deploy agent.

**deploy.yml**:

```yml
name: deploy-manifest-name
artifact:
  name: [artifact-name]
  source: [source-file]
  target: [target-directory]
process:
  user: [uid]
  group: [gid]
```

### Command-line usage

#### Prepare artifacts

The `unpack-artifact` command pulls artifact info. from the deploy manifest (`deploy.yml`).

`[sudo] deploy unpack-artifact`

#### Fix web root permissions

`[sudo] deploy fix-perms`