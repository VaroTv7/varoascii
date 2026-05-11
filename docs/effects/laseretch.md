# LaserEtch

![Demo](../img/effects_demos/laseretch_demo.gif)

## Quick Start

``` py title="laseretch.py"
from varoascii import Gradient
from varoascii.effects.effect_laseretch import LaserEtch

effect = LaserEtch("YourTextHere")

with effect.terminal_output() as terminal:
    effect.effect_config.final_gradient_direction = Gradient.Direction.HORIZONTAL
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_laseretch
