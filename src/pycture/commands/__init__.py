from .edit_commands import *
from .file_commands import OpenFile, SaveFile
from .view_commands import *

from .help_commands import ShowHelp
from .command import Command


view_command_list = [ViewDifference, ViewMapOfChanges]
file_command_list = [OpenFile, SaveFile]
edit_command_list = [
    ConvertToGrayScale,
    TransformByLinearSegments,
    EditBrightnessAndContrast,
    SpecifyHistogram,
    GammaCorrection,
    Rotate,
    Scale,
    VerticalMirror,
    HorizontalMirror,
    Transpose,
    RotateClockwise,
    RotateSimple]
equalize_command_list = [EqualizeRed, EqualizeGreen, EqualizeBlue, EqualizeRGB]
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
