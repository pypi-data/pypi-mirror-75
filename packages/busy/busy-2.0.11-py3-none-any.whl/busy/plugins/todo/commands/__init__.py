from busy.commander import Command
import busy.plugins.todo


class TodoCommand(Command):

    def execute(self, parsed):
        return self.execute_todo(parsed, self._root.get_queue(busy.plugins.todo.TodoQueue.key))

    def execute_todo(self, parsed, queue):  # pragma: no cover
        pass


