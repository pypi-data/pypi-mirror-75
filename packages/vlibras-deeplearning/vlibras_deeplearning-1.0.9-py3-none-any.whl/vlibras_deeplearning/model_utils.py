import logging
import os
import pathlib
import shutil
import subprocess

from tqdm import tqdm

logger = logging.getLogger(__name__)
PWD = os.path.realpath(os.path.dirname(__file__))

def _read_version_from_file(filepath):
    '''Return the version number found in the file identified by `filepath`.'''
    with open(filepath, 'r') as vf:
        return vf.readline().replace('v', '').strip()

vlibras_deeplearning_version = _read_version_from_file(os.path.join(PWD, 'VERSION'))
downloaded_model_version = None

def _check_if_versions_match():
    '''Return whether the downloaded version matches the package's version
    number.
    '''
    try:
        downloaded_model_version = _read_version_from_file(os.path.join(PWD, 'model', 'VERSION'))
        if downloaded_model_version != vlibras_deeplearning_version:
            # Mismatch between model and package version.
            logger.debug(f'Version mismatch: model={downloaded_model_version}, vdl={vlibras_deeplearning_version}')
            return False
    except:
        # Couldn't read version, assume files don't exist.
        logger.debug(f'Failed to read version.')
        return False

    return True


def _is_model_present(model_folder_path):
    '''Return `True` if all necessary model files for the current version are
    present.
    '''
    existing_files = list(pathlib.Path(model_folder_path).rglob('*'))
    desired_files = [
        os.path.join(model_folder_path, 'BIN', 'dict.gi.txt'),
        os.path.join(model_folder_path, 'BIN', 'dict.gr.txt'),
        os.path.join(model_folder_path, 'Checkpoints', 'checkpoint_best.pt'),
        os.path.join(model_folder_path, 'BPE', 'bpe_code'),
    ]
    desired_files = [pathlib.Path(desired_file) for desired_file in desired_files]

    return all([desired_file in existing_files for desired_file in desired_files])


def _execute_cmd(cmd):
    '''Utility helper function for calling Unix commands.'''
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ''):
        yield stdout_line

    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def _clone_repo(model_folder):
    '''Clone the correct version of the model into the `model_folder` directory
    using git LFS.
    '''
    logger.info(f'Downloading model, version {vlibras_deeplearning_version}...')
    cmd = [
        'git', 'clone', '--single-branch', '--depth', '1', '--branch',
        f'v{vlibras_deeplearning_version}',
        'https://gitlab.lavid.ufpb.br/vlibras-deeplearning/models.git',
        model_folder
    ]
    for line in _execute_cmd(cmd):
        print(line, end='')


def prepare_model():
    '''Make sure we have a working model inside the `model` directory for
    fairseq to use.
    '''
    model_folder = os.path.join(PWD, 'model')

    if not _check_if_versions_match() or not _is_model_present(model_folder):
        # Delete existing model folder (wrong version)
        if os.path.isdir(model_folder):
            shutil.rmtree(model_folder)

        # Download desired version
        _clone_repo(model_folder)
