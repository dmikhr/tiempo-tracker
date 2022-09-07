import argparse
from time_tracker.time_tracker import TimeTracker

# help flag provides flag help
# store_true actions stores argument as True

class Cli:
    def __init__(self):
        self.time_tracker = TimeTracker()
        self.methods_map = {'start': lambda task_name: self.time_tracker.task_start(task_name),
                            'add': lambda task_name: self.time_tracker.task_add(task_name),
                            'finish': lambda task_name: self.time_tracker.task_finish(),
                            'remove': lambda task_name: self.time_tracker.task_remove(task_name),
                            }
        self.parser = argparse.ArgumentParser()
        self._setup_arguments()
        self.args = vars(self.parser.parse_args())
        self._run()

    def _run(self):
        # pass
        # no_arg = True
        for arg_name, method_name in self.methods_map.items():
            if self.args.get(arg_name):
                print(f'calling with {arg_name}')
                # if self.args[arg_name] get
                # else response = method_name()
                response = method_name(self.args[arg_name])
                if response:
                    print(response)
                # no_arg = False
                break
        # if no_arg:
        #     print('Unknown parameter. Use --help to see available options')

    def _setup_arguments(self):
        self.parser.add_argument('-s', '--start',
                            help='Start task by providing its name')
        # flag without value
        self.parser.add_argument('-f', '--finish', action='store_true',
                            help='Finish current task.\
                                 Task also can be finished\
                                 by starting a different task')
        self.parser.add_argument('-a', '--add',
                            help='Add new task')
        self.parser.add_argument('-r', '--remove',
                            help='Remove the task')
        self.parser.add_argument('-l', '--list',
                            help='List of all tasks')
        self.parser.add_argument('-st', '--stats',
                            help='Stats about task')


def main():
    Cli()

if __name__ == '__main__':
    main()
