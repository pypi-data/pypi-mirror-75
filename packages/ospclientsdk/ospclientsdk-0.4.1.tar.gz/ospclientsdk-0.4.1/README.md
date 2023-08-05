# ospclientsdk
An SDK like wrapper around the openstackclient to reduce the need to write boilerplate 
subprocess code. 

## Installation

Ospclientsdk can be easily installed with a one line command. It is recommended (as best practice) to create a virtual
environment and install ospclientsdk. Please see the commands below to install. Note this is only supported
in python 3.6 and higher.

```
# install python virtualenv
$ pip install python-virtualenv

# create virtualenv
$ virtualenv ospclientsdk

# activate virtualenv
$ source ospclientsdk/bin/activate

# install blaster
$ (ospclientsdk) pip install ospclientsdk
```

## Usage

Let's dive into how to use this sdk. 

### Initialize
When working with the sdk the main interface you will be interacting with is the 
**ClientShell** class. This interface can be initialized with with or without credentials

```python
from ospclientsdk import ClientShell
import yaml


"""
You can provide a string path to a clouds.yaml file. If a cloud isn't specified
the shell will default to using one called 'openstack'
"""
shell = ClientShell(cloud_file='clouds.yaml', cloud='test')


"""
You can also preload the clouds.yaml file or build the dictionary by hand 
and provide it that way.
"""
creds = {}
with open('clouds.yaml') as f:
    creds = yaml.safe_load(f)
shell = ClientShell(cloud_dict=creds, cloud='test')


"""
You can also load the shell with credentials after it has been initialized
"""
shell = ClientShell()
shell.load_cloud_config(cloud_dict=creds, cloud='test')
```

Once the shell has been intialized you can see what command groups and commands
are available in a couple of ways. 

Note when the commands are loaded the white spaces are replaced with 
underscores ('_') to make it easier to parse and find what you're looking for. i.e. 
*server create* to *server_create* 

```python
from ospclientsdk import ClientShell

shell = ClientShell(cloud_file='clouds.yaml', cloud='test')


"""
You can see a simplied version of all available command groups and their respective commands.
This will return a dictionary. Where the key is the name of the of the command group and 
the values are a list of commands supported by the command group.  
"""
cmd_groups = shell.all_osp_cmd_groups
cmd_list = cmd_groups.get('data_processing', {})


"""
If you already know the name of the command group you want and would like to see the 
commands available for it. You can access one of the many command group properties.
"""
cmd_list = shell.data_processing_commands


"""
If you would like to check which are the available commands irrespective of command group
you can do so as well
"""
all_cmds = shell.all_osp_commands
```
### Executing Commands
Once you have an idea of what commands you want to execute you have a few different ways of 
executing them. Before we dive into those, let's talk a little bit about generating the options
and their arguments. 

### Options

The options and argument values for the command actions are always defined as dictionaries. Let's
touch on a couple examples

#### Example 1

Any time an option takes an argument
```python

# This
command create --option arg <res_name>


# Can be defined like
{'option': 'arg', 'name': 'res_name'}
```

#### Example 2
Any time an option takes an argument and can be specified multiple times 
```python

# This
command create --option arg1 --option arg2 <res_name>

# Can be defined like
{'option': ['arg1', 'arg2'], 'name': 'res_name'}
```

#### Example 3
Any time an option takes an argument with the value in k=v 
```python

# This
command create --option arg1=val1

# Can be defined like
{'option': [{'arg1': 'val1'}], 'name': 'res_name'} 
```

#### Example 4
Any time an option takes an argument with the value in k=v and can be specified multiple times. 
```python

# This
command create --option arg1=val1 --option arg2=val2 <res_name>

# Can be defined like
{'option': [{'arg1': 'val1'}, {'arg2': 'val2'}], 'name': 'res_name'}
```

#### Example 5
Any time an option takes an argument but the value can be a comma separated list of k=v 
```python

# This
command create --option arg1=val1,arg2=val2,arg3=val3 <res_name>

# Can be defined like
{'option': [{'arg1': 'val1', 'arg2': 'val2', 'arg3': 'val3'}], 'name': 'res_name'}
```

#### Example 6
Any time an option takes no argument and actions like a boolean flag 
```python

# This
command create --option <res_name>

# Can be defined like
{'option': True, 'name': 'res_name'}
```

#### Example 7
In the case of *add* command actions, which not only require the name or id of the resource
it needs the name or id of the target resource you want to add
```python

# This
command add --option arg1 <res_name> <tgt_res>

# Can be defined like
{'option': 'arg1', 'name': 'res_name', 'tgt_name': 'tgt_res'}
```
**Note** rather than `name` you could supply `id` and rather than `tgt_name` you can supply `tgt_id` 

#### Example 7
In the case of *delete* command actions, you can specify multiple resources
```python

# This
command delete <res_name_1> <res_name_2>

# Can be defined like
{'name': ['res_name_1', 'res_name_2']}
```


