from datetime import time, datetime


class Observable(object):
    def __init__(self):
        self.observers = set()

    def add_observer(self, observer):
        self.observers.add(observer)

    def notify(self, event, p_event=None):
        if p_event:
            p_event.add_sub_events(event)
            return

        for observer in self.observers:
            observer.update(event)


class ObserverMixin(object):
    def update(self, event):
        pass


class CircularQueue(object):
    def __init__(self, priority_fn):
        self.queue = []
        self.head = 0
        self.priority_fn = priority_fn

    def peek(self, plus=0):
        if len(self.queue) == 0:
            return None
        index = (self.head + plus) % len(self.queue)
        return self.queue[index]

    def next(self):
        self.head = (self.head + 1) % len(self.queue)

    def __call__(self, *args, **kwargs):
        self.next()
        current = self.peek()
        return current

    def __iter__(self):
        limit = len(self.queue)
        for i in range(limit):
            yield self()

    def list_in_order(self):
        return iter(self.queue)

    def __len__(self):
        return len(self.queue)

    def add(self, obj):
        # No need to be efficient, should not be called often
        current = self.peek()
        self.queue.append(obj)
        self.queue.sort(key=self.priority_fn, reverse=True)
        for i, el in enumerate(self.queue):
            if el is current:
                self.head = i
                break

    def reset_head(self):
        self.head = len(self.queue) - 1

    def is_first(self):
        return self.head == 0


class Clock(object):
    def __init__(self):
        self.records = []

    def new_laps(self, event):
        self.records.append((datetime.now(), event))
        return self

    def start(self, event):
        return self.new_laps(event)

    def end(self, event):
        return self.new_laps(event)

    def __iter__(self):
        if len(self.records) == 0:
            raise StopIteration()
        start, curr_event = self.records[0]
        for end, next_event in self.records[1:]:
            delta = end - start
            yield delta, curr_event
            curr_event = next_event

    def total_duration(self):
        if len(self.records) < 2:
            return None
        return self.records[-1][0] - self.records[0][0]



