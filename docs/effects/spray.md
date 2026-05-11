# Spray

![Demo](../img/effects_demos/spray_demo.gif)

## Quick Start

``` py title="spray.py"
from varoascii.effects.effect_spray import Spray

effect = Spray("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_spray
