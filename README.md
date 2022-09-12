### Introduction
---
Track time you've spent on different tasks. Then see how much time you've spent on each. 
Continuation of [time_management](https://github.com/dmikhr/time_management) script idea.
<br><br>

### **Development**
---
Built with Python, Poetry, SQLAlchemy for managing database, SQLite as database. 
<br>Testing: Pytest<br>
<br>Run package without building: `poetry run python -m time_tracker [options]` in the project directory
<br>Example: `poetry run python -m time_tracker -a Task1`
<br>Run tests: `poetry run pytest`
<br><br>

### **Installation**
---
**From source**
<br>run `make build` and then `make package-install` in the package directory.
<br>
**PIP**<br>
run `pip install tiempo-tracker`
<br>
When you run app for the first time it will create database. You'll see a message:
`Database not found. Creating new one`. Also app will show path where database is stored.
<br>
<br>

### **Usage**
---
tiempo-tracker can be invoked by `trt` command in terminal.
<br><br>Available options:
```
 -h, --help            show this help message and exit
  -s START, --start START
                        Start task by providing its name
  -f, --finish          Finish current task. Task also can be finished 
                        by starting a different task
  -a ADD, --add ADD     Add new task
  -r REMOVE, --remove REMOVE
                        Remove the task
  -l, --list            List of all tasks
  -st STATS, --stats STATS
                        Stats about tasks
```

Start with adding new task:<br>
`trt -a task1`
<br><br>
Then track the task:<br>
`trt -s task1`<br>

To finish the task either start new one (add new task first if it doesn't exist yet):<br>
`trt -s task2`
<br>or finish task<br>
`trt -f`<br>
Show all added tasks:
`trt -l`<br>
If particular task is in progress there will be `(in progress)` status behind this task. Example:
```
Project_work
Exercising (in progress)
Flask_API_project
Some_task
```

Remove task if it's no longer needed:<br>
`trt -r`<br>

See how much time you've spent on each task during the day:<br>
`trt -st`<br>
Time will be presented in two formats `hr:min` and as decimal number. The latter is convenient if you track your time in spreadsheet and analyze it (how much time was spend on each task during different periods of time, visualization, etc.).