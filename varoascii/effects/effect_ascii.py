"""Generates ASCII art from the input text using FIGlet fonts and reveals it progressively.

Classes:
    Ascii: Generates ASCII art and reveals it with animation.
    AsciiConfig: Configuration for the Ascii effect.
    AsciiIterator: Effect iterator for the Ascii effect with progressive reveal.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from pyfiglet import Figlet, FigletFont

from varoascii import Color, ColorPair, Gradient
from varoascii.engine.base_config import (
    BaseConfig,
    FinalGradientDirectionArg,
    FinalGradientStepsArg,
    FinalGradientStopsArg,
)
from varoascii.engine.base_effect import BaseEffect, BaseEffectIterator
from varoascii.utils import argutils

if TYPE_CHECKING:
    from varoascii.engine.terminal import TerminalConfig


def get_effect_resources() -> tuple[str, type[BaseEffect], type[BaseConfig]]:
    """Get the command, effect class, and configuration class for the effect."""
    return "ascii", Ascii, AsciiConfig


def _get_local_fonts_dir() -> Path:
    """Return the path to the bundled fonts directory."""
    return Path(__file__).resolve().parent.parent / "fonts"


def _load_font(font_name: str) -> Figlet:
    """Load a FIGlet font, checking the local fonts directory first.

    Searches for .flf files in varoascii/fonts/ before falling back
    to pyfiglet's built-in font collection.

    Args:
        font_name: Name of the font to load.

    Returns:
        Figlet: A configured Figlet instance ready to render text.
    """
    local_dir = _get_local_fonts_dir()
    local_font_file = local_dir / f"{font_name}.flf"

    if local_font_file.exists():
        try:
            return Figlet(font=str(local_font_file))
        except Exception:
            pass

    # Try loading from pyfiglet's built-in fonts
    try:
        return Figlet(font=font_name)
    except Exception:
        return Figlet(font="standard")


def _list_available_fonts() -> list[str]:
    """List all available fonts (local + pyfiglet built-in).

    Returns:
        list[str]: Sorted list of font names.
    """
    fonts = set(FigletFont.getFonts())

    local_dir = _get_local_fonts_dir()
    if local_dir.exists():
        for flf_file in local_dir.glob("*.flf"):
            fonts.add(flf_file.stem)

    return sorted(fonts)


@dataclass
class AsciiConfig(BaseConfig):
    """Configuration for the Ascii effect."""

    parser_spec: argutils.ParserSpec = argutils.ParserSpec(
        name="ascii",
        help="Generates ASCII art from the input text and reveals it with animation.",
        description="ascii | Generates ASCII art using FIGlet fonts and reveals it progressively.",
        epilog="Example: varoascii ascii --font slant --reveal-mode row --final-gradient-stops 00ff00 --final-gradient-steps 12",
    )
    font: str = argutils.ArgSpec(
        name="--font",
        type=str,
        default="standard",
        help="FIGlet font to use for ASCII art generation. Use --list-fonts to see available fonts.",
    )  # pyright: ignore[reportAssignmentType]

    list_fonts: bool = argutils.ArgSpec(
        name="--list-fonts",
        action="store_true",
        default=False,
        help="List available FIGlet fonts (local + built-in) and exit.",
    )  # pyright: ignore[reportAssignmentType]

    reveal_mode: str = argutils.ArgSpec(
        name="--reveal-mode",
        type=str,
        default="row",
        choices=["row", "column", "random", "instant"],
        help="How to reveal the ASCII art: row (top-to-bottom), column (left-to-right), random, or instant.",
    )  # pyright: ignore[reportAssignmentType]

    reveal_speed: int = argutils.ArgSpec(
        name="--reveal-speed",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=3,
        help="Number of characters to reveal per frame. Higher = faster.",
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_stops: tuple[Color, ...] = FinalGradientStopsArg(
        default=(Color("00ff00"), Color("00aa00")),
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_steps: tuple[int, ...] | int = FinalGradientStepsArg(
        default=12,
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_direction: Gradient.Direction = FinalGradientDirectionArg(
        default=Gradient.Direction.VERTICAL,
    )  # pyright: ignore[reportAssignmentType]


class AsciiIterator(BaseEffectIterator[AsciiConfig]):
    """Effect iterator for the Ascii effect with progressive reveal animation."""

    def __init__(self, effect: Ascii) -> None:
        super().__init__(effect)
        self.pending: list = []
        self.build()

    def build(self) -> None:
        """Prepare the gradient mapping and the reveal order for characters."""
        final_gradient = Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.canvas.text_bottom,
            self.terminal.canvas.text_top,
            self.terminal.canvas.text_left,
            self.terminal.canvas.text_right,
            self.config.final_gradient_direction,
        )

        all_characters = list(self.terminal.get_characters())

        # Hide all characters initially (unless instant mode)
        for character in all_characters:
            self.terminal.set_character_visibility(character, is_visible=False)

        # Determine reveal order based on mode
        if self.config.reveal_mode == "row":
            # Reveal top-to-bottom (highest row first in the engine's coordinate system)
            all_characters.sort(key=lambda c: (-c.input_coord.row, c.input_coord.column))
        elif self.config.reveal_mode == "column":
            # Reveal left-to-right
            all_characters.sort(key=lambda c: (c.input_coord.column, -c.input_coord.row))
        elif self.config.reveal_mode == "random":
            random.shuffle(all_characters)
        # "instant" — reveal all at once (handled in __next__)

        # Store the color mapping for each character
        self._color_map = {}
        for character in all_characters:
            color = final_gradient_mapping.get(character.input_coord, Color("ffffff"))
            self._color_map[character] = color

        if self.config.reveal_mode == "instant":
            # Show everything at once
            for character in all_characters:
                color = self._color_map[character]
                character.animation.set_appearance(character.input_symbol, ColorPair(fg=color))
                self.terminal.set_character_visibility(character, is_visible=True)
            self.pending = []
        else:
            self.pending = all_characters

    def __next__(self) -> str:
        if self.pending:
            # Reveal a batch of characters per frame
            batch_size = self.config.reveal_speed
            batch = self.pending[:batch_size]
            self.pending = self.pending[batch_size:]

            for character in batch:
                color = self._color_map[character]
                character.animation.set_appearance(character.input_symbol, ColorPair(fg=color))
                self.terminal.set_character_visibility(character, is_visible=True)

            return self.frame

        # One final frame to ensure everything is rendered
        if not hasattr(self, "_done"):
            self._done = True
            return self.frame

        raise StopIteration


class Ascii(BaseEffect[AsciiConfig]):
    """Generates ASCII art from input text and reveals it with animation.

    Uses FIGlet fonts including custom fonts from the varoascii/fonts/ directory.
    Supports multiple reveal modes: row, column, random, and instant.
    """

    def __init__(
        self,
        input_data: str,
        effect_config: AsciiConfig | None = None,
        terminal_config: TerminalConfig | None = None,
    ) -> None:
        config = effect_config or AsciiConfig._build_config()

        if config.list_fonts:
            fonts = _list_available_fonts()
            local_dir = _get_local_fonts_dir()
            local_fonts = set()
            if local_dir.exists():
                local_fonts = {f.stem for f in local_dir.glob("*.flf")}

            print(f"Fuentes disponibles ({len(fonts)}):\n")
            for font in fonts:
                marker = " ⭐ [LOCAL]" if font in local_fonts else ""
                print(f"  {font}{marker}")
            print(f"\nFuentes locales en: {local_dir}")
            import sys
            sys.exit(0)

        figlet = _load_font(config.font)
        ascii_text = figlet.renderText(input_data.strip())
        super().__init__(ascii_text, config, terminal_config)

    @property
    def _config_cls(self) -> type[AsciiConfig]:
        return AsciiConfig

    @property
    def _iterator_cls(self) -> type[AsciiIterator]:
        return AsciiIterator
