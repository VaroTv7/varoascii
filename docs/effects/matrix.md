# Matrix

![Demo](../img/effects_demos/matrix_demo.gif)

## Quick Start

``` py title="matrix.py"
from varoascii.effects.effect_matrix import Matrix

effect = Matrix("YourTextHere\n" * 10)
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_matrix
