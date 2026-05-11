"""Terminal Text Effects package.

This package provides various text effects for terminal applications.
"""

from varoascii.engine.animation import Animation, Scene
from varoascii.engine.base_character import EffectCharacter, EventHandler
from varoascii.engine.motion import (
    Motion,
    Path,
    Segment,
    Waypoint,
)
from varoascii.engine.terminal import Terminal
from varoascii.utils import easing, geometry, graphics
from varoascii.utils.geometry import Coord
from varoascii.utils.graphics import Color, ColorPair, Gradient

Event = EventHandler.Event
Action = EventHandler.Action
