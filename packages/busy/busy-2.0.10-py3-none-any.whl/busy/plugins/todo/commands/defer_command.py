from busy import dateparser

from busy.commander import Commander
from . import TodoCommand


class DeferCommand(TodoCommand):

    command = 'defer'

    @classmethod
    def register(self, parser):
        parser.add_argument('--to', '--for', dest='time_info')

    def execute_todo(self, parsed, queue):
        tasklist = queue.list(*parsed.criteria or [1])
        # indices = [i[0]-1 for i in tasklist]
        if hasattr(parsed, 'time_info') and parsed.time_info:
            time_info = parsed.time_info
        else:
            print('\n'.join([str(i[1]) for i in tasklist]))
            time_info = input('Defer to [tomorrow]: ').strip() or 'tomorrow'
        queue.defer(dateparser.relative_date(time_info), *parsed.criteria)


Commander.register(DeferCommand)


