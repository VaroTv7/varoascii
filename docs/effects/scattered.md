# Scattered

![Demo](../img/effects_demos/scattered_demo.gif)

## Quick Start

``` py title="scattered.py"
from varoascii.effects.effect_scattered import Scattered

effect = Scattered("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_scattered
