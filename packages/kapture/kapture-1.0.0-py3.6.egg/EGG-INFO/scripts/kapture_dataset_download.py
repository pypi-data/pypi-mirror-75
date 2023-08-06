#!/home/jmorat/miniconda3/envs/kapture-tmp/bin/python
# Copyright 2020-present NAVER Corp. Under BSD 3-clause license

"""
script to easily  download kapture datasets.
"""

import argparse
import logging
import sys
import os
import os.path as path
import requests
import yaml
import fnmatch
from typing import Dict, Optional, List
from tqdm import tqdm
import tarfile
import hashlib
from shutil import rmtree
from datetime import datetime

logger = logging.getLogger('download')
logging.basicConfig(format='%(levelname)-8s::%(name)s: %(message)s')

INDEX_FILENAME = 'kapture_dataset_index.yaml'
DEFAULT_DATASET_PATH = path.normpath(path.abspath('.'))
DEFAULT_REPOSITORY_URL = 'https://github.com/naver/kapture/raw/master/dataset'

datasets = {}


def ask_confirmation(question):
    """
    ask "question" to the user.
    The "answer" return value is True for "yes" or False for "no".
    """
    validate = ['yes', 'y', 'ye']
    prompt = ' [y/N]\n'
    sys.stdout.write(question + prompt)
    user_choice = input().lower()
    return user_choice in validate


