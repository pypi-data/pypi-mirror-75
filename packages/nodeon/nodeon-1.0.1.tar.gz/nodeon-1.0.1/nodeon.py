# coding=utf-8

from __future__ import print_function

import json
import os
import os.path as osp
import platform
import sys
import tarfile
from hashlib import sha256

import requests
from plumbum import cli, colors

CLI_NAME = "nodeon"
CLI_VERSION = "1.0.0"

NODEON_DIR = osp.expanduser('~/.nodeon')
DOWNLOAD_DIR = osp.join(NODEON_DIR, '.nodes')
TMP_DIR = osp.join(NODEON_DIR, '.tmp')

MIRROR_TAOBAO = {'name': 'TaoBao', 'url': 'https://npm.taobao.org/mirrors/node'}
MIRROR_OFFICIAL = {'name': 'Node.js', 'url': 'https://nodejs.org/dist'}
MIRROR_CUSTOM = {'name': 'Custom', 'url': ''}
DEFAULT_MIRROR = MIRROR_TAOBAO


def mkdirp(*directory_names):
    for directory_name in directory_names:
        if not osp.exists(directory_name):
            os.makedirs(directory_name)


mkdirp(DOWNLOAD_DIR, TMP_DIR)


def extract_tar_file(tar_path, target_path):
    with tarfile.open(tar_path) as tar:
        for file_name in tar.getnames():
            tar.extract(file_name, target_path)


