
A tiny C# utility to monitor Windows processes and kill the processes that work longer than the threshold specified:

# To Compile
```shell
$ mcs -out:WinProcessMonitor.exe WinProcessMonitor.cs
```

# To Run
```shell
$ mono WinProcessMonitor.exe processName 1000  2000 /path/to/logfile/log.txt
```
where
* processName  is the process name
* 1000     is the threshold (in seconds) after which the process will be killed
* 2000     is the watchdog time interval used to check if the target process is still running
* log.txt  is the log file

