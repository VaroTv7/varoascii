"""Glitch effect — text corrupts and repairs itself with digital distortion.

A VaroASCII original effect. Characters randomly glitch into corrupted symbols
with chromatic aberration colors, then progressively settle into their final form.

Classes:
    Glitch: Text corruption and repair effect.
    GlitchConfig: Configuration for the Glitch effect.
    GlitchIterator: Iterates over the Glitch effect.
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
    return "glitch", Glitch, GlitchConfig


# Glitch character sets
_GLITCH_CHARS = list("░▒▓█▄▀▐▌╌╍╎╏┆┇┊┋╳╱╲█▓▒░⣿⡿⠿⢿⣻⣽⣾⣷")
_GLITCH_COLORS = [
    Color("ff0040"),  # rojo glitch
    Color("00ff41"),  # verde matrix
    Color("00ffff"),  # cyan
    Color("ff00ff"),  # magenta
    Color("ffff00"),  # amarillo
    Color("ffffff"),  # blanco
]


@dataclass
class GlitchConfig(BaseConfig):
    """Configuration for the Glitch effect.

    Attributes:
        glitch_intensity: Probability (0-100) that a character glitches per frame.
        glitch_duration: Number of frames the glitch phase lasts before settling.
        settle_speed: How many characters settle per frame during the resolve phase.
        final_gradient_stops: Colors for the final resolved text gradient.
        final_gradient_steps: Number of gradient steps.
        final_gradient_direction: Direction of the final gradient.
    """

    parser_spec: argutils.ParserSpec = argutils.ParserSpec(
        name="glitch",
        help="Text glitches and corrupts, then repairs itself. VaroASCII original.",
        description="glitch | Digital distortion effect — text corrupts and repairs. VaroASCII original.",
        epilog="Example: varoascii glitch --glitch-intensity 60 --glitch-duration 40",
    )

    glitch_intensity: int = argutils.ArgSpec(
        name="--glitch-intensity",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=50,
        help="Probability (1-100) that a character glitches each frame during the glitch phase.",
    )  # pyright: ignore[reportAssignmentType]

    glitch_duration: int = argutils.ArgSpec(
        name="--glitch-duration",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=30,
        help="Number of frames the glitch chaos phase lasts before characters begin settling.",
    )  # pyright: ignore[reportAssignmentType]

    settle_speed: int = argutils.ArgSpec(
        name="--settle-speed",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=2,
        help="Number of characters that settle (stop glitching) per frame during the resolve phase.",
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_stops: tuple[Color, ...] = FinalGradientStopsArg(
        default=(Color("00ff41"), Color("00ffff")),
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_steps: tuple[int, ...] | int = FinalGradientStepsArg(
        default=12,
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_direction: Gradient.Direction = FinalGradientDirectionArg(
        default=Gradient.Direction.HORIZONTAL,
    )  # pyright: ignore[reportAssignmentType]


class GlitchIterator(BaseEffectIterator[GlitchConfig]):
    """Iterator for the Glitch effect.

    Phases:
        1. appear: Characters appear as glitched symbols.
        2. chaos: Characters randomly glitch for glitch_duration frames.
        3. settle: Characters progressively resolve to their real form.
    """

    def __init__(self, effect: Glitch) -> None:
        super().__init__(effect)
        self.phase = "appear"
        self.frame_count = 0
        self.glitching: list[EffectCharacter] = []
        self.settled: set[EffectCharacter] = set()
        self.character_final_colors: dict[EffectCharacter, Color] = {}
        self.build()

    def build(self) -> None:
        """Build the initial glitched state."""
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
            # Start with a random glitch symbol
            glitch_symbol = random.choice(_GLITCH_CHARS)
            glitch_color = random.choice(_GLITCH_COLORS)
            character.animation.set_appearance(glitch_symbol, ColorPair(fg=glitch_color))
            self.terminal.set_character_visibility(character, is_visible=True)
            self.glitching.append(character)

    def _apply_glitch_to_char(self, character: EffectCharacter) -> None:
        """Apply a random glitch to a single character."""
        glitch_symbol = random.choice(_GLITCH_CHARS)
        glitch_color = random.choice(_GLITCH_COLORS)
        character.animation.set_appearance(glitch_symbol, ColorPair(fg=glitch_color))

    def _settle_char(self, character: EffectCharacter) -> None:
        """Settle a character to its final real appearance."""
        final_color = self.character_final_colors[character]
        character.animation.set_appearance(character.input_symbol, ColorPair(fg=final_color))

    def __next__(self) -> str:
        if self.phase == "appear":
            # First frame — everything is already glitched from build()
            self.phase = "chaos"
            return self.frame

        if self.phase == "chaos":
            self.frame_count += 1

            # Randomly glitch characters
            for character in self.glitching:
                if random.randint(1, 100) <= self.config.glitch_intensity:
                    self._apply_glitch_to_char(character)

            if self.frame_count >= self.config.glitch_duration:
                self.phase = "settle"
                random.shuffle(self.glitching)

            return self.frame

        if self.phase == "settle":
            if self.glitching:
                # Settle a batch of characters
                batch_size = self.config.settle_speed
                batch = self.glitching[:batch_size]
                self.glitching = self.glitching[batch_size:]

                for character in batch:
                    self._settle_char(character)
                    self.settled.add(character)

                # Still-glitching characters keep flickering
                for character in self.glitching:
                    if random.randint(1, 100) <= 30:  # reduced intensity
                        self._apply_glitch_to_char(character)

                return self.frame

            # All settled — done
            if not hasattr(self, "_done"):
                self._done = True
                return self.frame

            raise StopIteration

        raise StopIteration


class Glitch(BaseEffect[GlitchConfig]):
    """Text glitches and corrupts, then repairs itself.

    A VaroASCII original effect. Characters appear as corrupted symbols
    with chromatic aberration colors, glitch chaotically, then progressively
    settle into their final form with a color gradient.
    """

    @property
    def _config_cls(self) -> type[GlitchConfig]:
        return GlitchConfig

    @property
    def _iterator_cls(self) -> type[GlitchIterator]:
        return GlitchIterator
