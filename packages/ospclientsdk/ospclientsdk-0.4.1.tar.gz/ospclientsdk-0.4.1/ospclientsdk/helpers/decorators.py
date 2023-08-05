"""
    helpers.decorators

    The decorator that contains the logic for executing the
    openstack cli commands.

"""

import os
import json
import subprocess
from logging import getLogger
from string import Template
from functools import update_wrapper
from .context import cur_context
from shlex import split

LOG = getLogger(__name__)


class Command(object):
    """
    Command is a class decorator that handles the underlying functionality
    of executing the openstack commands locally through subprocess. This makes
    it easier to add future api commands that reflect the cli without repeating
    this logic code in the mixin classes.
    """

    default_os_command_template = Template("openstack $command $options")
    alt_remote_os_command_template = Template("$client_path/$os_command")

    def __init__(self, func):
        update_wrapper(self, func)
        self.function = func

    def __call__(self, *args, **kwargs):
        """
        This is the brains of the class that get's called when a decorated
        :param args:
        :param kwargs:
        :return:
        """
        self.function(*args, **kwargs)
        func_name = self.function.__name__

        # This means function declared in one of the command group mixins was called
        # because only commmand options parameter is passed. The idea
        # is we infer the command requested based on the function executed. i.e.
        # the 'server_create(options)' function would normalize and map to 'server create'
        # on the CLI.
        if len(args) == 2 and func_name.find('raw') == -1:
            return self.run_cmd(func_name, args[1], context=cur_context())

        # Assume the user is trying has called the run_raw_command function to pass in a raw
        # string of an openstack command. Either because there is an api call that
        # maps to a CLI command or a particular option and it's argument can't/hasn't been
        # normalized yet.
        elif len(args) == 2 and func_name.find('raw') != -1:
            return self.run_cmd_raw(args[1], context=cur_context())

        # This means run_command function in shell implementation is called because
        # user passes in the cmd as a parameter. Most likely because one of the command
        # mixin classes does not have a defined function yet that maps to a particular
        # command on the CLI.
        elif len(args) == 3:
            LOG.info(args)
            return self.run_cmd(args[1], args[2], context=cur_context())

    def __get__(self, instance, owner):
        # Refer to the second answer on why I added this
        # so I can implement the descriptor protocol
        # https://stackoverflow.com/questions/2365701/decorating-python-class-methods-how-do-i-pass-the-instance-to-the-decorator
        from functools import partial
        return partial(self.__call__, instance)

    def run_cmd(self, cmd, options, context=None):
        """
        This is a higher level api command, that is used to normalize and
        join the final command to it options and parameters.

        :param cmd: str
        :param options: dict
        :return: str
        """
        opts = self._normalize_options(options)
        cmd = cmd.replace('_', ' ')
        if len(set(cmd.split(' ')).intersection(['create', 'list', 'show'])) != 0 and opts.find('--help') == -1:
            opts += ' -f json'
        cmd_str = self.default_os_command_template.safe_substitute(command=cmd, options=opts)

        LOG.info(cmd_str)
        return self.run_cmd_raw(cmd_str, context)

    def run_cmd_raw(self, command, context=None):
        """
        This is a lower level api command meant to pass the full
        joined cli command with it's options

        :param command: str
        :return: str
        """
        LOG.debug('command: %s' % command)
        resp = self.exec_local_cmd(command, context)

        try:
            # Let's try to deserialize into a dictionary for easier manipulation
            data = json.loads(resp['stdout'])
            resp['stdout'] = data
            return resp
        except Exception:
            # assume it's not a json so just return the output
            return resp

    def _normalize_options(self, options):
        """
        This takes the dictionary representation of cli command arguments and options
        and normalizes it into their respective format. Example

        This dictionary of arguments/options for 'server create'

        dict(image='rhel-7.5-server-x86_64',
            flavor='m1.small',
            network=['provider_net', 'private_net'],
            max=2,
            key_name='test-key',
            name='test_client')

        is converted to:

        --image rhel-7.4-server-x86_64
        --flavor m1.small
        --network private_net
        --network provider_net
        --key-name test-key
        test_client


        :param options: dict
        :return: str
        """
        cmd_str = ""
        if isinstance(options, dict):
            asset = options.pop('name') if options.get('name', None) else options.pop('id', None)

            # This most likely means it's an add command so we need to append this as the last argument
            target = options.pop('tgt_name') if options.get('tgt_name', None) else options.pop('tgt_id', None)

            for key, val in options.items():
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            opt_list = ["=".join([k.replace('_', '-'), str(v)]) for k, v in item.items()]
                            if len(opt_list) > 1:
                                opt_list = ",".join(opt_list)
                            else:
                                opt_list = opt_list[-1]
                            cmd_str += "--%s %s " % (key.replace('_', '-'), opt_list)
                            continue
                        cmd_str += "--%s %s " % (key.replace('_', '-'), item)
                    continue
                if isinstance(val, bool):
                    cmd_str += "--%s " % key.replace('_', '-')
                    continue
                if isinstance(val, str):
                    if os.path.isdir(val) or os.path.isfile(val):
                        val = os.path.abspath(val)
                    if os.path.sep in val and not os.path.isfile(val):
                        val = os.path.abspath(val)
                    cmd_str += "--%s %s " % (key.replace('_', '-'), val)
                    continue
                cmd_str += "--%s %s " % (key.replace('_', '-'), val)
            if asset:
                if isinstance(asset, list):
                    asset = " ".join(asset)
                cmd_str += asset
            if target:
                cmd_str += " %s" % target
        return cmd_str

    def exec_local_cmd(self, cmd, context=None):
        """Execute command locally.

        :param cmd: str
        :return: dict
        """
        resp = dict()

        # there is a context assume we are running commmands over
        # ssh so we use plumbum sshmachine to easily setup the
        # connection and auth env vars
        if context:
            from plumbum import SshMachine
            with SshMachine(host=context.hostname,
                            user=context.username,
                            port=context.port,
                            keyfile=context.key_file,
                            password=context.password,
                            ssh_opts=context.ssh_opts) as shell:

                # set the local auth variables remotely
                for k, v in context.get_os_vars().items():
                    shell.env.update({k: v})

                # if a client path assume not in PATH, we need to prefix the command
                if context.client_path:
                    cmd = self.alt_remote_os_command_template.safe_substitute(client_path=context.client_path,
                                                                              os_command=cmd)
                    LOG.debug(cmd)

                # run command over ssh and return the results
                proc = shell.popen(split(cmd))
                output = proc.communicate()
                resp['rc'] = proc.returncode
                resp['stdout'] = output[0].decode('utf-8')
                resp['stderr'] = output[1].decode('utf-8')
                return resp

        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = proc.communicate()
        resp['rc'] = proc.returncode
        resp['stdout'] = output[0].decode('utf-8')
        resp['stderr'] = output[1].decode('utf-8')
        return resp
