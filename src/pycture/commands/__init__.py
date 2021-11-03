from .edit_commands import EditBrightness, ConvertToGrayScale, TransformByLinearSegments
from .file_commands import OpenFile, SaveFile
from .view_commands import (ViewRedHistogram, ViewGreenHistogram, ViewBlueHistogram,
                            ViewGrayScaleHistogram, ViewCumulativeRedHistogram,
                            ViewCumulativeGreenHistogram, ViewCumulativeBlueHistogram,
                            ViewCumulativeGrayScaleHistogram, ViewImageBrightness,
                            ViewImageSize, ViewImageContrast, ViewImageEntropy,
                            ViewImageRanges)

from .help_commands import ShowHelp
from .command import Command


file_command_list = [OpenFile, SaveFile]
edit_command_list = [
    EditBrightness,
    ConvertToGrayScale,
    TransformByLinearSegments]
histogram_command_list = [
    ViewRedHistogram,
    ViewGreenHistogram,
    ViewBlueHistogram,
    ViewGrayScaleHistogram]
cumulative_histogram_command_list = [
    ViewCumulativeRedHistogram,
    ViewCumulativeGreenHistogram,
    ViewCumulativeBlueHistogram,
    ViewCumulativeGrayScaleHistogram]
info_command_list = [
    ViewImageBrightness,
    ViewImageSize,
    ViewImageContrast,
    ViewImageEntropy,
    ViewImageRanges]
help_command_list = [ShowHelp]