class NodeOn(cli.Application):
    PROGNAME = CLI_NAME | colors.green
    VERSION = CLI_VERSION | colors.green
    DESCRIPTION = "A program to create Node.js virtual environments."

    list_node_versions = cli.Flag(['list'], default=False, help='Display all Node.js versions.')
    only_lts = cli.Flag(['lts'], default=False, help='Display or use only LTS versions.')
    verbose = cli.Flag(['verbose'], default=False, help='Display verbose messages.')

    USAGE = """
    nodeon [project-name] [--node] [--mirror] [--list] [--lts]

    Example usages:

        # create virtual node with the latest stable version of Node.js
        nodeon my-project

        # create virtual node with the latest LTS version of Node.js
        nodeon my-project --lts

        # create virtual node with Node.js v14.0.0
        nodeon my-project --node=14.0.0

        # create virtual node with custom mirror
        nodeon my-project --mirror=https://nodejs.org/dist

        # show Node.js LTS versions
        nodeon --list --lts
    """

    _node_mirror = DEFAULT_MIRROR
    _node_version = ''
    _node_metadatas = []

    env_name = ''
    env_config = {}

    @property
    def node_version(self):
        if not self._node_version:
            if self.env_config:
                self._node_version = self.env_config['version']
            else:
                self._node_version = self.node_metadatas[0]['version']

        return self._node_version

    @property
    def node_mirror_base_url(self):
        return self._node_mirror['url']

    @property
    def node_metadatas(self):
        if self._node_metadatas:
            return self._node_metadatas

        metas = []
        url = self.node_mirror_base_url + '/index.json'

        if self.verbose:
            print('Fetching Node.js versions from mirror %s' % url)

        for meta in requests.get(url).json():
            version = meta['version'].encode().lstrip('v')
            # only use version greater than v4.0.0
            if int(version.split('.')[0]) >= 4:
                if self.only_lts:
                    if not meta['lts']:
                        continue

                meta['version'] = version
                metas.append(meta)

        self._node_metadatas = metas
        return self._node_metadatas

    def main(self, *args):

        if self.nested_command:
            return

        if self.list_node_versions:
            self.display_node_versions()
            return

        if len(args) != 1:
            self.help()
            return

        self.env_name = args[0]
        env_config_path = osp.join(NODEON_DIR, self.env_name + '.nodeon.json')

        if osp.exists(env_config_path):
            self.env_config = json.load(open(env_config_path))
        else:
            self.download_node_binary()
            self.extract_node_zip_file()
            self.env_config['version'] = self.node_version
            json.dump(self.env_config, open(env_config_path, 'w'), indent=4)

        self.active_environment()

    @cli.autoswitch(str)
    def node(self, version):
        """The Node.js version used to create virtual environment.
        Default is the latest stable version."""

        self._node_version = version

    @cli.autoswitch(str)
    def mirror(self, url=MIRROR_TAOBAO['name']):
        """Set mirror server to download Node.js binary file.
        Default is TaoBao in China(https://npm.taobao.org/mirrors/node)."""

        MIRROR_CUSTOM['url'] = url.rstrip('/')
        self._node_mirror = MIRROR_CUSTOM

    def active_environment(self):

        new_shell_envs = {
            'LIBRARY_PATH': osp.join(self.node_dir_path, 'lib') + ':$LIBRARY_PATH:',
            'LD_LIBRARY_PATH': osp.join(self.node_dir_path, 'lib') + ':$LD_LIBRARY_PATH:',
            'CPLUS_INCLUDE_PATH': osp.join(self.node_dir_path, 'include') + ':$CPLUS_INCLUDE_PATH:',
            'C_INCLUDE_PATH': osp.join(self.node_dir_path, 'include') + ':$C_INCLUDE_PATH:',
            'PATH': osp.join(self.node_dir_path, 'bin') + ':$PATH:', 'NODEON_ACTIVE_ENV_NAME': self.env_name,
        }

        new_envs = []
        for env_name, env_value in new_shell_envs.items():
            original_value = os.environ.get(env_name, '')
            if env_value not in original_value:
                new_envs.append("export {}={}".format(env_name, env_value))

        envs_shell_script_string = '\n'.join(new_envs)
        envs_shell_script_path = osp.join(TMP_DIR, 'envs.sh')
        open(envs_shell_script_path, 'w').write(envs_shell_script_string)

    @property
    def node_zip_filepath(self):
        return osp.join(DOWNLOAD_DIR, self.node_zip_filename)

    @property
    def node_dir_path(self):
        return self.node_zip_filepath.rstrip('.tar.gz')

    @property
    def node_zip_filename(self):
        system_info = self.get_system_info()
        filename = 'node-v{version}-{system}-{arch}.tar.gz'.format(
            version=self.node_version,
            **system_info
        )
        return filename

    def download_node_binary(self):
        checksum = self.get_node_checksum(self.node_version, self.node_zip_filename)

        # cache exists
        if osp.isfile(self.node_zip_filepath):
            node_binary_data = open(self.node_zip_filepath, 'rb').read()
            cache_file_checksum = sha256(node_binary_data).hexdigest()
            # exists
            if cache_file_checksum == checksum:
                return self.node_zip_filepath

        node_binary_url = '{host}/v{version}/{filename}'.format(
            host=self.node_mirror_base_url,
            version=self.node_version,
            filename=self.node_zip_filename,
        )
        if self.verbose:
            print('Downloading Node.js binary from %s to %s' % (node_binary_url, self.node_zip_filepath))
        else:
            print('Downloading Node.js %s...' % self.node_version)

        # download binary file
        req = requests.get(node_binary_url)
        if req.status_code != 200:
            sys.exit('Downloading failed(%s): %s.' % (req.status_code, req.content) | colors.red)
        print('Download successfully.')

        node_binary_data = req.content

        # validate checksum
        download_node_binary_checksum = sha256(node_binary_data).hexdigest()
        if download_node_binary_checksum != checksum:
            sys.exit('Checksum mismatch.' | colors.red)

        open(self.node_zip_filepath, 'wb').write(node_binary_data)

    def extract_node_zip_file(self):
        extract_target_dir_path = osp.split(self.node_zip_filepath)[0]
        # check if extracted
        extracted_check_file = osp.join(self.node_dir_path, 'nodeon_extracted.txt')
        if not osp.exists(extracted_check_file):
            print('Extracting...')
            extract_tar_file(self.node_zip_filepath, extract_target_dir_path)
            open(extracted_check_file, 'w').write('extracted')
            print('Extract successfully.')

    def get_node_checksum(self, node_version, filename):
        checksum_url = '{host}/v{version}/SHASUMS256.txt'.format(
            host=self.node_mirror_base_url,
            version=node_version,
        )
        for line in requests.get(checksum_url).content.splitlines():
            (checksum, _filename) = [i.strip() for i in line.strip().split(' ') if i.strip()]
            if _filename == filename:
                return checksum

    def get_system_info(self):
        system = platform.system().lower()
        if system not in ['linux', 'darwin']:
            sys.exit('Nodeon only support Linux/macOS right now.' | colors.red)

        arch = platform.machine().lower()
        if '64' in arch:
            arch = 'x64'
        elif '86' in arch:
            arch = 'x86'
        else:
            sys.exit('Nodeon only support x86/x64 right now.' | colors.red)

        return {'system': system, 'arch': arch}

    def display_node_versions(self):
        get_major_version = lambda _version: _version.split('.')[0]

        versions = (meta['version'] for meta in self.node_metadatas)

        # group version with major version
        last_major_version = ''
        results = []
        for version in versions:
            major_version = get_major_version(version)
            if major_version != last_major_version:
                results.append([])
                last_major_version = major_version
            results[-1].append(version + '\t')

        for index, versions in enumerate(results):
            results[index] = ''.join(versions)

        print('\n'.join(results))


if __name__ == "__main__":
    NodeOn.run()
