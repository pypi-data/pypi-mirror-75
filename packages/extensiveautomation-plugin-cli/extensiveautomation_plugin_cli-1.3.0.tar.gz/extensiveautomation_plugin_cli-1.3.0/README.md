# CLI plugin for ExtensiveAutomation server

This plugin enable to interact with remote system throught the SSH protocol.

## Table of contents
* [Installing from pypi](#installing-from-pypi)
* [Installing from source](#installing-from-source)
* [About actions](#about-actions)
    * [ssh/send_commands.yml](#sshsend_commandsyml)
    * [ssh/send_expect.yml](#sshsend_expectyml)
* [About workflows](#about-workflows) 
    * [ssh/send_commands.yml](#sshsend_commandsyml)
    * [ssh/send_expect.yml](#sshsend_expectyml)
    
## Installing from pypi

1. Run the following command

        pip install extensiveautomation_plugin_cli

2. Execute the following command to take in account this new plugin

        ./extensiveautomation --reload
        
3. Samples are deployed on data storage.

## Installing from source

1. Clone the following repository 

        git clone https://github.com/ExtensiveAutomation/extensiveautomation-plugin-cli.git
        cd extensiveautomation-plugin-cli/src/ea/
        
2. Copy the folder `sutadapters` in the source code server and overwrite-it

        cp -rf sutadapters/ /<install_path_project>/src/ea/
        
3. Copy the folder `var` in the source code server/ and overwrite-it

        cp -rf var/ /<install_path_project>/src/ea/

4. Finally execute the following command to install depandencies

        cd /<install_path_project>/src/
        python3 extensiveautomation.py --install-adapter CLI
        python3 extensiveautomation.py --reload
        
## About actions

## ssh/send_commands.yml

Send ssh commands on one or severals hosts.

Parameter(s):
- ssh-commands (text): bash commands

```yaml
- name: ssh-commands
  value: |-
    echo "hello world" >> /var/log/messages
    echo "hola mondu" >> /var/log/messages
```
 
- ssh-hosts (list): ssh remote addresses

```yaml
- name: ssh-hosts
  value:
   - ssh-host: 10.0.0.55
     ssh-login: root
     ssh-password: bonjour
```

- agent (text): agent name to use

```yaml
- name: ssh-agent
  value: agent02.ssh
```

## ssh/send_expect.yml

Send ssh commands on one or severals hosts and expect outputs.

Parameter(s):
- ssh-commands (text): bash commands

```yaml
- name: ssh-commands
 value: |-
    # get hostname
    uname -n
    .*\n[!CAPTURE:MACHINE_HOSTNAME:]\n.*
```
   
- ssh-hosts (dict): ssh remote addresses

```yaml
- name: ssh-hosts
  value:
   - ssh-host: 10.0.0.55
     ssh-login: root
     ssh-password: bonjour
```

- agent (text): agent name to use

```yaml
- name: ssh-agent
  value: agent02.ssh
```

## About workflows

## ssh/send_commands.yml

This worflow show how to use `ssh` actions.

## ssh/send_expect.yml

This worflow show how to use `ssh` actions.
