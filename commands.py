import logging


class Command:
    def __init__(self, command_name: str, permission: int):
        self.command_name = command_name
        self.permission = permission

    def execute(self):
        pass


class CommandManager:
    def __init__(self):
        self.commands = []

    def add_command(self, command: Command):
        self.commands.append(command)
        logging.debug(f"added command: {command.command_name}")


def test_command_manager():
    c = CommandManager()
    cmd = Command("test", 1)
    c.add_command(cmd)


test_command_manager()
