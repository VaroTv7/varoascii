"""Hack effect — Hollywood-style hacking animation.

A VaroASCII original effect. Columns of binary/hex data rain down
the screen, then progressively resolve into the actual message,
simulating a movie-style computer breach sequence.

Classes:
    Hack: Hollywood hacking reveal effect.
    HackConfig: Configuration for the Hack effect.
    HackIterator: Iterates over the Hack effect.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from varoascii import Color, ColorPair, EffectCharacter, Gradient
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
    return "hack", Hack, HackConfig


_BINARY_CHARS = list("01")
_HEX_CHARS = list("0123456789ABCDEF")
_HACK_SYMBOLS = list("█▓▒░╔╗╚╝║═┃━┏┓┗┛│─┌┐└┘")
_CODE_COLORS = [
    Color("00ff41"),  # green
    Color("00cc33"),  # dark green
    Color("009922"),  # deeper green
    Color("33ff66"),  # light green
]


@dataclass
class HackConfig(BaseConfig):
    """Configuration for the Hack effect.

    Attributes:
        scramble_duration: Frames of binary/hex scrambling before text resolves.
        resolve_speed: Characters that resolve to real text per frame.
        code_style: Style of scrambling characters (binary, hex, or mixed).
        final_gradient_stops: Colors for the resolved text.
        final_gradient_steps: Gradient steps.
        final_gradient_direction: Gradient direction.
    """

    parser_spec: argutils.ParserSpec = argutils.ParserSpec(
        name="hack",
        help="Hollywood-style hacking animation. VaroASCII original.",
        description="hack | Binary/hex data resolves into text like a movie hack scene. VaroASCII original.",
        epilog="Example: varoascii hack --scramble-duration 40 --code-style hex",
    )

    scramble_duration: int = argutils.ArgSpec(
        name="--scramble-duration",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=35,
        help="Frames of binary/hex scrambling before characters begin resolving.",
    )  # pyright: ignore[reportAssignmentType]

    resolve_speed: int = argutils.ArgSpec(
        name="--resolve-speed",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=2,
        help="Characters that resolve to real text per frame.",
    )  # pyright: ignore[reportAssignmentType]

    code_style: str = argutils.ArgSpec(
        name="--code-style",
        type=str,
        default="mixed",
        choices=["binary", "hex", "mixed"],
        help="Style of scrambling characters: binary (0/1), hex (0-F), or mixed.",
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_stops: tuple[Color, ...] = FinalGradientStopsArg(
        default=(Color("00ff41"), Color("00ffff")),
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_steps: tuple[int, ...] | int = FinalGradientStepsArg(
        default=12,
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_direction: Gradient.Direction = FinalGradientDirectionArg(
        default=Gradient.Direction.VERTICAL,
    )  # pyright: ignore[reportAssignmentType]


class HackIterator(BaseEffectIterator[HackConfig]):
    """Iterator for the Hack effect.

    Phases:
        1. scramble: All characters show random binary/hex data.
        2. resolve: Characters progressively reveal the real text.
        3. flash: Brief white flash when all text is revealed.
        4. done: Final stable display.
    """

    def __init__(self, effect: Hack) -> None:
        super().__init__(effect)
        self.phase = "scramble"
        self.frame_count = 0
        self.unresolved: list[EffectCharacter] = []
        self.character_final_colors: dict[EffectCharacter, Color] = {}
        self.build()

    def _get_scramble_char(self) -> str:
        """Get a random scramble character based on code style."""
        if self.config.code_style == "binary":
            return random.choice(_BINARY_CHARS)
        elif self.config.code_style == "hex":
            return random.choice(_HEX_CHARS)
        else:  # mixed
            pool = _BINARY_CHARS + _HEX_CHARS + _HACK_SYMBOLS
            return random.choice(pool)

    def build(self) -> None:
        """Build gradient and show all chars as scrambled data."""
        final_gradient = Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.canvas.text_bottom,
            self.terminal.canvas.text_top,
            self.terminal.canvas.text_left,
            self.terminal.canvas.text_right,
            self.config.final_gradient_direction,
        )

        all_chars = list(self.terminal.get_characters())

        for character in all_chars:
            self.character_final_colors[character] = final_gradient_mapping.get(
                character.input_coord, Color("ffffff")
            )
            # Start with scrambled code
            symbol = self._get_scramble_char()
            color = random.choice(_CODE_COLORS)
            character.animation.set_appearance(symbol, ColorPair(fg=color))
            self.terminal.set_character_visibility(character, is_visible=True)

        # Resolve order: column by column (left to right) for cinematic feel
        all_chars.sort(key=lambda c: (c.input_coord.column, -c.input_coord.row))
        self.unresolved = all_chars

    def __next__(self) -> str:
        if self.phase == "scramble":
            self.frame_count += 1

            # Continuously scramble all characters
            for character in self.unresolved:
                if random.randint(1, 100) <= 70:
                    symbol = self._get_scramble_char()
                    color = random.choice(_CODE_COLORS)
                    character.animation.set_appearance(symbol, ColorPair(fg=color))

            if self.frame_count >= self.config.scramble_duration:
                self.phase = "resolve"

            return self.frame

        if self.phase == "resolve":
            if self.unresolved:
                batch = self.unresolved[:self.config.resolve_speed]
                self.unresolved = self.unresolved[len(batch):]

                for character in batch:
                    # Brief "discovery" flash — white before final color
                    final_color = self.character_final_colors[character]
                    character.animation.set_appearance(
                        character.input_symbol, ColorPair(fg=Color("ffffff"))
                    )

                # Still-scrambling chars keep changing
                for character in self.unresolved:
                    if random.randint(1, 100) <= 40:
                        symbol = self._get_scramble_char()
                        color = random.choice(_CODE_COLORS)
                        character.animation.set_appearance(symbol, ColorPair(fg=color))

                return self.frame

            # All resolved — apply final colors
            self.phase = "colorize"
            self._colorize_frame = 0
            return self.frame

        if self.phase == "colorize":
            self._colorize_frame += 1
            all_chars = list(self.terminal.get_characters())

            if self._colorize_frame == 1:
                # Flash frame — all white
                for character in all_chars:
                    character.animation.set_appearance(
                        character.input_symbol, ColorPair(fg=Color("ffffff"))
                    )
                return self.frame
            elif self._colorize_frame == 2:
                # Apply final gradient colors
                for character in all_chars:
                    final_color = self.character_final_colors[character]
                    character.animation.set_appearance(
                        character.input_symbol, ColorPair(fg=final_color)
                    )
                return self.frame
            else:
                self.phase = "done"

        if self.phase == "done":
            if not hasattr(self, "_done"):
                self._done = True
                return self.frame
            raise StopIteration

        raise StopIteration


class Hack(BaseEffect[HackConfig]):
    """Hollywood-style hacking animation.

    A VaroASCII original effect. Characters display as scrolling binary/hex
    code that progressively resolves into the real message, with a final
    flash when the "breach" is complete. Supports binary, hex, and mixed modes.
    """

    @property
    def _config_cls(self) -> type[HackConfig]:
        return HackConfig

    @property
    def _iterator_cls(self) -> type[HackIterator]:
        return HackIterator
