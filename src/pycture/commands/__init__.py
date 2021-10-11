from .edit_commands import EditBrightnessCommand
from .file_commands import OpenFileCommand, SaveFileCommand
from .view_commands import ViewHistogramCommand
from .command import Command


file_commands_list = [OpenFileCommand, SaveFileCommand]
edit_commands_list = [EditBrightnessCommand]
red_view_commands_list = [ViewHistogramCommand]
green_view_commands_list = [ViewHistogramCommand]
blue_view_commands_list = [ViewHistogramCommand]
gray_view_commands_list = [ViewHistogramCommand]