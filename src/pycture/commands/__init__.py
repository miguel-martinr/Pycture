from .edit_commands import EditBrightnessCommand
from .file_commands import OpenFileCommand, SaveFileCommand
from .view_commands import ViewHistogramCommand
from .command import Command


file_commands_list = [OpenFileCommand, SaveFileCommand]
edit_commands_list = [EditBrightnessCommand]
view_commands_list = [ViewHistogramCommand]