# Pour

![Demo](../img/effects_demos/pour_demo.gif)

## Quick Start

``` py title="pour.py"
from varoascii.effects.effect_pour import Pour

effect = Pour("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_pour
