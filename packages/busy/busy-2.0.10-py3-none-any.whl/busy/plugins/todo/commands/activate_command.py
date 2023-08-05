from busy.commander import Commander
from . import TodoCommand


class ActivateCommand(TodoCommand):

    command = 'activate'

    @classmethod
    def register(self, parser):
        parser.add_argument('--today', '-t', action='store_true')

    def execute_todo(self, parsed, queue):
        if hasattr(parsed, 'today') and parsed.today:
            queue.activate(today=True)
        else:
            queue.activate(*parsed.criteria)


Commander.register(ActivateCommand)


