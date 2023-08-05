from .pool import Pool


class Todo(object):
    def __init__(self, commands):
        self._commands = commands

    def execute(self, command):
        return command.execute()

    def process(self):
        self._in_progress()
        self._done()
        return getattr(self, 'response')

    def _in_progress(self):
        with Pool() as pool:
            response = pool.map(self.execute, self._commands)
        setattr(self, 'response', response)

    def _done(self):
        response = getattr(self, 'response')
        if not response:
            raise RuntimeError('work muss progress before calling done')
