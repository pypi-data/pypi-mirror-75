import os
from threading import local
from logging import getLogger

LOG = getLogger(__name__)


def cur_context():
    """
    This is used by the Command object functions
    to retrieve the SshContext object from the local
    context stack.
    """
    if context.stack:
        return context.stack[-1]


class SshContext(object):
    """
    SshContext is a context object
    that gets initialized by the remote_shell
    function and stores all the SSH data to
    be sent to Command decorator.
    """
    def __init__(self,
                 hostname=None,
                 username='root',
                 port=22,
                 password=None,
                 connect_timeout=600,
                 key_file=None,
                 ssh_opts=(),
                 client_path=None):

        self.client_path = client_path
        self.hostname = hostname
        self.username = username
        self.port = port
        self.password = password
        self.connect_timeout = connect_timeout
        self.key_file = key_file
        self.ssh_opts = ssh_opts

    def __enter__(self):
        """
        When in context it adds itself
        to the local context stack.

        :return: SshContext Object
        """
        context.stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Once the context is exited, it removes itself
        from the local context stack.

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        context.stack.pop()

    def get_os_vars(self):
        """
        Retrieves the local OS auth environmental
        variables set locally so that they can be
        set remotely

        :return: dict
        """
        vars_dict = {k: v for k, v in os.environ.items() if k.find('OS_') != -1}
        return vars_dict


def remote_shell(hostname=None,
                 port=22,
                 username='root',
                 password=None,
                 connect_timeout=600,
                 key_file=None,
                 ssh_opts=[],
                 client_path=None):
    """
    Used by 'with' to SSH to a remote host and run commands
    remotely.

    :param hostname: the shortname,FQDN, or IP of the host to connect to
    :param port: the port to use, will default to 22
    :param username: the username to login with, will default to 'root'
    :param password: the password to login with. Not required if using key_file
    :param connect_timeout: the connection timeout, defaults to 5 minutes
    :param key_file: the ssh key file (-i ) that should be used for passwordless ssh. Not required if using password
    :param ssh_opts: ssh options to append to the connection
    :param client_path: an alternative path that should be used to get to the 'openstack' command when not in $PATH
    :return: SshContext object
    """

    if key_file:
        key_file = os.path.abspath(key_file)

    _ssh_opts = ['-oPasswordAuthentication=no',
                 '-oStrictHostKeyChecking=no']

    if ssh_opts:
        _ssh_opts.extend(ssh_opts)

    c = SshContext(hostname=hostname,
                   port=port,
                   username=username,
                   password=password,
                   connect_timeout=connect_timeout,
                   key_file=key_file,
                   ssh_opts=tuple(set(_ssh_opts).union(ssh_opts)) if ssh_opts else tuple(_ssh_opts),
                   client_path=client_path
                   )

    return c


class LocalContext(local):

    def __init__(self):

        self.stack = []


# All threads will have a context which is
# managed by a stack of Context objects.
context = LocalContext()
