from pycture.commands.edit_commands.edit_brightness_and_contrast import EditBrightnessAndContrast
from pycture.commands.edit_commands.gamma_correction import GammaCorrection
from .edit_commands import (EditBrightnessAndContrast, ConvertToGrayScale,
                            TransformByLinearSegments, EqualizeRed,
                            EqualizeGreen, EqualizeBlue, EqualizeRGB,
                            SpecifyHistogram)
from .file_commands import OpenFile, SaveFile
from .view_commands import (ViewRedHistogram, ViewGreenHistogram, ViewBlueHistogram,
                            ViewGrayScaleHistogram, ViewCumulativeRedHistogram,
                            ViewCumulativeGreenHistogram, ViewCumulativeBlueHistogram,
                            ViewCumulativeGrayScaleHistogram, ViewImageBrightness,
                            ViewImageSize, ViewImageContrast, ViewImageEntropy,
                            ViewImageRanges, ViewDifference)

from .help_commands import ShowHelp
from .command import Command


view_command_list = [ViewDifference]
file_command_list = [OpenFile, SaveFile]
edit_command_list = [
    ConvertToGrayScale,
    TransformByLinearSegments,
    EditBrightnessAndContrast,
    SpecifyHistogram,
    GammaCorrection]
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
