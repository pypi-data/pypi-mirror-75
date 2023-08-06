import re

from ...queue import Queue
from ...item import Item
from ...commander import Command
from ...commander import Commander
from busy import dateparser
from .commands import TodoCommand

MARKER = re.compile(r'\s*\-*\>\s*')
REPEAT = re.compile(r'^\s*repeat(?:\s+[io]n)?\s+(.+)\s*$', re.I)
RESOURCE = re.compile(r'\s+at\s+(\S+)')


class Task(Item):

    def __init__(self, description=None):
        super().__init__(description)

    def as_plan(self, date):
        return Plan(self.description, date)

    def as_done(self, date):
        return DoneTask(self._marker_split[0], date)

    def as_followon(self):
        if len(self._marker_split) > 1:
            description = self._marker_split[1]
            if not REPEAT.match(description):
                return Task(description)

    def as_repeat(self):
        if len(self._marker_split) > 1:
            match = REPEAT.match(self._marker_split[1])
            if match:
                date = dateparser.relative_date(match.group(1))
                return Plan(self.description, date)

    @property
    def project(self):
        tags = self.tags
        return tags[0] if tags else None

    @property
    def _marker_split(self):
        return MARKER.split(self.description, maxsplit=1)

    @property
    def resource(self):
        match = RESOURCE.search(self.description)
        if match:
            return match.group(1)
        else:
            return ""

    @property
    def without_resource(self):
        split = RESOURCE.split(self.description, maxsplit=1)
        if len(split) > 1:
            return split[0] + split[2]
        else:
            return self.description


class Plan(Item):

    schema = ['date', 'description']
    listfmt = "{1.date:%Y-%m-%d}  {1.description}"

    def __init__(self, description=None, date=None):
        super().__init__(description)
        self._date = dateparser.absolute_date(date)

    @property
    def date(self):
        return self._date

    def as_todo(self):
        return Task(self.description)


class DoneTask(Item):

    schema = ['date', 'description']
    listfmt = "{1.date:%Y-%m-%d}  {1.description}"

    def __init__(self, description=None, date=None):
        super().__init__(description)
        self._date = dateparser.absolute_date(date)

    @property
    def date(self):
        return self._date


def is_today_or_earlier(plan):
    return plan.date <= dateparser.today()


class TodoQueue(Queue):
    itemclass = Task
    key = 'tasks'

    def __init__(self, manager=None, items=[]):
        super().__init__(manager, items)
        self._plans = None
        self._done = None

    @property
    def plans(self):
        if not self._plans:
            if self.manager:
                self._plans = self.manager.get_queue(PlanQueue.key)
            else:
                self._plans = PlanQueue()
        return self._plans

    @property
    def done(self):
        if not self._done:
            if self.manager:
                self._done = self.manager.get_queue('done')
            else:
                self._done = DoneQueue()
        return self._done

    def defer(self, date, *criteria):
        indices = self.select(*(criteria or [1]))
        plans = [self.get(i+1).as_plan(date) for i in indices]
        self.plans.add(*plans)
        self.delete_by_indices(*indices)

    def activate(self, *criteria, today=False):
        if today:
            indices = self.plans.select(is_today_or_earlier)
        elif criteria:
            indices = self.plans.select(*criteria)
        else:
            return
        tasks = [self.plans.get(i+1).as_todo() for i in indices]
        self.add(*tasks, index=0)
        self.plans.delete_by_indices(*indices)

    def finish(self, *indices, date=None):
        if not date:
            date = dateparser.today()
        donelist, keeplist = self._split_by_indices(*indices)
        self._items = keeplist
        self.done.add(*[t.as_done(date) for t in donelist])
        self.add(*filter(None, [t.as_followon() for t in donelist]))
        self.plans.add(*filter(None, [t.as_repeat() for t in donelist]))

    def resource(self, index=1):
        return self._items[index-1].resource if self._items else None

    def get_without_resource(self, index=1):
        return self._items[index-1].without_resource if self._items else None


Queue.register(TodoQueue, default=True)


class PlanQueue(Queue):
    itemclass = Plan
    key = 'plans'


Queue.register(PlanQueue)


class DoneQueue(Queue):
    itemclass = DoneTask
    key = 'done'


Queue.register(DoneQueue)
