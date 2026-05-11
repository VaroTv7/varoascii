# Beams

![Demo](../img/effects_demos/beams_demo.gif)

## Quick Start

``` py title="beams.py"
from varoascii.effects.effect_beams import Beams

effect = Beams("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_beams