For a full list of commands and options refer to the
[openstackclient](https://docs.openstack.org/python-openstackclient/latest/cli/command-list.html) documentation. 

#### High Level APIs
The first and recommended way is to use the high level APIs the shell provides 
through a series of proxy instances. Each proxy object reflects a command group
and provides APIs that map to the corresponding CLI commands.



##### Example 1

```python

from ospclientsdk import ClientShell

shell = ClientShell(cloud_file='clouds.yaml', cloud='test')

# Build a dictionary of the required arguements/options and their parameters.
# Each key is command option and the value is the parameter.
server_params = dict(name="ccit_test_client",
                     image="rhel-7.5-server-x86_64-released",
                     flavor="m1.small",
                     key_name="db2-test",
                     network=["test_private_network"],
                     wait=True
                     )

# To create a server using the above define dict I simply access
# the compute instance and us the server_create function
results = shell.compute.server_create(server_params)
``` 

##### Example 2

```python

from ospclientsdk import ClientShell

shell = ClientShell(cloud_file='clouds.yaml', cloud='test')

# Build a dictionary of the required arguements/options and their parameters.
# Each key is command option and the value is the parameter.
trunk_port_params = dict(name="test_compute_trunk",
                         parent_port="test_port",
                         subport=[dict(port="dummy_port",
                                       segmentation_type="vlan",
                                       segmentation_id=2007
                                      )]
                        )

# To create a network trunk port using the above defined dict I simply access
# the neutronclient instance and us the network_trunk_create function
results = shell.neutronclient.network_trunk_create(trunk_port_params)

``` 

#### Mid Level API

You can use the **run_command** to to supply the command 
(using the underscore version of the command) and a dictionary options and it's parameters. 

This can come in handy in scenarios where it's quite possible that other openstackclient 
plugins have been installed after the clientshell has been initialized. But you still want
to take advantage of supplying the command options and arguments as a dictionary. 

```python

from ospclientsdk import ClientShell

shell = ClientShell(cloud_file='clouds.yaml', cloud='test')

# Build a dictionary of the required arguements/options and their parameters.
# Each key is command option and the value is the parameter.
trunk_port_params = dict(name="test_compute_trunk",
                         parent_port="test_port",
                         subport=[dict(port="dummy_port",
                                       segmentation_type="vlan",
                                       segmentation_id=2007
                                      )]
                        )

# To create a network trunk port using the above defined dict I
# use I pass in the command as a string and the options as a dictionaru
results = shell.run_command('network_trunk_create', trunk_port_params)
``` 

#### Low Level API

You can use the function **run_raw_command** to explicitly run full commands. This will
allow you to pass in a string directly. 

This commmand might be useful if there are problems
with the clientshell normalizing the options or if you want to leverage the underlying shell to
chain together commands and do some complex processing without having to setup 
subprocess boilerplate code yourself.  

Note since we aren't doing any string checking make sure you aren't passing in anything unsafe
for the underlying shell to execute. Also make sure to escape your command properly. 
```python
from ospclientsdk import ClientShell

shell = ClientShell(cloud_file='clouds.yaml', cloud='test')

# Pass in a string representing a string command
results = shell.run_raw_command('openstack server show -f json')
``` 

### Output

When the ospclientsdk executes it will return back
to you a dictionary. It will contain the following keys:
* rc
* stdout
* stderr

You can use the rc value to determine if the command passed (0) or failed (1) and how to respond to 
either scenario. The stdout key will always be deserialized into a dictionary so that 
it can be easily manipulated and accessed. The stderr will typically always be a text string.

### Running openstack commands remotely

There are use cases where it's useful to run the commands remotely on a test driver or bastion host.
The SDK provides a `remote_shell` context that can forward all CLI commands to the desired host without 
a lot of extra boilerplate code. Before using this context first install the necessary ssh package:

```bash
$ pip install ospclientsdk['remote_shell']
``` 

Next it's recommended you will load your ssh agent up with a key appropriate to the target client host.

Then you can start using it. Below are some examples

```python
from ospclientsdk import ClientShell, remote_shell

shell = ClientShell(cloud_file='clouds.yaml', cloud='test')

# Build a dictionary of the required arguements/options and their parameters.
# Each key is command option and the value is the parameter.
server_params = dict(name="ccit_test_client",
                     image="rhel-7.5-server-x86_64-released",
                     flavor="m1.small",
                     key_name="db2-test",
                     network=["test_private_network"],
                     wait=True
                     )


# Here is an example where we log into a remote host using user 'cloud-user' and a key file
# using the high level api
with remote_shell(hostname="10.x.x.x", username="cloud-user", key_file="keys/test-key"):
        results = shell.compute.server_create(server_params)


# Here is an example running raw commands to a remote host using the FQDN and 'fedora' user 
# but we've specified a client path for where to look for the 'openstack' binary since it is
# not in the $PATH on the remote host. This comes in useful if you've installed the client
# in a virtualenv on the remote host.
with remote_shell(hostname="host.example.com", username="fedora", key_file="keys/test-key", client_path="/home/fedora/cbn/bin"):
        results = shell.run_raw_command('openstack server show -f json')

```

