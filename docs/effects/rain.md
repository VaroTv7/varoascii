# Rain

![Demo](../img/effects_demos/rain_demo.gif)

## Quick Start

``` py title="rain.py"
from varoascii.effects.effect_rain import Rain

effect = Rain("YourTextHere")
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
```

::: varoascii.effects.effect_rain
