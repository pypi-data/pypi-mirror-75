import os
import subprocess
from uuid import uuid4
from abc import ABC
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import StrictUndefined
from jinja2.exceptions import UndefinedError
from argparse import ArgumentParser
from rkd.contract import ExecutionContext
from rkd.yaml_parser import YamlFileLoader
from rkd.exception import MissingInputException
from rkd.inputoutput import Wizard
from ..base import HarborBaseTask
from ...exception import MissingDeploymentConfigurationError

HARBOR_ROOT = os.path.dirname(os.path.realpath(__file__)) + '/../../deployment/files'


class BaseDeploymentTask(HarborBaseTask, ABC):
    ansible_dir: str = '.rkd/deployment'
    _config: dict
    vault_args: list = []

    def get_config(self) -> dict:
        """Loads and parses deployment.yml file. Supports Ansible Vault encryption"""

        deployment_filenames = ['deployment.yml', 'deployment.yaml']

        try:
            self._config
        except AttributeError:

            # try multiple files
            for filename in deployment_filenames:
                if os.path.isfile(filename):

                    #
                    # Check file contents before
                    #
                    with open(filename, 'rb') as f:
                        content = f.read().decode('utf-8')
                        #
                        # When file is encrypted, then decrypt it
                        #
                        if content.startswith('$ANSIBLE_VAULT;'):
                            tmp_vault_filename = '.tmp-' + str(uuid4())
                            tmp_vault_path = './.rkd/' + tmp_vault_filename

                            self.io().info('Decrypting deployment file')
                            self.sh('cp %s %s' % (filename, tmp_vault_path))

                            try:
                                self.rkd([':harbor:vault:encrypt', '-d', tmp_vault_path] + self.vault_args)
                                self._config = YamlFileLoader(self._ctx.directories).load_from_file(
                                    tmp_vault_filename,
                                    'org.riotkit.harbor/deployment/v1'
                                )
                            finally:
                                self.sh('rm -f %s' % tmp_vault_path)

                            return self._config

                    self._config = YamlFileLoader(self._ctx.directories).load_from_file(
                        filename,
                        'org.riotkit.harbor/deployment/v1'
                    )

                    return self._config

            raise MissingDeploymentConfigurationError()

        return self._config

    def _verify_synced_version(self, abs_ansible_dir: str):
        """Verifies last synchronization - displays warning if Harbor version was changed after last
        files synchronization"""

        if not os.path.isfile(abs_ansible_dir + '/.synced'):
            return

        with open(abs_ansible_dir + '/.synced', 'rb') as f:
            synced_version = f.read().decode('utf-8').strip()
            actual_version = self.get_harbor_version()

            if synced_version != actual_version:
                self.io().warn('Ansible deployment in .rkd/deployment is not up-to-date. We recommend to update' +
                               ' from %s to %s' % (synced_version, actual_version))

    def _write_synced_version(self, abs_ansible_dir: str):
        """Writes information about, in which Harbor version the files were synced last time"""

        with open(abs_ansible_dir + '/.synced', 'wb') as f:
            f.write(self.get_harbor_version().encode('utf-8'))

    def role_is_installed_and_configured(self) -> bool:
        return os.path.isfile(self.ansible_dir + '/.synced')

    def _ask_and_set_var(self, ctx: ExecutionContext, arg_name: str, title: str, attribute: str, secret: bool):
        """Ask user an interactive question, then add answer to the deployment.yml loaded in memory

        The variable will be appended to any node, where the variable is empty.
        Example: We have 5 servers, 3 without a password. So the password will be applied to 3 servers.
        """

        self.get_config()

        if not ctx.get_arg(arg_name):
            return

        for group_name, nodes in self._config['nodes'].items():
            node_num = 0

            for node in nodes:
                node_num += 1
                if attribute in self._config['nodes'][group_name][node_num - 1]:
                    continue

                wizard = Wizard(self).ask(title, attribute=attribute, secret=secret)
                self._config['nodes'][group_name][node_num - 1][attribute] = wizard.answers[attribute]

    def install_and_configure_role(self, ctx: ExecutionContext, force_update: bool = False) -> bool:
        """Install an Ansible role from galaxy, and configure playbook, inventory, all the needed things"""

        abs_ansible_dir = os.path.realpath(self.ansible_dir)
        should_update = force_update or not os.path.isfile(abs_ansible_dir + '/.synced')

        self.io().info('Checking role installation...')
        self._silent_mkdir(abs_ansible_dir)
        self._verify_synced_version(abs_ansible_dir)

        # optionally ask user and set facts such as passwords, key paths, sudo passwords
        # ansible-vault password prompt is handed by ansible-vault itself
        self._ask_and_set_var(ctx, '--ask-ssh-login', 'SSH username', 'user', secret=True)
        self._ask_and_set_var(ctx, '--ask-ssh-pass', 'SSH password', 'password', secret=True)
        self._ask_and_set_var(ctx, '--ask-ssh-key-path', 'SSH private key path', 'private_key', secret=False)
        self._ask_and_set_var(ctx, '--ask-sudo-pass', 'Sudo password for remote machines', 'sudo_pass', secret=True)

        if not self._synchronize_structure_from_template(abs_ansible_dir, only_jinja_templates=True):
            self.io().error_msg('Cannot synchronize templates')
            return False

        if should_update:
            self.io().info('Role will be updated')

            if not self._synchronize_structure_from_template(abs_ansible_dir):
                self.io().error_msg('Cannot synchronize structure')
                return False

            self.io().debug('Downloading fresh role...')
            self.download_roles()

            self._write_synced_version(abs_ansible_dir)

        return True

    def download_roles(self):
        self.sh(' '.join([
            'ansible-galaxy',
            'install', '-r', self.ansible_dir + '/requirements.yml',
            '-p', self.ansible_dir + '/roles/',
            '--force'
        ]), capture=False)

    def _synchronize_structure_from_template(self, abs_ansible_dir: str, only_jinja_templates: bool = False) -> bool:
        """Synchronizes template structure into .rkd/deployment"""

        self.io().debug(
            'Synchronizing structure from template (only_jinja_templates=' + str(only_jinja_templates) + ')')

        # synchronize directory structure
        for root, subdirs, files in os.walk(HARBOR_ROOT):
            relative_root = root[len(HARBOR_ROOT) + 1:]

            self._silent_mkdir(abs_ansible_dir + '/' + relative_root)

            for file in files:
                if only_jinja_templates and not file.endswith('.j2'):
                    continue

                abs_src_file_path = root + '/' + file
                abs_dest_file_path = abs_ansible_dir + '/' + relative_root + '/' + file

                if not self._copy_file(abs_src_file_path, abs_dest_file_path):
                    self.io().error('Cannot process file %s' % abs_dest_file_path)
                    return False

        return True

    def _copy_file(self, abs_src_file_path: str, abs_dest_file_path: str):
        """Copies a file from template directory - supports jinja2 files rendering on-the-fly"""

        if abs_dest_file_path.endswith('.j2'):
            abs_dest_file_path = abs_dest_file_path[:-3]

            with open(abs_src_file_path, 'rb') as f:
                tpl = Environment(loader=FileSystemLoader(['./', './rkd/deployment']), undefined=StrictUndefined)\
                        .from_string(f.read().decode('utf-8'))

            try:
                variables = self._prepare_variables()

                with open(abs_dest_file_path, 'wb') as f:
                    f.write(tpl.render(**variables).encode('utf-8'))

            except UndefinedError as e:
                self.io().error(str(e) + " - required in " + abs_src_file_path + ", please define it in deployment.yml")
                return False

            return True

        subprocess.check_call(['cp', '-p', abs_src_file_path, abs_dest_file_path])
        self.io().debug('Created ' + abs_dest_file_path)
        return True

    def _prepare_variables(self):
        """Glues together variables from environment and from deployment.yaml for exposing in JINJA2 templates"""

        variables = {}
        variables.update(os.environ)
        variables.update(self.get_config())

        if 'git_url' not in variables:
            variables['git_url'] = subprocess\
                .check_output(['git', 'config', '--get', 'remote.origin.url']).decode('utf-8')\
                .replace('\n', '')\
                .strip()

        if 'git_secret_url' not in variables:
            variables['git_secret_url'] = variables['git_url'].replace('\n', '')

        return variables

    def _preserve_vault_parameters_for_usage_in_inner_tasks(self, ctx: ExecutionContext):
        """Preserve original parameters related to Vault, so those parameters can be propagated to inner tasks"""

        try:
            vault_passwords = ctx.get_arg_or_env('--vault-passwords')
        except MissingInputException:
            vault_passwords = ''

        # keep the vault arguments for decryption of deployment.yml
        self.vault_args = ['--vault-passwords=' + vault_passwords]
        if ctx.get_arg('--ask-vault-pass'):
            self.vault_args.append('--ask-vault-pass')

    def _get_vault_opts(self, ctx: ExecutionContext, chdir: str = '') -> str:
        """Creates options to pass in Ansible Vault commandline"""

        try:
            vault_passwords = ctx.get_arg_or_env('--vault-passwords').split('||')
        except MissingInputException:
            vault_passwords = []

        num = 0
        opts = ''
        enforce_ask_pass = ctx.get_arg('--ask-vault-pass')

        for passwd in vault_passwords:
            num = num + 1

            if not passwd:
                continue

            if passwd.startswith('./') or passwd.startswith('/'):
                if os.path.isfile(passwd):
                    opts += ' --vault-password-file="%s" ' % (chdir + passwd)
                else:
                    self.io().error('Vault password file "%s" does not exist, calling --ask-vault-pass' % passwd)
                    enforce_ask_pass = True
            else:
                tmp_vault_file = './.rkd/.tmp-vault-' + str(uuid4())

                with open(tmp_vault_file, 'w') as f:
                    f.write(passwd)

                opts += ' --vault-password-file="%s" ' % (chdir + tmp_vault_file)

        if enforce_ask_pass:
            opts += ' --ask-vault-pass '

        return opts

    def _clear_old_vault_temporary_files(self):
        self.sh('rm -f ./.rkd/.tmp-vault*', capture=True)

    @classmethod
    def _add_vault_arguments_to_argparse(cls, parser: ArgumentParser):
        parser.add_argument('--ask-vault-pass', '-v', help='Ask for vault password interactively', action='store_true')
        parser.add_argument('--vault-passwords', '-V', help='Vault passwords separated by "||" eg. 123||456')

