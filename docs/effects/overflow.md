# Overflow

![Demo](../img/effects_demos/overflow_demo.gif)

## Quick Start

``` py title="overflow.py"
from varoascii.effects.effect_overflow import Overflow

effect = Overflow("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_overflow