class Dataset:
    def __init__(self,
                 name: str,
                 url: str,
                 root_path: str,
                 sha256sum: str,
                 sub_path: Optional[str] = None
                 ):
        """
        :param name: name of the archive (dataset or part of a dataset)
        :param url: input remote url of the dataset archive (tar).
        :param root_path: input absolute path to root directory where all datasets are installed.
        :param sha256sum: sha256 sum of the archive file on remote server.
        :param sub_path: input optional sub path where to install the dataset under root_path/sub_path.
                         If not given, tar file is extracted directly to root_path
        """
        self._name = name
        # remore url of the archive
        self._archive_url = url
        # local absolute path to archive
        self._archive_filepath = path.join(root_path, name + '.tar')
        # if _success_filepath is present, it means it as already been installed. It contains some debug info
        self._success_filepath = path.join(root_path, name + '.txt')
        # local absolute path where to the install the dataset (multiple dataset might be installed at same path).
        self._install_local_path = path.join(root_path, sub_path) if sub_path is not None else root_path
        self._sha256sum_archive_remote = sha256sum

    def is_archive_valid(self):
        if not path.isfile(self._archive_filepath):
            return False
        # size is consistent, check sha256
        sha256_hash = hashlib.sha256()
        with open(self._archive_filepath, 'rb') as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        sha256sum_archive_local = sha256_hash.hexdigest()
        logger.debug(f'sha256sum {self._archive_filepath} :\n\t{sha256sum_archive_local}')
        if sha256sum_archive_local != self._sha256sum_archive_remote:
            return False

        return True

    def prob_status(self):
        """
        gives the actual dataset status
         - online: means not downloaded, and not installed (extracted).
         - installed: means has been downloaded and installed (extracted).
         - downloaded: means has been downloaded (tar) but not installed (extracted) yet.
         - incomplete: means partially downloaded
         - corrupted: means that the downloaded archive is curropted (inconsistent size or sh256).
        """
        if path.isfile(self._success_filepath):
            return 'installed'
        if not path.isfile(self._archive_filepath):
            return 'online'

        assert path.isfile(self._archive_filepath)
        # file exists, check it has proper size
        r = requests.head(self._archive_url)
        size_archive_online = int(r.headers.get('content-length', 0))
        size_archive_local = int(path.getsize(self._archive_filepath))
        if size_archive_local < size_archive_online:
            logger.debug(f'file_size_online={size_archive_online} != file_size_local={size_archive_local}')
            return 'incomplete'
        if size_archive_local > size_archive_online:
            logger.critical(f'inconsistent file size ({size_archive_online} vs {size_archive_local})')
            return 'corrupted'

        assert size_archive_local == size_archive_online
        # size is consistent, check sha256
        if not self.is_archive_valid():
            return 'corrupted'

        # archive is there, but not installed
        return 'downloaded'

    def __repr__(self):
        return f'{self._name:30} | {self.prob_status():10} | {self._archive_url}'

    def download_archive_resume(self, resume_byte_pos: Optional[int] = None):
        """
        resume (or start if no pos given) the dataset download.
        :param resume_byte_pos: input position in bytes where to resume the Download
        """
        r = requests.head(self._archive_url)
        file_size_online = int(r.headers.get('content-length', 0))
        # Append information to resume download at specific byte position to header
        resume_header = ({'Range': f'bytes={resume_byte_pos}-'}
                         if resume_byte_pos else None)
        # Establish connection
        r = requests.get(self._archive_url, stream=True, headers=resume_header)
        # Set configuration
        block_size = 1024
        initial_pos = resume_byte_pos if resume_byte_pos else 0
        mode = 'ab' if resume_byte_pos else 'wb'
        with open(self._archive_filepath, mode) as f:
            with tqdm(total=file_size_online, unit='B',
                      unit_scale=True, unit_divisor=block_size,
                      desc=self._archive_filepath, initial=initial_pos,
                      ascii=True, miniters=1,
                      disable=logger.getEffectiveLevel() >= logging.CRITICAL) as pbar:
                for chunk in r.iter_content(32 * block_size):
                    f.write(chunk)
                    pbar.update(len(chunk))

    def download_archive_file(self):
        """ Starts or resumes the download if already started. """
        logger.debug(f'downloading {self._archive_filepath}')
        r = requests.head(self._archive_url)
        if path.isfile(self._archive_filepath):
            logger.debug('file is already (partially) there.')
            # file already there (at least partially)
            file_size_online = int(r.headers.get('content-length', 0))
            file_size_local = int(path.getsize(self._archive_filepath))
            if file_size_online == file_size_local:
                logger.info(f'file {self._archive_filepath} already downloaded.')
            else:
                logger.info(f'resume download from {file_size_local / file_size_online * 100.:4.1f}%')
                self.download_archive_resume(file_size_local)
        else:
            logger.info(f'start downloading {self._archive_filepath}.')
            self.download_archive_resume()

    def install_archive(self):
        if not self.is_archive_valid():
            raise ValueError('Archive file not valid: cant install.')
        logger.debug(f'extracting\n\tfrom: {self._archive_filepath}\n\tto  : {self._install_local_path}')
        # make sure directory exists
        os.makedirs(self._install_local_path, exist_ok=True)
        with tarfile.open(self._archive_filepath, 'r:*') as archive:
            archive.extractall(self._install_local_path)
        # creating success file
        logger.debug(f'creating {self._success_filepath}')
        with open(self._success_filepath, 'wt') as f:
            f.write(f'installed on: {datetime.now()}\nfrom: {self._archive_url}')
        # cleaning tar
        logger.debug(f'cleaning {self._archive_filepath}')
        os.remove(self._archive_filepath)

    def do_download_and_install(self, force_overwrite: bool = False):
        # test the dataset presence
        current_status = self.prob_status()
        if current_status == 'installed' and not force_overwrite:
            logger.info(f'{self._install_local_path} already exists: skipped')
            return

        if current_status != 'downloaded':
            # check archive file integrity
            if current_status == 'corrupted':
                # if corrupted: remove the archive and start over
                os.remove(self._archive_filepath)
            self.download_archive_file()

        # install it
        logger.info(f'installing {path.basename(self._archive_filepath)} to {self._install_local_path}')
        self.install_archive()
        # done
        logger.info(f'done isntalling {self._name}')

    def clean(self):
        """
        Remove all files (installed, archive, ..)
        warning: this may clean also other intricate installation

        :return:
        """
        # clean archive if any
        if path.isfile(self._archive_filepath):
            logger.debug(f'deleting {self._archive_filepath}')
            os.remove(self._archive_filepath)
        # clean success files if any
        if path.isfile(self._success_filepath):
            logger.debug(f'deleting {self._success_filepath}')
            os.remove(self._success_filepath)
        # clean installation if any
        if path.isdir(self._install_local_path):
            # warning: this may clean also other intricate installation
            logger.debug(f'deleting {self._install_local_path}/')
            # TODO: check symlink attack: https://bugs.python.org/issue4489
            rmtree(self._install_local_path)


