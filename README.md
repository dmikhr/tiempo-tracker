Track time you've spent on different tasks. Then see how much time you've spent on each. 
Continuation of [time_management](https://github.com/dmikhr/time_management) script idea.

### **Built with**
Python, SQLAlchemy for managing database, SQLite as database (see [pyproject.toml](https://github.com/dmikhr/tiempo-tracker/blob/main/pyproject.toml) for details)
<br>Testing: Pytest

### **Installation**
**From source**
<br>run `make build` and  then `make package-install` in package directory.

When you run app for the first time it will create database. You'll see a message:
`Database not found. Creating new one`


### **Usage**
```
 -h, --help            show this help message and exit
  -s START, --start START
                        Start task by providing its name
  -f, --finish          Finish current task. Task also can be finished by starting a different task
  -a ADD, --add ADD     Add new task
  -r REMOVE, --remove REMOVE
                        Remove the task
  -l, --list            List of all tasks
  -st STATS, --stats STATS
                        Stats about tasks
```