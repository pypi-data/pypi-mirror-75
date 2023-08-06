# Load dependencies
import ovito.modifiers.stdobj

# Load the native code modules.
from ovito.plugins.TimeAveragingPython import TimeAveragingModifier

# Inject modifier classes into parent module.
ovito.modifiers.TimeAveragingModifier = TimeAveragingModifier
ovito.modifiers.__all__ += ['TimeAveragingModifier']
