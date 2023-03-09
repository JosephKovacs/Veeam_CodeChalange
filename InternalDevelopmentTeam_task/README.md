
To synchronizes two folders: <strong>source</strong> and <strong>replica</strong>, please run the Python script as following:

```shell
$ python SyncFolderContent.py --sd /path/to/source --rd /path/to/replica --sync_period 10 --logfile /path/to/logfile --verbosity 1
```

To dump help, please do
```shell
$ python SyncFolderContent.py --help

    usage: SyncFolderContent.py [-h] [--sd [SD]] [--rd [RD]] [--sync_period [SYNC_PERIOD]] [--logfile [LOGFILE]] [--verbosity [VERBOSITY]]

    optional arguments:
    -h, --help            show this help message and exit
    --sd [SD]             source directory
    --rd [RD]             replica directory
    --sync_period [SYNC_PERIOD]
                            sync periodicity in seconds
    --logfile [LOGFILE]   log filename
    --verbosity [VERBOSITY]
                            log verbosity level
```
