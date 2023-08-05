from busy.commander import Commander
from . import TodoCommand


class ResourceCommand(TodoCommand):

    command = "resource"

    def execute_todo(self, parsed, queue):
        if parsed.criteria:  # pragma: nocover
            message = ("The `resource` command only returns the top item - "
                       "repeat without criteria")
            raise RuntimeError(message)
        else:
            return str(queue.resource() or '')


Commander.register(ResourceCommand)


