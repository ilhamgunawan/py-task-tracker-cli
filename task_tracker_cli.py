import cmd
from task_tracker import TaskTracker
import shlex

class TaskTrackerCli(cmd.Cmd):
    intro = "Welcome to task tracker CLI."
    prompt = "task-cli > "
    _service = TaskTracker

    def __init__(self):
        super().__init__()
        self._service = TaskTracker()

    def emptyline(self):
        pass

    def onecmd(self, line):
        # This is to convert "-" to "_" from the command line
        commands = line.split(" ", 1)
        command = commands[0].replace("-", "_")
        arguments = commands[1] if len(commands) > 1 else ""
        return super().onecmd(f"{command} {arguments}")

    def do_add(self, arg):
        args = shlex.split(arg)
        if len(args) < 1:
            print("Insufficient command.")
            return
        description = args[0]
        self._service.create_task(description)

    def do_update(self, arg):
        try:
            args = shlex.split(arg)
            if len(args) < 2:
                print("Insufficient command.")
                return
            _id = int(args[0])
            _description = args[1]
            self._service.update_task(int(_id), _description, None)
        except ValueError as e:
            print(f"Error parsing argument: {e}")

    def do_delete(self, arg):
        try:
            args = shlex.split(arg)
            if len(args) < 1:
                print("Insufficient command.")
                return
            _id = int(args[0])
            self._service.delete_task(int(_id))
        except ValueError as e:
            print(f"Error parsing argument: {e}")

    def do_mark_in_progress(self, arg):
        try:
            args = shlex.split(arg)
            if len(args) < 1:
                print("Insufficient command.")
                return
            _id = int(args[0])
            self._service.update_task(int(_id), None, "in-progress")
        except ValueError as e:
            print(f"Error parsing argument: {e}")

    def do_mark_done(self, arg):
        try:
            args = shlex.split(arg)
            if len(args) < 1:
                print("Insufficient command.")
                return
            _id = int(args[0])
            self._service.update_task(int(_id), None, "done")
        except ValueError as e:
            print(f"Error parsing argument: {e}")

    def do_list(self, arg):
        args = shlex.split(arg)
        if len(args) < 1:
            self._service.list_all_tasks()
        else:
            self._service.list_by_status(args[0])

    def do_exit(self, arg):
        """Exit task tracker CLI."""
        return True

    def __parse_command(self, _arg, _cmd_word_count: int):
        args = shlex.split(_arg)
        if len(args) < _cmd_word_count:
            raise Exception("Insufficient command.")