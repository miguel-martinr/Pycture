from .edit_commands import EditBrightnessCommand
from .file_commands import OpenFileCommand, SaveFileCommand
from .command import Command


file_commands = [OpenFileCommand, SaveFileCommand]
edit_commands = [EditBrightnessCommand]