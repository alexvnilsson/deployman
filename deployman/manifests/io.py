from contextlib import contextmanager
import os.path
import yaml
from yaml import YAMLObject, SafeLoader, error
import terminal

from manifests.errors import ReadManifestError
from manifests.deploymanifest import DeployManifest, DeployManifestArtifact, DeployManifestProcess

OPEN_MODE = 'r'

@contextmanager
def read_file(file_path: str=None) -> DeployManifest:
    try:
        with open(file_path, OPEN_MODE) as filestream:
            data = yaml.load(filestream, Loader=yaml.SafeLoader)
            manifest = read_yaml(data)
            manifest.set_manifest_path(file_path)
            yield manifest
    except ReadManifestError as e:
        terminal.err(term.ExitCodes.GeneralError, f"Fail to read {file_path}: " + e)

def read_yaml(data: dict):
    try:
        if isinstance(data["artifact"], list):
            _artifact = data["artifact"][0]
        elif isinstance(data["artifact"], dict):
            _artifact = data["artifact"]

        deploy_manifest_artifact = DeployManifestArtifact(
            _artifact["name"],
            _artifact["source"],
            _artifact["target"])

        if isinstance(data["process"], list):
            _process = data["process"][0]
        elif isinstance(data["process"], dict):
            _process = data["process"]

        deploy_manifest_process = DeployManifestProcess(_process["user"], _process["group"])

        deploy_manifest = DeployManifest(data["name"], deploy_manifest_artifact, deploy_manifest_process)
    except error.MarkedYAMLError as e:
        terminal.err(term.ExitCodes.GeneralError, f"Couldn't parse deploy manifest: " + e)

    return deploy_manifest