# remove-actions-opennebula
Remove actions from OpenNebula virtual machine, e.g. `terminate`, `stop` etc. Tested on OpenNebula 5.2.1+

![actions](https://ctrlv.cz/shots/2018/08/14/1tMw.png)

## Installation
Run `$ ./install.sh` as root.

## Usage
After installation you can use `remove_actions_opennebula` from shell.
```bash
$ remove_actions_opennebula --help
usage: remove_actions_opennebula [-h] [-u URL] [-p PROTOCOL] [-c CHROMEDRIVER]
                                 [-a ACTIONS [ACTIONS ...]]
                                 username password vm_name

Delete actions from OpenNebula VM.

positional arguments:
  username              OpenNebula username.
  password              OpenNebula password.
  vm_name               VM name.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to OpenNebula. (default: cloud.metacentrum.cz)
  -p PROTOCOL, --protocol PROTOCOL
                        Web protocol. (default: https://)
  -c CHROMEDRIVER, --chromedriver CHROMEDRIVER
                        Path to chromedriver binary. (default:
                        /usr/local/bin/chromedriver)
  -a ACTIONS [ACTIONS ...], --actions ACTIONS [ACTIONS ...]
                        Action types to remove. (default: ['terminate-hard'])

```

*Note: if provided, `actions` parameter must be the last one.*

### Example
```bash
$ remove_actions_opennebula <username> <password> <vm_name> -a stop release
Logged in!
Removed action 'terminate' sheduled at '01:00:00 01/01/2020'
Removed action 'stop' sheduled at '01:00:00 01/02/2020'
Removed action 'terminate' sheduled at '01:00:00 01/02/2021'
Done! Exiting...
```
