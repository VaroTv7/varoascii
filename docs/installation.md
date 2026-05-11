# Installation

varoascii can be installed as a system application using pipx or as a library using pip.

## System Application using Pipx

When installed as an application, varoascii can be called from the shell to produce effects on any input piped to stdin. Usages include invocation on shell launch, aliasing commands to pass output through TTE, and SSH login animations.

Pipx is the easiest way to make TTE available in your shell.

`pipx install varoascii`

!!! note

    If pipx is unavailable, you can install via `pip` and run TTE by calling the python binary with the module argument.

    ```bash title="ls redirection"
    ls -latr | python3 -m varoascii
    ```

[Application Usage](./appguide.md){ .md-button }

## Library installation using Pip

When installed as a library, varoascii can be imported to produce animations in your Python applications.

`pip install varoascii`

[Library Usage](./libguide.md){ .md-button }
