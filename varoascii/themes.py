"""Color themes for VaroASCII effects.

Provides predefined color palettes that can be applied to any effect
via the --theme CLI argument or programmatic API.

Each theme is a tuple of Color stops designed to create a cohesive
visual aesthetic when used as gradient stops.
"""

from varoascii.utils.graphics import Color

# Predefined color themes
THEMES: dict[str, tuple[Color, ...]] = {
    "cyberpunk": (
        Color("ff00ff"),  # magenta
        Color("00ffff"),  # cyan
        Color("ff0080"),  # hot pink
    ),
    "retrowave": (
        Color("ff6ec7"),  # neon pink
        Color("7b68ee"),  # medium slate blue
        Color("00ced1"),  # dark turquoise
    ),
    "matrix": (
        Color("00ff41"),  # matrix green
        Color("008f11"),  # dark green
        Color("003b00"),  # deep green
    ),
    "fire": (
        Color("ff4500"),  # orange-red
        Color("ff8c00"),  # dark orange
        Color("ffd700"),  # gold
    ),
    "ocean": (
        Color("006994"),  # sea blue
        Color("00bfff"),  # deep sky blue
        Color("40e0d0"),  # turquoise
    ),
    "sunset": (
        Color("ff6b6b"),  # coral
        Color("ffa07a"),  # light salmon
        Color("ffd93d"),  # saffron
    ),
    "arctic": (
        Color("e0f7fa"),  # ice white
        Color("80deea"),  # light cyan
        Color("4dd0e1"),  # medium cyan
    ),
    "lava": (
        Color("ff0000"),  # red
        Color("ff4500"),  # orange-red
        Color("8b0000"),  # dark red
    ),
    "neon": (
        Color("39ff14"),  # neon green
        Color("ff073a"),  # neon red
        Color("0ff0fc"),  # neon cyan
    ),
    "gold": (
        Color("ffd700"),  # gold
        Color("daa520"),  # goldenrod
        Color("b8860b"),  # dark goldenrod
    ),
}


def get_theme_names() -> list[str]:
    """Return a sorted list of available theme names."""
    return sorted(THEMES.keys())


def get_theme(name: str) -> tuple[Color, ...]:
    """Get a theme by name.

    Args:
        name: Theme name (case-insensitive).

    Returns:
        tuple[Color, ...]: Color stops for the theme.

    Raises:
        KeyError: If the theme name is not found.
    """
    key = name.lower()
    if key not in THEMES:
        available = ", ".join(get_theme_names())
        msg = f"Theme '{name}' not found. Available themes: {available}"
        raise KeyError(msg)
    return THEMES[key]
