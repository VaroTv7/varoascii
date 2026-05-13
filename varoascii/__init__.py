"""VaroASCII — Motor de efectos visuales y arte ASCII para terminal.

This package provides terminal text effects, ASCII art generation,
and color themes for creating stunning terminal animations.

Quick Start:
    >>> import varoascii
    >>> varoascii.render("Hello World", effect="rain")
    >>> varoascii.render("VaroASCII", effect="glitch", theme="cyberpunk")
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


def render(
    text: str,
    effect: str = "print",
    theme: str | None = None,
    font: str | None = None,
) -> None:
    """Render text with a terminal effect — high-level convenience function.

    This is the simplest way to use VaroASCII programmatically.

    Args:
        text: The text to animate.
        effect: Name of the effect to apply (e.g. "rain", "matrix", "glitch", "typewriter").
        theme: Optional color theme name (e.g. "cyberpunk", "retrowave", "fire").
        font: Optional FIGlet font name. If provided, the text is first converted to ASCII art.

    Example:
        >>> import varoascii
        >>> varoascii.render("Hello!", effect="glitch", theme="cyberpunk")
    """
    import importlib
    import pkgutil

    import varoascii.effects
    from varoascii.engine.terminal import TerminalConfig
    from varoascii.themes import get_theme

    # If a font is specified, generate ASCII art first
    if font:
        from varoascii.effects.effect_ascii import _load_font
        figlet = _load_font(font)
        text = figlet.renderText(text.strip())

    # Discover effects
    effect_map = {}
    for module_info in pkgutil.iter_modules(
        varoascii.effects.__path__,
        varoascii.effects.__name__ + ".",
    ):
        module = importlib.import_module(module_info.name)
        if hasattr(module, "get_effect_resources"):
            cmd, effect_cls, config_cls = module.get_effect_resources()
            effect_map[cmd] = (effect_cls, config_cls)

    if effect not in effect_map:
        available = ", ".join(sorted(effect_map.keys()))
        msg = f"Effect '{effect}' not found. Available: {available}"
        raise ValueError(msg)

    effect_cls, config_cls = effect_map[effect]
    terminal_config = TerminalConfig._build_config()
    effect_config = config_cls._build_config()

    # Apply theme
    if theme:
        theme_colors = get_theme(theme)
        if hasattr(effect_config, "final_gradient_stops"):
            effect_config.final_gradient_stops = theme_colors

    effect_instance = effect_cls(text, effect_config, terminal_config)
    with effect_instance.terminal_output() as terminal:
        for frame in effect_instance:
            terminal.print(frame)
