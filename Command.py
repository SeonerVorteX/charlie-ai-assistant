class Command:
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback
    
    def execute(self, args):
        self.callback(args)