def load_index(
        index_filepath: str,
        root_path: str,
        filter_patterns: Optional[List[str]] = None
) -> Dict[str, Dataset]:
    """
    Parses and load data from the index files, under yaml format.
    the yaml file looks like :
    ----
    robotcar_seasons_02:
      sub_path: robotcar_seasons
      url: http://download.europe.naverlabs.com//kapture/robotcar_seasons_02.tar
      sha256sum: 542ef47c00d5e387cfb0dcadb2459ae2fb17d59010cc51bae0c49403b4fa6a18
    ----

    :param index_filepath: input absolute path to index file
    :param root_path: input absolute path to install directory
    :param filter_patterns: optional input list of unix-like patterns (e.g. SiLDa*) to filter datasets
    :return: dict name -> [url, sub_path, sha256sum]
    """
    if not path.isfile(index_filepath):
        raise FileNotFoundError('no index file: do an update.')
    with open(index_filepath, 'rt') as f:
        dataset_yaml = yaml.safe_load(f)
    if len(dataset_yaml) == 0:
        raise FileNotFoundError('invalid index file: do an update.')

    datasets = {
        name: Dataset(name=name, root_path=root_path, **data) for name, data in dataset_yaml.items()
        if filter_patterns is None or any(fnmatch.fnmatch(name, pattern) for pattern in filter_patterns)
    }
    return datasets


