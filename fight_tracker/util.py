class Observable(object):
    def __init__(self):
        self.observers = set()

    def add_observer(self, observer):
        self.observers.add(observer)

    def notify(self, event):
        for observer in self.observers:
            observer.update(event)

    def notify_trigger(self, event):
        self.notify(event)
        event()


class ObserverMixin(object):
    def update(self, event):
        pass


class CircularQueue(object):
    def __init__(self, priority_fn):
        self.queue = []
        self.head = 0
        self.priority_fn = priority_fn

    def peek(self):
        if len(self.queue) == 0:
            return None
        return self.queue[self.head]

    def next(self):
        self.head = (self.head + 1) % len(self.queue)

    def __call__(self, *args, **kwargs):
        current = self.peek()
        self.next()
        return current

    def __iter__(self):
        limit = len(self.queue)
        for i in range(limit):
            yield self()

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
        self.head = 0

    def is_first(self):
        return self.head == 0