from Command import Command
from commands import commands

class CommandManager:
    def __init__(self):
        self.cache = {}

        for command in commands:
            self.cache[command.name] = command
    
    def add_command(self, command):
        name = command["name"]
        callback = command["callback"]
        self.cache[name] = Command(name, callback)
    
    def get(self, name):
        return self.cache[name]