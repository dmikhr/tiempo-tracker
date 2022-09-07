from sqlalchemy import create_engine, desc, update
from sqlalchemy.orm import sessionmaker, Session
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
            # self.session = TrackerDB('tasks.db').connect()
            db_dir = os.path.dirname(os.path.realpath(__file__))
            self.session = TrackerDB(f'{db_dir}/tasks.db').connect()

    def task_add(self, name, description=''):
        # handle - already exists, write test
        # search for task, if exists - show error
        """add new task"""
        self.session.add(
                        Task(name = name, 
                             description = description)
                        )
        self.session.commit()

        return f'Task {name} was added'

    def task_remove(self, name):
        # handle - not found and write test
        """remove task"""
        task_id = self.session.query(Task).filter(Task.name == name).one().id
        # to-do: wrap in transaction
        self.session.query(Task).filter(Task.id == task_id).delete()
        self.session.query(WorkBlock).filter(WorkBlock.task_id == task_id).delete()
        self.session.commit()
        # transaction end

        return f'Task {name} was removed'
    
    def task_start(self, name):
        # check if any task in progess already
        # return message what task is running already
        # handle task not found
        task_id = self.session.query(Task).filter(Task.name == name).one().id
        self.session.add(
                        WorkBlock(task_id = task_id, 
                                  start_time = int(time.time()))
                        )
        self.session.commit()

        return f'Task {name} is in progress now...'
    
    def task_finish(self):
        # refactor - get_active_task
        active_block = self.session.query(WorkBlock).\
                                   filter(WorkBlock.finish_time == None).\
                                   order_by(desc(WorkBlock.start_time)).one()
        active_task = self.session.query(Task).\
                                   filter(Task.id == active_block.task_id).one()
        stmt = update(WorkBlock).where(WorkBlock.id == active_task.id).\
                                 values(finish_time=int(time.time()))
        self.session.execute(stmt)
        self.session.commit()

        return (f'Task {active_task.name} was finished.'
                f'Last session time: {self._time_active_last(active_block)}'
                # f'Time in task today: {self._time_active_today(active_task)}'
                )
    
    def tasks_list(self):
        return self.session.query(Task).limit(-1).all()
    
    def tasks_stats(self):
        pass

    def task_status(self):
        """
        shows whether there is a task in progress
        if any task is active - show how much time you're working on it
        """
        pass
        # if (task := get_active_task()):
        #     print(f"Active task: {task.name}\nTime in progress (uninterrupted): {task.time_uninterrupted}\n Total today: {task_time_today}")
        # else:
        #     print('No task in progress')

    def _active_task(self):
        self.session.query(WorkBlock).filter(WorkBlock.finish_time == None).\
                                      order_by(desc(WorkBlock.start_time)).one()

    def _time_active_last(self, active_task):
        time_delta = active_task.finish_time - active_task.start_time
        return str(datetime.timedelta(seconds=time_delta))

    def _time_active_today(self):
        pass