def kapture_dataset_download_cli():
    """
    Parse the kapture_dataset_download command line .
    """
    parser = argparse.ArgumentParser(description='download kapture datasets.')
    parser_verbosity = parser.add_mutually_exclusive_group()
    parser_verbosity.add_argument('-v', '--verbose', action='store_const',
                                  dest='verbose', const=logging.INFO,
                                  help='display info messages [True].')
    parser_verbosity.add_argument('-q', '--silent', '--quiet', action='store_const',
                                  dest='verbose', const=logging.CRITICAL,
                                  help='silence all messages.')
    parser_verbosity.add_argument('-d', '--debug', action='store_const',
                                  dest='verbose', const=logging.DEBUG,
                                  help='display info and debug messages.')
    parser.add_argument('--install_path', default=path.normpath(path.join(DEFAULT_DATASET_PATH)),
                        help=f'path to index files listing all datasets'
                             f' [{path.normpath(path.join(DEFAULT_DATASET_PATH))}]')
    subparsers = parser.add_subparsers(help='sub-command help')
    ####################################################################################################################
    # create the parser for the "update" command
    parser_update = subparsers.add_parser('update', help='update dataset index')
    parser_update.set_defaults(cmd='update')
    parser_update.add_argument('--repo', default=DEFAULT_REPOSITORY_URL,
                               help='url of the repository.')
    ####################################################################################################################
    parser_list = subparsers.add_parser('list', help='display dataset index')
    parser_list.set_defaults(cmd='list')
    parser_list.add_argument('dataset', nargs='*', default=['*'])
    ####################################################################################################################
    parser_install = subparsers.add_parser('install', help='install dataset')
    parser_install.set_defaults(cmd='install')
    parser_install.add_argument('-f', '--force', action='store_true', default=False,
                                help='Force installation even if dataset has already been installed.')
    parser_install.add_argument('dataset', nargs='*', default=['+'],
                                help='name of the dataset to download. Can use unix-like wildcard.')
    ####################################################################################################################
    parser_download = subparsers.add_parser('download', help='dowload dataset, without installing it')
    parser_download.set_defaults(cmd='download')
    parser_download.add_argument('dataset', nargs='*', default=['+'],
                                 help='name of the dataset to download. Can use unix-like wildcard.')
    ####################################################################################################################
    parser_clean = subparsers.add_parser('clean', help='clean all')
    parser_clean.set_defaults(cmd='clean')
    parser_clean.add_argument('-f', '--force', action='store_true', default=False,
                              help='Do not ask for user confirmation.')
    ####################################################################################################################
    args = parser.parse_args()

    logger.setLevel(args.verbose or logging.INFO)
    logger.debug(f'{sys.argv[0]} \\\n' + '  \\\n'.join(
        '--{:20} {:100}'.format(k, str(v))
        for k, v in vars(args).items()))

    try:
        index_filepath = path.join(args.install_path, INDEX_FILENAME)
        if not hasattr(args, 'cmd'):
            # check user did not forgot the command
            logger.critical(f'Choose command among [ {" | ".join(subparsers.choices)} ]')
            exit(-1)

        if args.cmd == 'update':
            logger.info(f'updating dataset list from {args.repo} ...')
            index_remote_url = path.join(args.repo, INDEX_FILENAME)
            logger.debug(f'retrieving index at {index_remote_url}')
            r = requests.get(index_remote_url, allow_redirects=True)
            if r.status_code != requests.codes.ok:
                raise ConnectionError(f'unable to grab {index_remote_url} (code:{r.status_code})')
            with open(index_filepath, 'wt') as f:
                f.write(r.text)
            logger.info('dataset index retrieved successfully.')

        elif args.cmd == 'list':
            logger.info(f'listing dataset {index_filepath} ...')
            dataset_index = load_index(index_filepath=index_filepath,
                                       root_path=args.install_path,
                                       filter_patterns=args.dataset)
            print('\n'.join(str(dataset) for dataset in dataset_index.values()))

        elif args.cmd == 'install':
            logger.info(f'installing dataset {args.dataset} ...')
            dataset_index = load_index(index_filepath=index_filepath,
                                       root_path=args.install_path,
                                       filter_patterns=args.dataset)
            if len(dataset_index) == 0:
                raise ValueError('no matching dataset')
            logger.info(f'{len(dataset_index)} dataset will be installed.')
            for name, dataset in dataset_index.items():
                logger.info(f'downloading {name} ...')
                dataset.do_download_and_install(force_overwrite=args.force)

        elif args.cmd == 'download':
            logger.info(f'downloading dataset {args.dataset} ...')
            dataset_index = load_index(index_filepath=index_filepath,
                                       root_path=args.install_path,
                                       filter_patterns=args.dataset)
            if len(dataset_index) == 0:
                raise ValueError('no matching dataset')
            logger.info(f'{len(dataset_index)} dataset will be downloaded.')
            for name, dataset in dataset_index.items():
                logger.info(f'downloading {name} ...')
                dataset.download_archive_file()

        elif args.cmd == 'clean':
            logger.info(f'cleaning all dataset ...')
            # since we'll remove everything, ask user confirmation
            dataset_index = load_index(index_filepath=index_filepath,
                                       root_path=args.install_path)
            # just for info, enumerate installed or partially installed = not online
            nb_dataset_isntalled_index = len([d for d in dataset_index.values()
                                              if d.prob_status() is not 'online'])
            logger.info(f'all ({nb_dataset_isntalled_index}) datasets will be erased .')
            if not args.force and not ask_confirmation(
                    f'Are you sure you want to delete ALL {len(dataset_index)} datasets '):
                logger.info('cleaning canceled by user')
            else:
                for name, dataset in dataset_index.items():
                    logger.info(f'cleaning {name} ...')
                    dataset.clean()

        else:
            raise ValueError(f'unknown command {args.cmd}')

    except Exception as e:
        logger.critical(e)


if __name__ == '__main__':
    kapture_dataset_download_cli()
