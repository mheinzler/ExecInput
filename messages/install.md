# ExecInput

This Sublime Text package allows you to send input to `stdin` of the currently
running process. The process must have been started through the `exec` build
target which is used by all standard build systems.

It works by hooking into the `ExecCommand` class to get access to the currently
running process. Because of that, it should also be compatible with all other
build targets that extend the default `ExecCommand` class.

## Usage

Make sure to start a process that is waiting for input. Now there are multiple
ways to send input:

- Using the default key binding while the build output panel is visible:
    Ctrl+Alt+Enter
- Using the menu item `Tools` → `Send input`
- Using the `Command Palette` item `ExecInput: Send input`

The entered text will then be sent to the process and also added to the build
output panel.

Multiple lines of input can be send by using Shift+Enter.

## Customization

This packages provides the command `exec_input`. Use this if you want to
customize the key bindings, menu items, etc.
