"""Generates ASCII art from the input text using FIGlet fonts and reveals it.

Classes:
    Ascii: Generates ASCII art and reveals it.
    AsciiConfig: Configuration for the Ascii effect.
    AsciiIterator: Effect iterator for the Ascii effect.
"""

from __future__ import annotations

from dataclasses import dataclass
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


@dataclass
class AsciiConfig(BaseConfig):
    """Configuration for the Ascii effect."""

    parser_spec: argutils.ParserSpec = argutils.ParserSpec(
        name="ascii",
        help="Generates ASCII art from the input text and reveals it.",
        description="ascii | Generates ASCII art using FIGlet fonts and applies a reveal animation.",
        epilog="Example: varoascii ascii --font slant --final-gradient-stops 00ff00 --final-gradient-steps 12",
    )
    font: str = argutils.ArgSpec(
        name="--font",
        type=str,
        default="standard",
        help="FIGlet font to use for ASCII art generation.",
    )  # pyright: ignore[reportAssignmentType]
    
    list_fonts: bool = argutils.ArgSpec(
        name="--list-fonts",
        action="store_true",
        default=False,
        help="List available FIGlet fonts and exit.",
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_stops: tuple[Color, ...] = FinalGradientStopsArg(
        default=(Color("#00ff00"), Color("#008800")),
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_steps: tuple[int, ...] | int = FinalGradientStepsArg(
        default=12,
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_direction: Gradient.Direction = FinalGradientDirectionArg(
        default=Gradient.Direction.VERTICAL,
    )  # pyright: ignore[reportAssignmentType]


class AsciiIterator(BaseEffectIterator[AsciiConfig]):
    """Effect iterator for the Ascii effect."""

    def __init__(self, effect: Ascii) -> None:
        super().__init__(effect)
        self.active_characters.clear()
        self.build()

    def build(self) -> None:
        final_gradient = Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.canvas.text_bottom,
            self.terminal.canvas.text_top,
            self.terminal.canvas.text_left,
            self.terminal.canvas.text_right,
            self.config.final_gradient_direction,
        )

        for character in self.terminal.get_characters():
            color = final_gradient_mapping.get(character.input_coord, Color("#ffffff"))
            character.animation.set_appearance(character.input_symbol, ColorPair(fg=color))
            self.terminal.set_character_visibility(character, is_visible=True)

    def __next__(self) -> str:
        if self.active_characters:
            self.update()
            return self.frame
        
        # In this simple version, we just show it immediately and then stop.
        # We could add more complex animation later.
        if not hasattr(self, "_done"):
            self._done = True
            return self.frame
        raise StopIteration


class Ascii(BaseEffect[AsciiConfig]):
    """Generates ASCII art and reveals it."""

    def __init__(
        self,
        input_data: str,
        effect_config: AsciiConfig | None = None,
        terminal_config: TerminalConfig | None = None,
    ) -> None:
        config = effect_config or AsciiConfig._build_config()
        
        if config.list_fonts:
            print("\n".join(FigletFont.getFonts()))
            import sys
            sys.exit(0)

        # Try to find the font in the local fonts directory
        import os
        from pathlib import Path
        from pyfiglet import Figlet, FigletFont
        
        font_name = config.font
        
        # Determine the font to use
        try:
            f = Figlet(font=font_name)
        except:
            # Fallback to standard if font not found in pyfiglet's internal list
            # We could implement a custom loader here for .flf files in the future
            f = Figlet(font="standard")
        
        ascii_text = f.renderText(input_data.strip())
        super().__init__(ascii_text, config, terminal_config)

    @property
    def _config_cls(self) -> type[AsciiConfig]:
        return AsciiConfig

    @property
    def _iterator_cls(self) -> type[AsciiIterator]:
        return AsciiIterator
