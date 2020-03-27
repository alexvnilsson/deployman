#!/usr/bin/env python3

import getpass
import click
import shutil
import zipfile
from zipfile import ZipFile
import os
import os.path
from pathlib import Path
from glob import glob
import manifests
from terminal import Terminal, ExitCodes

#
# Variables
#

# user variables
home_dir = str(Path.home())
uploads_dir = os.path.join(home_dir, "uploads")

# site variables

site_dirname = "www"

@click.group()
def cli():
    pass

@cli.command('unpack-artifact')
@click.option('-m', '--manifest', default=None, help="Manifest file (YAML) to use.")
def artifact_unpack(manifest: str=None):
    if manifest != None:
        manifest_data = manifests.read(manifest)
    else:
        manifest_data = manifests.read()

    term = Terminal()

    manifest_path = manifest_data.path
    term.cmd_head("unpack-artifact", f"Manifest: {manifest_path}")

    artifact_path = os.path.realpath(manifest_data.artifact.source)
    output_dir = os.path.realpath(manifest_data.artifact.target)
    root_dir = os.path.dirname(output_dir)
    output_basename = os.path.basename(output_dir)
    copy_output_basename = f"{output_basename}_old"
    copy_output_dir = os.path.realpath(os.path.join(root_dir, copy_output_basename))

    if not os.path.exists(artifact_path):
        term.exit(ExitCodes.GeneralError, f"{artifact_path} does not exist.")

    if not zipfile.is_zipfile(artifact_path):
        term.exit(ExitCodes.GeneralError, f"{artifact_path} is not a ZIP-archive.")

    if os.path.exists(output_dir):
        term.task("Move old artifacts", f"mv {output_dir} {copy_output_dir}")
        shutil.move(output_dir, os.path.join(root_dir, copy_output_dir))
        term.ok()
        term.task("Make new output directory for artifacts", f"mkdir {output_basename}")
        os.mkdir(os.path.join(root_dir, output_basename))
        term.ok()

    with ZipFile(artifact_path) as artifact_zip:
        term.task("Unpack artifact archive", f"zip extractall {input}")
        artifact_zip.extractall(output_dir)
        term.ok()

    if os.path.exists(copy_output_dir):
        term.task("Remove old artifacts", f"rmtree {copy_output_basename}")
        shutil.rmtree(copy_output_dir)
        term.ok()

@cli.command('fix-perms')
@click.option('-m', '--manifest', default=None, help="Manifest file (YAML) to use.")
def fix_perms(manifest: str=None):
    if manifest != None:
        manifest_data = manifests.read(manifest)
    else:
        manifest_data = manifests.read()

    term = Terminal()

    output_dir = os.path.realpath(manifest_data.artifact.target)
    root_dir = os.path.dirname(output_dir)

    manifest_path = manifest_data.path
    term.cmd_head("unpack-artifact", f"Manifest: {manifest_path}")

    term.task("Verify artifact target exists", output_dir)

    if not os.path.exists(output_dir):
        term.fail()
    else:
        term.ok()

    p_user = manifest_data.process.user
    p_group = manifest_data.process.group
    output_dir_mod = 0o755

    term.task(f"Update directory permissions for web root")

    try:
        os.chown(output_dir, p_user, p_group)
        os.chmod(output_dir, output_dir_mod)

        term.ok()
    except Exception as e:
        term.fail()
        print(e)
        term.exit()

    d_glob = f"{output_dir}/**"
    d_path_mod = 0o755

    term.task("Update directory permissions", d_glob)

    try:
        for d in glob(d_glob):
            d_path = os.path.realpath(os.path.join(output_dir, d))
            os.chmod(d_path, d_path_mod)

        term.ok()
    except Exception as e:
        term.fail(None)
        print(e)
        term.exit()

    f_glob = f"{output_dir}/**/*"
    f_path_mod = 0o644

    term.task("Update file permissions", f_glob)   

    try:
        for f in glob(f_glob):
            f_path = os.path.realpath(os.path.join(output_dir, f))
            os.chown(f_path, p_user, p_group)
            os.chmod(f_path, f_path_mod)

        term.ok()
    except Exception as e:
        term.fail(None)
        print(e)
        term.exit()

    

if __name__ == '__main__':
    cli()