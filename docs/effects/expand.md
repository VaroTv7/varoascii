# Expand

![Demo](../img/effects_demos/expand_demo.gif)

## Quick Start

``` py title="expand.py"
from varoascii.effects.effect_expand import Expand

effect = Expand("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_expand
