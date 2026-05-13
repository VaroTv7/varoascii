"""Cinema effect — cinematic title card reveal with dramatic lighting.

A VaroASCII original effect. Text starts completely dark, then dramatic
spotlights sweep across revealing characters with lens flare highlights,
finishing with a golden/silver title card glow — like a movie opening.

Classes:
    Cinema: Cinematic title card effect.
    CinemaConfig: Configuration for the Cinema effect.
    CinemaIterator: Iterates over the Cinema effect.
"""

from __future__ import annotations

import math
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
    return "cinema", Cinema, CinemaConfig


@dataclass
class CinemaConfig(BaseConfig):
    """Configuration for the Cinema effect.

    Attributes:
        sweep_speed: How fast the spotlight sweeps across (columns per frame).
        spotlight_width: Width of the spotlight beam in columns.
        dramatic_pause: Frames of darkness before the sweep begins.
        final_gradient_stops: Colors for the final title card.
        final_gradient_steps: Gradient steps.
        final_gradient_direction: Gradient direction.
    """

    parser_spec: argutils.ParserSpec = argutils.ParserSpec(
        name="cinema",
        help="Cinematic title card reveal with dramatic spotlight. VaroASCII original.",
        description="cinema | Movie-style title reveal with sweeping spotlight. VaroASCII original.",
        epilog="Example: varoascii cinema --sweep-speed 2 --spotlight-width 6",
    )

    sweep_speed: int = argutils.ArgSpec(
        name="--sweep-speed",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=2,
        help="Columns the spotlight moves per frame.",
    )  # pyright: ignore[reportAssignmentType]

    spotlight_width: int = argutils.ArgSpec(
        name="--spotlight-width",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=5,
        help="Width of the spotlight beam in columns.",
    )  # pyright: ignore[reportAssignmentType]

    dramatic_pause: int = argutils.ArgSpec(
        name="--dramatic-pause",
        type=argutils.NonNegativeInt.type_parser,
        metavar=argutils.NonNegativeInt.METAVAR,
        default=8,
        help="Frames of darkness before the spotlight begins.",
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_stops: tuple[Color, ...] = FinalGradientStopsArg(
        default=(Color("ffd700"), Color("ffffff"), Color("ffd700")),
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_steps: tuple[int, ...] | int = FinalGradientStepsArg(
        default=12,
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_direction: Gradient.Direction = FinalGradientDirectionArg(
        default=Gradient.Direction.HORIZONTAL,
    )  # pyright: ignore[reportAssignmentType]


class CinemaIterator(BaseEffectIterator[CinemaConfig]):
    """Iterator for the Cinema effect.

    Phases:
        1. darkness: Dramatic pause in complete darkness.
        2. sweep: Spotlight sweeps left-to-right revealing characters.
        3. glow: Revealed text transitions from spotlight white to final gradient.
        4. done: Stable final display.
    """

    def __init__(self, effect: Cinema) -> None:
        super().__init__(effect)
        self.phase = "darkness"
        self.frame_count = 0
        self.spotlight_pos = 0
        self.max_column = 0
        self.min_column = 0
        self.all_chars: list[EffectCharacter] = []
        self.character_final_colors: dict[EffectCharacter, Color] = {}
        self.revealed: set[EffectCharacter] = set()
        self.glow_step = 0
        self.build()

    def build(self) -> None:
        """Prepare characters in darkness."""
        final_gradient = Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.canvas.text_bottom,
            self.terminal.canvas.text_top,
            self.terminal.canvas.text_left,
            self.terminal.canvas.text_right,
            self.config.final_gradient_direction,
        )

        self.all_chars = list(self.terminal.get_characters())

        columns = set()
        for character in self.all_chars:
            self.character_final_colors[character] = final_gradient_mapping.get(
                character.input_coord, Color("ffffff")
            )
            # Start in darkness
            character.animation.set_appearance(character.input_symbol, ColorPair(fg=Color("0a0a0a")))
            self.terminal.set_character_visibility(character, is_visible=True)
            columns.add(character.input_coord.column)

        if columns:
            self.min_column = min(columns)
            self.max_column = max(columns)
        self.spotlight_pos = self.min_column

    def __next__(self) -> str:
        if self.phase == "darkness":
            self.frame_count += 1
            if self.frame_count >= self.config.dramatic_pause:
                self.phase = "sweep"
            return self.frame

        if self.phase == "sweep":
            half_width = self.config.spotlight_width // 2

            for character in self.all_chars:
                col = character.input_coord.column
                dist = abs(col - self.spotlight_pos)

                if dist <= half_width:
                    # In spotlight — bright white/yellow
                    intensity = 1.0 - (dist / max(half_width, 1)) * 0.5
                    r = int(255 * intensity)
                    g = int(240 * intensity)
                    b = int(200 * intensity)
                    color = Color(f"{r:02x}{g:02x}{b:02x}")
                    character.animation.set_appearance(character.input_symbol, ColorPair(fg=color))
                    self.revealed.add(character)
                elif character in self.revealed:
                    # Already revealed — dim afterglow
                    final_color = self.character_final_colors[character]
                    character.animation.set_appearance(character.input_symbol, ColorPair(fg=final_color))
                else:
                    # Not yet reached — stay dark
                    character.animation.set_appearance(character.input_symbol, ColorPair(fg=Color("0a0a0a")))

            self.spotlight_pos += self.config.sweep_speed

            if self.spotlight_pos > self.max_column + self.config.spotlight_width:
                self.phase = "glow"

            return self.frame

        if self.phase == "glow":
            self.glow_step += 1
            # All characters settle to their final gradient color
            for character in self.all_chars:
                final_color = self.character_final_colors[character]
                character.animation.set_appearance(character.input_symbol, ColorPair(fg=final_color))

            if self.glow_step >= 3:
                self.phase = "done"
            return self.frame

        if self.phase == "done":
            if not hasattr(self, "_done"):
                self._done = True
                return self.frame
            raise StopIteration

        raise StopIteration


class Cinema(BaseEffect[CinemaConfig]):
    """Cinematic title card reveal with dramatic spotlight.

    A VaroASCII original effect. Text starts in complete darkness,
    a spotlight sweeps across revealing characters with a golden glow,
    then settles into the final gradient — like a movie title card.
    """

    @property
    def _config_cls(self) -> type[CinemaConfig]:
        return CinemaConfig

    @property
    def _iterator_cls(self) -> type[CinemaIterator]:
        return CinemaIterator
