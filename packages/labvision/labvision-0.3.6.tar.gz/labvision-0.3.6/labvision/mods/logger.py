

class Logger():
    def __init__(self, fp=None):
        self.fp = fp

    def __call__(self, msg):
        print(msg)
        if self.fp is not None:
            with open(self.fp, 'a') as f:
                f.write(f'{msg}\n')
