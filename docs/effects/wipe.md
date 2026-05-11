# Wipe

![Demo](../img/effects_demos/wipe_demo.gif)

## Quick Start

``` py title="wipe.py"
from varoascii.effects.effect_wipe import Wipe

effect = Wipe("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_wipe
