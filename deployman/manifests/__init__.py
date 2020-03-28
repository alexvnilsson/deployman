import os
import os.path
import yaml

import terminal
from manifests import io
from manifests.deploymanifest import DeployManifest, DeployManifestArtifact, DeployManifestProcess
from manifests.errors import ReadManifestError

DEFAULT_MANIFEST_FILENAME = "deploy.yml"

def make_manifest_path(root_dir: str=None, filename: str=None, terminal_mode:bool=False):
    if root_dir == None:
        root_dir = os.getcwd()

    if filename is None:
        filename = DEFAULT_MANIFEST_FILENAME

    manifest_path = os.path.realpath(os.path.join(root_dir, filename))

    return manifest_path


def read(filename: str=None, terminal_mode:bool=False):
    if filename is None:
        manifest_path = make_manifest_path(terminal_mode=terminal_mode)
    else:
        manifest_path = os.path.realpath(filename)

    manifest_filename = os.path.basename(manifest_path)
    manifest_dirname = os.path.dirname(manifest_path)

    if os.path.exists(manifest_path) == False:
        if terminal_mode:
            terminal.err(term.ExitCodes.GeneralError, f"{manifest_filename} doesn't exist in directory {manifest_dirname}.")
        else:
            raise ReadManifestError(f"Unable to read {manifest_filename}, file doesn't exist.")

    if os.path.isfile(manifest_path) == False:
        if terminal_mode:
            terminal.err(term.ExitCodes.GeneralError, f"{manifest_path} is not a file.")
        else:
            raise ReadManifestError(f"{manifest_filename} is not a file.")

    with io.read_file(manifest_path) as md:
        manifest_data = md

    return manifest_data


    