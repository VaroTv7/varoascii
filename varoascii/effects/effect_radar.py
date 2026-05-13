"""Radar effect — characters appear as a radar sweep passes over them.

A VaroASCII original effect. A radar line sweeps in a circular pattern,
and characters illuminate as the sweep reaches their position, fading
from bright green to a dim afterglow.

Classes:
    Radar: Radar sweep reveal effect.
    RadarConfig: Configuration for the Radar effect.
    RadarIterator: Iterates over the Radar effect.
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
    return "radar", Radar, RadarConfig


@dataclass
class RadarConfig(BaseConfig):
    """Configuration for the Radar effect."""

    parser_spec: argutils.ParserSpec = argutils.ParserSpec(
        name="radar",
        help="Characters reveal as a radar sweep passes over them. VaroASCII original.",
        description="radar | Radar sweep character reveal. VaroASCII original.",
        epilog="Example: varoascii radar --sweep-count 2 --sweep-speed 6",
    )

    sweep_count: int = argutils.ArgSpec(
        name="--sweep-count",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=2,
        help="Number of full 360-degree sweeps before all characters are locked.",
    )  # pyright: ignore[reportAssignmentType]

    sweep_speed: int = argutils.ArgSpec(
        name="--sweep-speed",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=6,
        help="Degrees the sweep line moves per frame.",
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_stops: tuple[Color, ...] = FinalGradientStopsArg(
        default=(Color("00ff41"), Color("00ffff")),
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_steps: tuple[int, ...] | int = FinalGradientStepsArg(
        default=12,
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_direction: Gradient.Direction = FinalGradientDirectionArg(
        default=Gradient.Direction.RADIAL,
    )  # pyright: ignore[reportAssignmentType]


class RadarIterator(BaseEffectIterator[RadarConfig]):
    """Iterator for the Radar effect."""

    def __init__(self, effect: Radar) -> None:
        super().__init__(effect)
        self.angle = 0.0
        self.sweep_number = 0
        self.all_chars: list[EffectCharacter] = []
        self.character_final_colors: dict[EffectCharacter, Color] = {}
        self.char_angles: dict[EffectCharacter, float] = {}
        self.hit_count: dict[EffectCharacter, int] = {}
        self.center_col = 0.0
        self.center_row = 0.0
        self.build()

    def build(self) -> None:
        """Compute angle of each character relative to center."""
        final_gradient = Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.canvas.text_bottom,
            self.terminal.canvas.text_top,
            self.terminal.canvas.text_left,
            self.terminal.canvas.text_right,
            self.config.final_gradient_direction,
        )

        self.all_chars = list(self.terminal.get_characters())
        if not self.all_chars:
            return

        cols = [c.input_coord.column for c in self.all_chars]
        rows = [c.input_coord.row for c in self.all_chars]
        self.center_col = (min(cols) + max(cols)) / 2
        self.center_row = (min(rows) + max(rows)) / 2

        for character in self.all_chars:
            self.character_final_colors[character] = final_gradient_mapping.get(
                character.input_coord, Color("ffffff")
            )
            dx = character.input_coord.column - self.center_col
            dy = -(character.input_coord.row - self.center_row)
            angle_rad = math.atan2(dy, dx)
            angle_deg = math.degrees(angle_rad) % 360
            self.char_angles[character] = angle_deg
            self.hit_count[character] = 0

            character.animation.set_appearance(character.input_symbol, ColorPair(fg=Color("0a1a0a")))
            self.terminal.set_character_visibility(character, is_visible=True)

    def _angle_distance(self, a: float, b: float) -> float:
        """Shortest angular distance between two angles in degrees."""
        diff = abs(a - b) % 360
        return min(diff, 360 - diff)

    def __next__(self) -> str:
        if self.sweep_number >= self.config.sweep_count:
            # Final: lock all to final colors
            for character in self.all_chars:
                final_color = self.character_final_colors[character]
                character.animation.set_appearance(character.input_symbol, ColorPair(fg=final_color))

            if not hasattr(self, "_done"):
                self._done = True
                return self.frame
            raise StopIteration

        beam_width = 15.0  # degrees

        for character in self.all_chars:
            char_angle = self.char_angles[character]
            dist = self._angle_distance(self.angle, char_angle)

            if dist <= beam_width:
                # In the beam — bright
                brightness = 1.0 - (dist / beam_width) * 0.6
                hit_factor = min(self.hit_count[character] + 1, self.config.sweep_count)
                base_brightness = hit_factor / self.config.sweep_count

                final_color = self.character_final_colors[character]
                hex_clean = final_color.rgb_color if hasattr(final_color, "rgb_color") else str(final_color).lstrip("#")
                if "Color" in hex_clean:
                    import re
                    match = re.search(r"[0-9a-fA-F]{6}", hex_clean)
                    if match:
                        hex_clean = match.group(0)
                if len(hex_clean) < 6:
                    hex_clean = hex_clean.ljust(6, "0")
                r = int(int(hex_clean[0:2], 16) * brightness)
                g = int(int(hex_clean[2:4], 16) * brightness)
                b = int(int(hex_clean[4:6], 16) * brightness)
                color = Color(f"{min(255,r):02x}{min(255,g):02x}{min(255,b):02x}")
                character.animation.set_appearance(character.input_symbol, ColorPair(fg=color))

                if dist <= 3:
                    self.hit_count[character] = min(self.hit_count[character] + 1, self.config.sweep_count)
            else:
                # Afterglow based on how many times it's been hit
                hits = self.hit_count[character]
                if hits > 0:
                    afterglow = 0.15 + (hits / self.config.sweep_count) * 0.4
                    final_color = self.character_final_colors[character]
                    hex_clean = final_color.rgb_color if hasattr(final_color, "rgb_color") else str(final_color).lstrip("#")
                    if "Color" in hex_clean:
                        import re
                        match = re.search(r"[0-9a-fA-F]{6}", hex_clean)
                        if match:
                            hex_clean = match.group(0)
                    if len(hex_clean) < 6:
                        hex_clean = hex_clean.ljust(6, "0")
                    r = int(int(hex_clean[0:2], 16) * afterglow)
                    g = int(int(hex_clean[2:4], 16) * afterglow)
                    b = int(int(hex_clean[4:6], 16) * afterglow)
                    color = Color(f"{min(255,r):02x}{min(255,g):02x}{min(255,b):02x}")
                    character.animation.set_appearance(character.input_symbol, ColorPair(fg=color))

        self.angle += self.config.sweep_speed
        if self.angle >= 360:
            self.angle -= 360
            self.sweep_number += 1

        return self.frame


class Radar(BaseEffect[RadarConfig]):
    """Characters reveal as a radar sweep passes over them.

    A VaroASCII original effect. A radar beam sweeps in a 360-degree
    pattern from the center of the text. Characters glow when the beam
    passes over them and retain an afterglow that brightens with each sweep.
    """

    @property
    def _config_cls(self) -> type[RadarConfig]:
        return RadarConfig

    @property
    def _iterator_cls(self) -> type[RadarIterator]:
        return RadarIterator
