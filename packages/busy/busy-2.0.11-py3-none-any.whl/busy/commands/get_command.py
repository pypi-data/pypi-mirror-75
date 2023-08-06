from ..commander import QueueCommand
from ..commander import Commander
from ..ui.get_item_ui import GetItemUi


class GetCommand(QueueCommand):

    command = 'get'

    @classmethod
    def register(self, parser):
        super().register(parser)
        parser.add_argument('--interactive', action='store_true')

    def execute_on_queue(self, parsed, queue):
        if parsed.criteria:
            message = ("The `get` command only returns the top item - "
                       "repeat without criteria")
            raise RuntimeError(message)
        else:
            value = str(queue.get() or '')
            if parsed.interactive:  # pragma: no cover
                frame = GetItemUi(value)
            else:
                return value


Commander.register(GetCommand)
