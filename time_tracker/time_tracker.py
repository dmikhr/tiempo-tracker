from time_tracker.db import TrackerDB, Task, WorkBlock
import time
import datetime
import os


class TimeTracker:
    def __init__(self, session=None):
        # if no session was supplyed connect to default database
        if session:
            self.session = session
        else:
            db_dir = os.path.dirname(os.path.realpath(__file__))
            self.session = TrackerDB(f'{db_dir}/tasks.db').connect()

    def task_add(self, name, description=''):
        """
        handle - already exists, write test
        search for task, if exists - show error
        description - currently not implemented
        """
        """add new task"""
        if len(self.session.query(Task).\
                            filter(Task.name == name).all()) == 0:
            self.session.add(
                            Task(name = name,
                                description = description)
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
        if len(self.session.query(Task).\
                            filter(Task.name == name).all()) == 1:
            task_id = self.session.query(Task).filter(Task.name == name).one().id
            # to-do: wrap in transaction
            self.session.query(Task).filter(Task.id == task_id).delete()
            self.session.query(WorkBlock).filter(WorkBlock.task_id == task_id).delete()
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
        if len(self.session.query(Task).filter(Task.name == name).all()) == 0:
            return f'Task {name} not found. Maybe task was incorrectly typed?'
        # if there is an active task - stop it first
        # if active task is the same - show message
        if self._any_active_task():
            task_id = self.session.query(Task).filter(Task.name == name).one().id
            if self.session.query(WorkBlock).filter(WorkBlock.finish_time == None).\
                                             one().task_id == task_id:
                return f'Task {name} is already in progress'
            self.task_finish()
        task_id = self.session.query(Task).filter(Task.name == name).one().id
        self.session.add(
                        WorkBlock(task_id = task_id,
                                  start_time = int(time.time()))
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
                                   filter(Task.id == active_block.task_id).one()

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
        """
        return 'Feature is under development'

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
        in case you were working for example up to 1 A.M. it makes sence to track that activity 
        as previous day
        hours after midnight
        """
        day_starts = 4
        seconds_in_hour = 60 * 60
        seconds_in_day = 24 * seconds_in_hour
        epoch_time = int(time.time())
        today_start_time = epoch_time - (epoch_time % (seconds_in_day)) + day_starts * seconds_in_hour
        today_work_blocks = self.session.query(WorkBlock).\
                                         filter(WorkBlock.finish_time >= today_start_time).\
                                         filter(WorkBlock.task_id == task_id).all()

        today_wrok_time = 0
        for today_work_block in today_work_blocks:
            today_wrok_time += (today_work_block.finish_time - today_work_block.start_time)
        return str(datetime.timedelta(seconds=today_wrok_time))

# fix multiple null records
# self.session.query(WorkBlock).filter(WorkBlock.finish_time == None).delete()
# self.session.commit()