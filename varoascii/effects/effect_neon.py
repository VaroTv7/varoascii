"""Neon effect — text pulses with a glowing neon sign effect.

A VaroASCII original effect. Characters appear dark, then pulse with
increasing brightness as if a neon sign is powering up, with subtle
flickering to simulate electrical instability.

Classes:
    Neon: Neon glow pulsation effect.
    NeonConfig: Configuration for the Neon effect.
    NeonIterator: Iterates over the Neon effect.
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
    return "neon", Neon, NeonConfig


@dataclass
class NeonConfig(BaseConfig):
    """Configuration for the Neon effect.

    Attributes:
        glow_phases: Number of brightness pulses before the sign stabilizes.
        flicker_probability: Chance (0-100) that the sign flickers off briefly.
        power_up_speed: Characters that light up per frame during initial power-up.
        final_gradient_stops: Colors for the final glowing text.
        final_gradient_steps: Gradient steps.
        final_gradient_direction: Gradient direction.
    """

    parser_spec: argutils.ParserSpec = argutils.ParserSpec(
        name="neon",
        help="Text glows like a neon sign powering up. VaroASCII original.",
        description="neon | Neon sign glow effect with flickering. VaroASCII original.",
        epilog="Example: varoascii neon --glow-phases 4 --flicker-probability 15",
    )

    glow_phases: int = argutils.ArgSpec(
        name="--glow-phases",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=3,
        help="Number of brightness pulses before stabilizing.",
    )  # pyright: ignore[reportAssignmentType]

    flicker_probability: int = argutils.ArgSpec(
        name="--flicker-probability",
        type=argutils.NonNegativeInt.type_parser,
        metavar=argutils.NonNegativeInt.METAVAR,
        default=10,
        help="Probability (0-100) that the sign flickers off briefly each pulse.",
    )  # pyright: ignore[reportAssignmentType]

    power_up_speed: int = argutils.ArgSpec(
        name="--power-up-speed",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=5,
        help="Characters that light up per frame during initial power-up.",
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_stops: tuple[Color, ...] = FinalGradientStopsArg(
        default=(Color("ff00ff"), Color("ff69b4"), Color("ff1493")),
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_steps: tuple[int, ...] | int = FinalGradientStepsArg(
        default=12,
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_direction: Gradient.Direction = FinalGradientDirectionArg(
        default=Gradient.Direction.HORIZONTAL,
    )  # pyright: ignore[reportAssignmentType]


def _dim_color(color: Color, factor: float) -> Color:
    """Dim a color by a factor (0.0 = black, 1.0 = original)."""
    hex_str = str(color)
    # Extract RGB from the color — handle both with and without #
    clean = hex_str.lstrip("#")
    if len(clean) < 6:
        clean = clean.ljust(6, "0")
    r = int(int(clean[0:2], 16) * factor)
    g = int(int(clean[2:4], 16) * factor)
    b = int(int(clean[4:6], 16) * factor)
    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))
    return Color(f"{r:02x}{g:02x}{b:02x}")


class NeonIterator(BaseEffectIterator[NeonConfig]):
    """Iterator for the Neon effect.

    Phases:
        1. dark: All characters hidden.
        2. power_up: Characters appear one by one in dim color.
        3. pulse: Brightness pulses up and down several times.
        4. flicker: Random brief blackouts.
        5. stable: Final glow at full brightness.
    """

    def __init__(self, effect: Neon) -> None:
        super().__init__(effect)
        self.phase = "dark"
        self.frame_count = 0
        self.pulse_count = 0
        self.power_up_pending: list[EffectCharacter] = []
        self.all_chars: list[EffectCharacter] = []
        self.character_final_colors: dict[EffectCharacter, Color] = {}
        self.brightness = 0.0
        self.brightness_direction = 1  # 1 = increasing, -1 = decreasing
        self.flicker_frames = 0
        self.build()

    def build(self) -> None:
        """Build gradient mapping and prepare characters."""
        final_gradient = Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.canvas.text_bottom,
            self.terminal.canvas.text_top,
            self.terminal.canvas.text_left,
            self.terminal.canvas.text_right,
            self.config.final_gradient_direction,
        )

        self.all_chars = list(self.terminal.get_characters())
        for character in self.all_chars:
            self.character_final_colors[character] = final_gradient_mapping.get(
                character.input_coord, Color("ffffff")
            )
            self.terminal.set_character_visibility(character, is_visible=False)

        # Randomize power-up order for a more organic feel
        self.power_up_pending = list(self.all_chars)
        random.shuffle(self.power_up_pending)

    def _set_all_brightness(self, factor: float) -> None:
        """Set all characters to a specific brightness."""
        for character in self.all_chars:
            color = _dim_color(self.character_final_colors[character], factor)
            character.animation.set_appearance(character.input_symbol, ColorPair(fg=color))

    def _set_all_off(self) -> None:
        """Turn all characters dark (flicker off)."""
        for character in self.all_chars:
            character.animation.set_appearance(character.input_symbol, ColorPair(fg=Color("111111")))

    def __next__(self) -> str:
        if self.phase == "dark":
            self.phase = "power_up"
            return self.frame

        if self.phase == "power_up":
            if self.power_up_pending:
                batch = self.power_up_pending[:self.config.power_up_speed]
                self.power_up_pending = self.power_up_pending[len(batch):]
                for character in batch:
                    dim = _dim_color(self.character_final_colors[character], 0.2)
                    character.animation.set_appearance(character.input_symbol, ColorPair(fg=dim))
                    self.terminal.set_character_visibility(character, is_visible=True)
                return self.frame
            self.phase = "pulse"
            self.brightness = 0.2
            return self.frame

        if self.phase == "pulse":
            # Handle flicker
            if self.flicker_frames > 0:
                self.flicker_frames -= 1
                if self.flicker_frames == 0:
                    self._set_all_brightness(self.brightness)
                return self.frame

            # Random flicker chance
            if random.randint(1, 100) <= self.config.flicker_probability:
                self._set_all_off()
                self.flicker_frames = random.randint(1, 3)
                return self.frame

            # Pulse brightness
            self.brightness += 0.08 * self.brightness_direction
            if self.brightness >= 1.0:
                self.brightness = 1.0
                self.brightness_direction = -1
            elif self.brightness <= 0.15:
                self.brightness = 0.15
                self.brightness_direction = 1
                self.pulse_count += 1

            self._set_all_brightness(self.brightness)

            if self.pulse_count >= self.config.glow_phases:
                self.phase = "stabilize"
                self.brightness = 0.5

            return self.frame

        if self.phase == "stabilize":
            self.brightness += 0.05
            if self.brightness >= 1.0:
                self.brightness = 1.0
                self._set_all_brightness(1.0)
                self.phase = "done"
            else:
                self._set_all_brightness(self.brightness)
            return self.frame

        if self.phase == "done":
            if not hasattr(self, "_done"):
                self._done = True
                return self.frame
            raise StopIteration

        raise StopIteration


class Neon(BaseEffect[NeonConfig]):
    """Text glows like a neon sign powering up.

    A VaroASCII original effect. Characters power up from darkness,
    pulse with increasing brightness, flicker randomly, and finally
    stabilize at full glow with a color gradient.
    """

    @property
    def _config_cls(self) -> type[NeonConfig]:
        return NeonConfig

    @property
    def _iterator_cls(self) -> type[NeonIterator]:
        return NeonIterator
