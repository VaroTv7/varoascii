# RandomSequence

![Demo](../img/effects_demos/randomsequence_demo.gif)

## Quick Start

``` py title="randomsequence.py"
from varoascii.effects.effect_random_sequence import RandomSequence

effect = RandomSequence("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_random_sequence
