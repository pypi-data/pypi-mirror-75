# -*- coding: utf-8 -*-
"""
    ospclientsdk.shell

    The client shell to interact
    with the openstackclient.

"""

__all__ = ["ClientShell"]

import yaml
import os
from .helpers import *
from .exceptions import OspShellError
from .constants import LOG_FORMAT, LOG_LEVELS, DEBUG_LOG_FORMAT
from logging import getLogger, Formatter, StreamHandler


class ClientShell(object):

    """
    ClientShell Class that provides the SDK API
    like wrapper around the openstackclient.

    """

    def __init__(self, cloud_dict=None, cloud_file=None, cloud=None, log_level='info'):

        self.logger = self._setup_logging(log_level=log_level)

        if cloud_dict:
            self.load_cloud_config(cloud_dict, cloud)
        if cloud_file:
            if os.path.isfile(cloud_file):
                with open(os.path.abspath(cloud_file)) as f:
                    cloud_configs = yaml.safe_load(f)
                self.load_cloud_config(cloud_configs, cloud)
        self.load_available_os_commands()
        self._setup_proxy_classes()

    def load_cloud_config(self, cloud_dict, cloud=None):
        """
        This function is to load the credentials dictionary into memory
        by exposing the values using the environmental variables.

        :param cloud_dict: dict
        :param cloud: str
        :return:
        """

        if cloud_dict.get('clouds', {}):
            creds = cloud_dict.get('clouds', {}).get('openstack') \
                if not cloud else cloud_dict.get('clouds', {}).get(cloud, {})

            if creds and 'auth' in creds and creds.get('auth', {}):
                for key, value in creds.get('auth', {}).items():
                    os.environ['OS_' + key.upper()] = value
                os.environ['OS_REGION_NAME'] = 'regionOne' if 'region' not in creds else creds['region_name']
            else:
                raise OspShellError('The auth key in cloud credentials was empty or incorrect cloud specified.')
        else:
            for key, value in cloud_dict.items():
                if key in ['tenant_name', 'project_name']:
                    os.environ['OS_PROJECT_NAME'] = value
                    continue
                if key == 'domain_name':
                    os.environ['OS_DOMAIN_NAME'] = value
                    continue
                os.environ['OS_' + key.upper()] = value
        self.logger.info('Successfully loaded cloud credentials.')

    def load_available_os_commands(self):
        """
        Load the available commands groups and the respective
        commands into the shell as properties.

        :return:
        """

        results = self.run_command('command_list', {})
        if results['rc'] != 0:
            self.logger.error("Command to gather command options was not successful.")
            self.logger.error(results['stderr'])

        resp = results['stdout']
        resp = {cs.get('Command Group').split('.')[-2] if len(cs.get('Command Group').split('.')) > 2
                else cs.get('Command Group').split('.')[-1]: [c.replace(' ', '_')
                                                              for c in cs.get('Commands')] for cs in resp}
        setattr(self, 'all_osp_cmd_groups', resp)
        all_os_cmds = list()
        for cg, cs in resp.items():
            all_os_cmds.extend(cs)
            self.logger.debug("Caching list of commands for group: %s" % cg)
            setattr(self, "%s_commands" % cg, cs)
        setattr(self, "all_osp_commands", all_os_cmds)

    def _setup_logging(self, log_level='info'):
        """
        Setup basic logging for the library.

        :param log_level: str
        :return: logger
        """

        osplogger = getLogger('ospclientsdk')
        if not osplogger.handlers:
            chandler = StreamHandler()
            chandler.setLevel(LOG_LEVELS[log_level])
            if log_level == 'info':
                chandler.setFormatter(Formatter(LOG_FORMAT))
            else:
                chandler.setFormatter(Formatter(DEBUG_LOG_FORMAT))
            osplogger.setLevel(LOG_LEVELS[log_level])
            osplogger.addHandler(chandler)
        return osplogger

    def _setup_proxy_classes(self):
        """
        This will setup all the mixin proxy instances based on the command groups and commands
        discovered during the initialization and set them as properties dynamically.

        The mixin classes will be named after the command groups. The commands will be functions
        of the mixin
        :return:
        """

        for key, values in getattr(self, 'all_osp_cmd_groups').items():
            func_dict = dict()
            for v in values:
                # https://stackoverflow.com/questions/13184281/python-dynamic-function-creation-with-custom-names
                #
                def func(*args, **kwargs):
                    self.logger.debug(args[1])

                func.__name__ = v
                cmd = Command(func)
                func_dict.update({v: cmd})

            proxy_class = type('%sMixin' % "".join([word.capitalize() for word in key.split('_')]),
                               (object,),
                               func_dict)
            setattr(self, '%s' % key.lower(), proxy_class())

    def is_valid_command(self, cmd):
        """
        Test whether the specified command exists in cache and available from
        the client.

        :param cmd:
        :return:
        """
        if cmd.find('_') == -1:
            cmd = cmd.replace(' ', '_')
        if cmd not in getattr(self, 'all_osp_commands'):
            return False
        return True

    @Command
    def run_command(self, cmd, options):
        """
        This is a mid level convenience method that can be used
        in cases where new openstackclient plugins have been installed
        after the initialize but no higher level mixin function exists
        for it. You can still leverage it by passing a cmd as a string
        and the options/arguments as a dictionary

        cmd needs to utilize underscores where spaces would be, i.e.
        network_trunk_create == "network trunk create"

        :param cmd: str
        :param options: dict
        :return: dict
        """
        self.logger.debug("cmd: %s options: %s" % (cmd, options))

    @Command
    def run_raw_command(self, cmd_str):
        """
        This is a lowest level method that can be used to pass in a
        whole string command. i.e.

        'openstack <command> <options> <arguments>'

        It's not recommended to use this function unless necessary
        because it can accept any string and execute it
        locally which could be unsafe
        .
        :param cmd_str: str
        :return: dict
        """
        self.logger.debug("cmd: %s" % cmd_str)
