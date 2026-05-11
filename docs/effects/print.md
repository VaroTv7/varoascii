# Print

![Demo](../img/effects_demos/print_demo.gif)

## Quick Start

``` py title="print.py"
from varoascii.effects.effect_print import Print

effect = Print("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_print
