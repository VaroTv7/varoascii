# Crumble

![Demo](../img/effects_demos/crumble_demo.gif)

## Quick Start

``` py title="crumble.py"
from varoascii.effects.effect_crumble import Crumble

effect = Crumble("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_crumble
