# Deployment manager

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

`deploy unpack-artifact [filename]`