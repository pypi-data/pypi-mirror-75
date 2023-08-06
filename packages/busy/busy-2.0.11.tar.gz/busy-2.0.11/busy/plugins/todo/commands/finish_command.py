from busy.commander import Commander
from . import TodoCommand


class FinishCommand(TodoCommand):

    command = 'finish'

    @classmethod
    def register(self, parser):
        parser.add_argument('--yes', action='store_true')

    def execute_todo(self, parsed, queue):
        tasklist = queue.list(*parsed.criteria or [1])
        indices = [i[0]-1 for i in tasklist]
        if self.is_confirmed(parsed, tasklist, 'Finish', 'Finishing'):
            queue.finish(*indices)


Commander.register(FinishCommand)


