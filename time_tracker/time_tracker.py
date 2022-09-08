from time_tracker.db import TrackerDB, Task, WorkBlock
import time
import datetime
from pathlib import Path
import os


class TimeTracker:
    def __init__(self, session=None, epoch_time=None):
        # if no session was supplyed connect to default database
        if session:
            self.session = session
        else:
            db_dir = os.path.dirname(os.path.realpath(__file__))
            db_path = Path(f'{db_dir}/tracker.db')
            if not db_path.is_file():
                print('Database not found. Creating new one')
                print("If you run app for the first time - it's normal behavior")
                TrackerDB(str(db_path)).create()
            self.session = TrackerDB(str(db_path)).connect()

        # can be used for testing purposes
        self.epoch_time = epoch_time

    def task_add(self, name, description=''):
        """
        handle - already exists, write test
        search for task, if exists - show error
        description - currently not implemented
        """
        """add new task"""
        if not self._task_exists(name):
            self.session.add(
                            Task(name=name,
                                 description=description)
                            )
            self.session.commit()

            return f'Task {name} was added'
        else:
            return f'Task {name} already exists'

    # idea: replace if-check with decorator
    # @check(error_msg)
    def task_remove(self, name):
        # handle - not found and write test
        """remove task"""
        if self._task_exists(name):
            task_id = self._task_id(name)
            # to-do: wrap in transaction
            self.session.query(Task).filter(Task.id == task_id).delete()
            self.session.query(WorkBlock).filter(WorkBlock.task_id == task_id)\
                                         .delete()
            self.session.commit()
            # transaction end

            return f'Task {name} was removed'
        return f'Task {name} not found'

    def task_start(self, name):
        """
        check if any task in progess already
        return message what task is running already
        handle task not found
        """
        if not self._task_exists(name):
            return f'Task {name} not found. Maybe task was incorrectly typed?'
        # if there is an active task - stop it first
        # if active task is the same - show message
        if self._any_active_task():
            task_id = self._task_id(name)
            if self.session.query(WorkBlock).\
                    filter(WorkBlock.finish_time == None).\
                    one().task_id == task_id:
                return f'Task {name} is already in progress'
            self.task_finish()
        task_id = self._task_id(name)
        self.session.add(
                        WorkBlock(task_id=task_id,
                                  start_time=int(time.time()))
                        )
        self.session.commit()

        return f'Task {name} is in progress now...'

    def task_finish(self):
        # refactor - get_active_task
        if not self._any_active_task():
            return 'No task is in progress. Start task first.'
        active_block = self.session.query(WorkBlock).\
                            filter(WorkBlock.finish_time == None).one()
        active_task = self.session.query(Task).\
                                   filter(Task.id == active_block.task_id)\
                                    .one()

        finish_time = int(time.time())

        active_block.finish_time = finish_time
        self.session.commit()
        self.session.flush()

        return (f'Task {active_task.name} was finished.'
                f'\nLast session time: {self._time_active_last(active_block.start_time, finish_time)}'
                f'\nTime in task today: {self._time_active_today(active_task.id)}'
                )

    def tasks_list(self):
        # to-do - implement sorting
        active_task_id = -1
        tasks = self.session.query(Task).limit(-1).all()
        if self._any_active_task():
            active_task_id = self.session.query(WorkBlock).\
                                        filter(WorkBlock.finish_time == None).one().task_id
        tasks_output = []
        for task in tasks:
            tasks_output.append(f"{task.name}{' (in progress)' if task.id == active_task_id else ''}")
        return '\n'.join(tasks_output)

    def tasks_stats(self):
        """
        will be implemented in future versions
        time spent on each task. Show only tasks that were active today.
        Time is calculated for today (with respect to day_starts in _time_active_today())
        """
        today_active_tasks = {}
        # idea for future improvements: implement with join
        today_work_blocks_all = self.session.query(WorkBlock).\
                                             filter(WorkBlock.finish_time >= self._today_start_time()).all()
        # distinct on throws SADeprecationWarning, for reliability implement feature without it for now
        task_id_distinct = set(map(lambda item: item.task_id, today_work_blocks_all))
        for task_id in task_id_distinct:
            task_name = self.session.query(Task).filter(Task.id == task_id).one().name
            today_active_tasks[task_name] = self._time_active_today(task_id)
        # consider moving to separate method
        output_text = []
        for task, time_str in today_active_tasks.items():
            output_text.append(f'{task}\t{time_str}')
        return '\n'.join(output_text)

    def task_status(self):
        """
        shows whether there is a task in progress
        if any task is active - show how much time you're working on it
        """
        # to-do: refactor task_finish and task_status
        if not self._any_active_task():
            return 'No task is active'
        active_block = self.session.query(WorkBlock).\
                                   filter(WorkBlock.finish_time == None).one()
        active_task = self.session.query(Task).\
                                   filter(Task.id == active_block.task_id).one()
        return (f'Task in progress: {active_task.name}'
                f'\nCurrent session time: {self._time_active_last(active_block.start_time, int(time.time()))}'
                f'\nTime in task today: {self._time_active_today(active_task.id)}'
                )

    def _any_active_task(self):
        return len(self.session.query(WorkBlock).filter(WorkBlock.finish_time == None).all()) == 1

    def _time_active_last(self, start_time, finish_time):
        time_delta = finish_time - start_time
        return str(datetime.timedelta(seconds=time_delta))

    def _time_active_today(self, task_id):
        """
        return amount of time spent on a given task today
        change when new day starts
        """
        today_work_blocks = self._work_blocks_today(task_id)
        today_work_time = 0
        for today_work_block in today_work_blocks:
            today_work_time += (today_work_block.finish_time - today_work_block.start_time)
        # in future development consider making _time_active_today return time in seconds and
        # add another method to format time for output to keep time calculation
        # and its representation separate
        time_formatted = self._round_time_and_fromat(str(datetime.timedelta(seconds=today_work_time)))
        time_decimal = self._time_to_decimal(time_formatted)
        return f'{time_formatted} ({time_decimal})'

    def _round_time_and_fromat(self, time_str):
        """
        remove seconds, round up if seconds >= 45 sec.
        '0:20:00' -> '0:20', '0:20:35' -> '0:20'
        assuming time blocks can't exceed 24hr - all stats currently works for 1 day data
        can be implemented with str formatting, but here for educational purposes implemented from scratch
        """
        hr, min, sec = time_str.split(':')
        if int(sec) > 45:
            if int(min) < 59:
                min = str(int(min) + 1)
                if int(min) < 10:
                    min = str(f'0{min}')
            elif int(min) == 59:
                min = '00'
                hr = str(int(hr) + 1)
        return f'{hr}:{min}'

    def _time_to_decimal(self, time_str):
        """
        for long term time tracking in spreadsheets decimal time representation might be useful
        for things like time management, task prioritisation analysis, etc.
        """
        hr, min = time_str.split(':')
        return round((int(hr) * 60 + int(min)) / 60, 1)

    def _work_blocks_today(self, task_id):
        """
        in case you were working for example up to 1 A.M. it makes sence to track that activity
        as previous day hours after midnight
        """
        today_work_blocks = self.session.query(WorkBlock).\
                                         filter(WorkBlock.finish_time >= self._today_start_time()).\
                                         filter(WorkBlock.task_id == task_id).all()
        return today_work_blocks

    def _task_id(self, task_name):
        return self.session.query(Task).filter(Task.name == task_name).one().id

    def _task_exists(self, task_name):
        return len(self.session.query(Task).\
                                filter(Task.name == task_name).all()) == 1

    def _today_start_time(self):
        day_starts = 4 # hrs
        seconds_in_hour = 60 * 60
        seconds_in_day = 24 * seconds_in_hour
        if self.epoch_time:
            epoch_time = self.epoch_time
        else:
            epoch_time = int(time.time())
        return epoch_time - (epoch_time % (seconds_in_day)) + day_starts * seconds_in_hour
