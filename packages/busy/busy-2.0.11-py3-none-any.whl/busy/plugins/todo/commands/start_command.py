from busy.commander import Commander
from . import TodoCommand
from ....commands.manage_command import text_editor


class StartCommand(TodoCommand):

    command = 'start'

    @classmethod
    def register(self, parser):
        parser.add_argument('project', action='store', nargs='?')

    def execute_todo(self, parsed, queue):
        if parsed.criteria:
            raise RuntimeError('Start takes only an optional project name')
        queue.activate(today=True)
        if queue.count() < 1:
            raise RuntimeError('There are no active tasks')
        project = parsed.project or queue.get().project
        if not project:
            raise RuntimeError('The `start` command required a project')
        queue.manage(project, editor=text_editor)
        queue.pop(project)


Commander.register(StartCommand)
