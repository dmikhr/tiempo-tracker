Introduction
=========================
Track time you've spent on different tasks. Then see how much time you've spent on each. 
Continuation of `time_management <https://github.com/dmikhr/time_management>`_ script idea.


**Development**
=========================
Built with Python, Poetry, SQLAlchemy for managing database, SQLite as database. 
Testing: Pytest
Run package without building: ``poetry run python -m time_tracker [options]`` in the project directory
Example: ``poetry run python -m time_tracker -a Task1``
Run tests: ``poetry run pytest``


**Installation**
=========================
**From source**
run ``make build`` and then ``make package-install`` in the package directory.

**PIP**
run ``pip install tiempo-tracker``

When you run app for the first time it will create database. You'll see a message:
``Database not found. Creating new one``. Also app will show path where database is stored.


**Usage**
=========================
tiempo-tracker can be invoked by ``trt`` command in terminal.
Available options:
::
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


Start with adding new task:
``trt -a task1``

Then track the task:
``trt -s task1``

To finish the task either start new one (add new task first if it doesn't exist yet):
``trt -s task2``
or finish task
``trt -f``
Show all added tasks:
``trt -l``
If particular task is in progress there will be ``(in progress)`` status behind this task. Example:
``````
Project_work
Exercising (in progress)
Flask_API_project
Some_task
``````

Remove task if it's no longer needed:
``trt -r``

See how much time you've spent on each task during the day:
``trt -st``
Time will be presented in two formats ``hr:min`` and as decimal number. The latter is convenient if you track your time in spreadsheet and analyze it (how much time was spend on each task during different periods of time, visualization, etc.).