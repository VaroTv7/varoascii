"""Typewriter effect — characters appear one by one as if being typed.

A VaroASCII original effect. Characters appear sequentially with a blinking
cursor that moves across the text, simulating a mechanical typewriter.

Classes:
    Typewriter: Typewriter text reveal effect.
    TypewriterConfig: Configuration for the Typewriter effect.
    TypewriterIterator: Iterates over the Typewriter effect.
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
    return "typewriter", Typewriter, TypewriterConfig


@dataclass
class TypewriterConfig(BaseConfig):
    """Configuration for the Typewriter effect.

    Attributes:
        typing_speed: Characters typed per frame.
        cursor_symbol: Symbol used for the cursor.
        cursor_color: Color of the cursor.
        pause_on_space: Extra frames to pause when reaching a space character.
        mistake_probability: Probability (0-100) of making a typing mistake.
        final_gradient_stops: Colors for the final text gradient.
        final_gradient_steps: Number of gradient steps.
        final_gradient_direction: Direction of the final gradient.
    """

    parser_spec: argutils.ParserSpec = argutils.ParserSpec(
        name="typewriter",
        help="Characters appear as if typed on a typewriter. VaroASCII original.",
        description="typewriter | Mechanical typewriter text reveal effect. VaroASCII original.",
        epilog="Example: varoascii typewriter --typing-speed 1 --cursor-symbol █ --mistake-probability 5",
    )

    typing_speed: int = argutils.ArgSpec(
        name="--typing-speed",
        type=argutils.PositiveInt.type_parser,
        metavar=argutils.PositiveInt.METAVAR,
        default=1,
        help="Number of characters typed per frame.",
    )  # pyright: ignore[reportAssignmentType]

    cursor_symbol: str = argutils.ArgSpec(
        name="--cursor-symbol",
        type=str,
        default="█",
        help="Symbol to use as the typing cursor.",
    )  # pyright: ignore[reportAssignmentType]

    cursor_color: Color = argutils.ArgSpec(
        name="--cursor-color",
        type=argutils.ColorArg.type_parser,
        metavar=argutils.ColorArg.METAVAR,
        default=Color("00ff00"),
        help="Color of the typing cursor.",
    )  # pyright: ignore[reportAssignmentType]

    pause_on_space: int = argutils.ArgSpec(
        name="--pause-on-space",
        type=argutils.NonNegativeInt.type_parser,
        metavar=argutils.NonNegativeInt.METAVAR,
        default=2,
        help="Extra frames to pause when the cursor reaches a space character.",
    )  # pyright: ignore[reportAssignmentType]

    mistake_probability: int = argutils.ArgSpec(
        name="--mistake-probability",
        type=argutils.NonNegativeInt.type_parser,
        metavar=argutils.NonNegativeInt.METAVAR,
        default=3,
        help="Probability (0-100) of making a typing mistake that gets corrected.",
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_stops: tuple[Color, ...] = FinalGradientStopsArg(
        default=(Color("ffcc00"), Color("ff8800")),
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_steps: tuple[int, ...] | int = FinalGradientStepsArg(
        default=12,
    )  # pyright: ignore[reportAssignmentType]

    final_gradient_direction: Gradient.Direction = FinalGradientDirectionArg(
        default=Gradient.Direction.HORIZONTAL,
    )  # pyright: ignore[reportAssignmentType]


class TypewriterIterator(BaseEffectIterator[TypewriterConfig]):
    """Iterator for the Typewriter effect.

    Characters are revealed left-to-right, top-to-bottom with a visible
    cursor. Occasionally makes a mistake and corrects it.
    """

    _MISTAKE_CHARS = list("abcdefghijklmnopqrstuvwxyz0123456789!@#$%")

    def __init__(self, effect: Typewriter) -> None:
        super().__init__(effect)
        self.pending: list[EffectCharacter] = []
        self.cursor_char: EffectCharacter | None = None
        self.pause_frames = 0
        self.mistake_state: dict | None = None  # tracks active mistake correction
        self.character_final_colors: dict[EffectCharacter, Color] = {}
        self.build()

    def build(self) -> None:
        """Build the typing order and prepare the gradient."""
        final_gradient = Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.canvas.text_bottom,
            self.terminal.canvas.text_top,
            self.terminal.canvas.text_left,
            self.terminal.canvas.text_right,
            self.config.final_gradient_direction,
        )

        all_chars = list(self.terminal.get_characters())

        # Sort by row (top-to-bottom) then column (left-to-right)
        all_chars.sort(key=lambda c: (-c.input_coord.row, c.input_coord.column))

        for character in all_chars:
            self.character_final_colors[character] = final_gradient_mapping.get(
                character.input_coord, Color("ffffff")
            )
            self.terminal.set_character_visibility(character, is_visible=False)

        self.pending = all_chars

    def _type_character(self, character: EffectCharacter) -> None:
        """Reveal a character with its final color."""
        color = self.character_final_colors[character]
        character.animation.set_appearance(character.input_symbol, ColorPair(fg=color))
        self.terminal.set_character_visibility(character, is_visible=True)

    def _show_cursor(self, character: EffectCharacter) -> None:
        """Show the cursor at a character's position."""
        if self.cursor_char and self.cursor_char != character:
            # Restore the previous cursor position to its real character
            prev_color = self.character_final_colors[self.cursor_char]
            self.cursor_char.animation.set_appearance(
                self.cursor_char.input_symbol, ColorPair(fg=prev_color)
            )
        character.animation.set_appearance(
            self.config.cursor_symbol, ColorPair(fg=self.config.cursor_color)
        )
        self.terminal.set_character_visibility(character, is_visible=True)
        self.cursor_char = character

    def __next__(self) -> str:
        # Handle pause (e.g., after a space)
        if self.pause_frames > 0:
            self.pause_frames -= 1
            return self.frame

        # Handle mistake correction
        if self.mistake_state is not None:
            state = self.mistake_state
            if state["phase"] == "show_mistake":
                # Show the wrong character briefly
                state["phase"] = "pause"
                state["frames_left"] = 3
                char = state["character"]
                wrong = random.choice(self._MISTAKE_CHARS)
                char.animation.set_appearance(wrong, ColorPair(fg=Color("ff0040")))
                return self.frame
            elif state["phase"] == "pause":
                state["frames_left"] -= 1
                if state["frames_left"] <= 0:
                    state["phase"] = "correct"
                return self.frame
            elif state["phase"] == "correct":
                # Fix the mistake — type the correct character
                char = state["character"]
                self._type_character(char)
                self.mistake_state = None
                return self.frame

        if self.pending:
            batch_size = self.config.typing_speed
            batch = self.pending[:batch_size]
            self.pending = self.pending[batch_size:]

            for character in batch:
                # Check for typing mistake
                if (
                    character.input_symbol.strip()
                    and random.randint(1, 100) <= self.config.mistake_probability
                ):
                    self._show_cursor(character)
                    self.mistake_state = {
                        "phase": "show_mistake",
                        "character": character,
                    }
                    # Put remaining batch back
                    return self.frame

                self._type_character(character)

                # Pause on spaces (but not if all remaining chars are also spaces)
                if character.input_symbol == " ":
                    has_non_space = any(c.input_symbol.strip() for c in self.pending)
                    if has_non_space:
                        self.pause_frames = self.config.pause_on_space

            # Show cursor at next position if there are more characters
            if self.pending:
                self._show_cursor(self.pending[0])

            return self.frame

        # Remove cursor and finish
        if self.cursor_char:
            final_color = self.character_final_colors[self.cursor_char]
            self.cursor_char.animation.set_appearance(
                self.cursor_char.input_symbol, ColorPair(fg=final_color)
            )
            self.cursor_char = None
            return self.frame

        if not hasattr(self, "_done"):
            self._done = True
            return self.frame

        raise StopIteration


class Typewriter(BaseEffect[TypewriterConfig]):
    """Characters appear as if typed on a mechanical typewriter.

    A VaroASCII original effect. Features a visible cursor, natural typing
    rhythm with pauses on spaces, and occasional typos that get corrected.
    """

    @property
    def _config_cls(self) -> type[TypewriterConfig]:
        return TypewriterConfig

    @property
    def _iterator_cls(self) -> type[TypewriterIterator]:
        return TypewriterIterator
