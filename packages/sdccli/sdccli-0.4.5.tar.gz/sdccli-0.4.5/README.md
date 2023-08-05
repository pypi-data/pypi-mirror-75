Sysdig Monitor/Secure Python CLI
===

A Python client CLI for Sysdig Monitor/Sysdig Secure.

Installation
------------
#### Manual ([virtualenv](http://virtualenv.readthedocs.org/en/latest/) is recommended.)
    python3 setup.py install
#### Docker
    docker build -t sdc-cli .
    docker run -v config.yml:/config.yml sdc-cli [options]...


Configuration
-------------

The token can be passed as an environment variable in `SDC_TOKEN` or with separated variables
for montior (`SDC_MONITOR_TOKEN`) and secure (`SDC_SECURE_TOKEN`):
```
$ SDC_TOKEN=<token> sdc-cli scanning runtime list
```

The url can be passed as the environment variables `SDC_MONITOR_URL` for the monitor and
`SDC_SECURE_URL` for the secure.

It can also be configured in `~/.config/sdc-cli/config.yml` or `/etc/sdc-cli/config.yml`.
This configuration file can have multiple environments, where `main` will be used if the
environment is not explicitly selected (by the variable `SDC_ENV` or the `-e` option):
```
envs:
    main: # Default environment
        monitor:
            token: "" # Add here your monitor token
            url: "" # Add here the monitor url or remove it if you don't use it on prem
            disable_ssl_verification: yes
        secure:
            token: "" # Add here your secure token
            url: "" # Add here the secure url or remove it if you don't use it on prem

    other: # Another environment
        secure:
            token: ""
```


Usage
-----

Run it without parameters to get the list of all the commands:
```
$ sdc-cli
Usage: sdc-cli [OPTIONS] COMMAND [ARGS]...

  You can provide the monitor/secure tokens by the SDC_MONITOR_TOKEN and
  SDC_SECURE_TOKEN environment variables.

Options:
  -c, --config TEXT  Uses the provided file as a config file. If the config
                     file is not provided, it will be searched at
                     ~/.config/sdc-cli/config.yml and /etc/sdc-cli/config.yml.
  -e, --env TEXT     Uses a preconfigured environment in the config file. If
                     it's not provided, it will use the 'main' environment or
                     retrieve it from the env var SDC_ENV.
  --json             Output raw API JSON
  --version          Show the version and exit.
  --help             Show this message and exit.

Commands:
  alert       Sysdig Monitor alert operations
  backup      Backup operations
  capture     Sysdig capture operations
  command     Sysdig Secure commands audit operations
  compliance  Sysdig Secure compliance operations
  dashboard   Sysdig Monitor dashboard operations
  event       Sysdig Monitor events operations
  policy      Sysdig Secure policy operations
  scanning    Scanning operations
  settings    Settings operations
  profile     Profile operations
```

Run it with `--help` to see all the documentation of a subcommand:
```
$ sdc-cli event add --help
Usage: sdc-cli event add [OPTIONS] NAME

  NAME: the name of the new event.

Options:
  --description TEXT  a longer description offering detailed information about
                      the event.
  --severity INTEGER  syslog style from 0 (high) to 7 (low).
  --filter TEXT       metadata, in Sysdig Monitor format, of nodes to
                      associate with the event, e.g. ``host.hostName =
                      'ip-10-1-1-1' and container.name = 'foo'``.
  --tag TEXT          A key=value that can be used to tag the event. Can be
                      used for filtering/segmenting purposes in Sysdig
                      Monitor.
  --help              Show this message and exit.
```

Every command can be run with `--json` to get the full json response:
```
$ sdc-cli --json scanning runtime list
{
    "scope": "",
    "time": {
        "from": 1552936553745052,
        "to": 1552936613745052
    },
    "images": [
        {
            "imageId": "c6ff8a6aa5f62c37f1e47d61baaf635ab0d10aa784ceeed16f340f95292fcfc6",
            "repo": "docker.io/wallabag/wallabag",
            "tag": "latest",
            "digest": "sha256:8a80a21a2c3492a6c34c198e8d0a27795bdd741dcdf8448ad862292cc143f06f",
            "analysisStatus": "analyzed",
            "policyEvalStatus": "fail",
            "containers": [
                {
                    "containerId": "fbfb5fbd20f0"
                }
            ]
        }
    ]
}

```

Some examples:
* Get the list of scanning images:
```
$ sdc-cli scanning image list
Full Tag                                  Image ID                                                                Analysis Status
[...]
docker.io/debian:latest                   a0bd3e1c8f9eb8ff9d65828e8062ae9284b60cb83abe59fe46c74d77d88eb952        analyzed
```
* Get one image by tag:
```
$ sdc-cli scanning image get docker.io/debian:latest
```
* Create a secure capture:
```
$ sdc-cli capture --secure add --duration 120 mycapture myhost
```

Date fromat
-----------

Many commands accept dates and date ranges. sdc-cli is very permissive on date formats. Some examples of valid dates and their translations are:
* "2019-05-01" -> May 1, 2019 at 00:00
* "9AM" -> 9:00 AM of current day
* "9:00" -> 9:00 AM of current day
* "May 1" -> May 1 of current year at 00:00
* "1" -> Day 1 of current month at 00:00
* "May 1 9:00" -> May 1 of current year at 9:00 AM


Bash/Zsh Complete
-----------------

To enable bash completion add the following to your .bashrc:
```
eval "$(_SDC_CLI_COMPLETE=source sdc-cli)"
```

Or for zsh add in your .zshrc:
```
eval "$(_SDC_CLI_COMPLETE=source_zsh sdc-cli)"
```
