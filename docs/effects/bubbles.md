# Bubbles

![Demo](../img/effects_demos/bubbles_demo.gif)

## Quick Start

``` py title="bubbles.py"
from varoascii.effects.effect_bubbles import Bubbles

effect = Bubbles("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_bubbles
