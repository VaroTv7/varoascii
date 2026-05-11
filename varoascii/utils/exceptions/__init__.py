"""varoascii exceptions module."""

from varoascii.utils.exceptions.animation_exceptions import (
    ActivateEmptySceneError,
    AnimationSceneError,
    FrameDurationError,
    SceneNotFoundError,
)
from varoascii.utils.exceptions.base_character_exceptions import (
    DuplicateEventRegistrationError,
    EventRegistrationCallerError,
    EventRegistrationTargetError,
)
from varoascii.utils.exceptions.motion_exceptions import (
    ActivateEmptyPathError,
    DuplicatePathIDError,
    DuplicateWaypointIDError,
    PathInvalidSpeedError,
    PathNotFoundError,
    WaypointNotFoundError,
)
from varoascii.utils.exceptions.terminal_exceptions import (
    InvalidCharacterGroupError,
    InvalidCharacterSortError,
    InvalidColorSortError,
    UnsupportedAnsiSequenceError,
)
