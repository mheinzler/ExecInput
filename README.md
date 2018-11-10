# ExecInput

This Sublime Text package allows you to send input to `stdin` of the currently
running process. The process must have been started through the `exec` build
target which is used by all standard build systems.

It works by hooking into the `ExecCommand` class to get access to the currently
running process. Because of that, it should also be compatible with all other
build targets that extend the default `ExecCommand` class.

## Installation

### Package Control

The easiest way to install is using Sublime Text's [Package Control]
[package-control]:

- Open the `Command Palette` using the menu item `Tools` → `Command Palette...`
- Choose `Package Control: Install Package`
- Install `ExecInput`

### Download

- Download a [release][releases]
- Extract the package and rename it to `ExecInput`
- Copy the package into your `Packages` directory. You can find this using the
    menu item `Preferences` → `Browse Packages...`.

## Usage

Make sure to start a process that is waiting for input. Now there are multiple
ways to send input:

- Using the default key binding: <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+
    <kbd>Enter</kbd>
- Using the menu item `Tools` → `Send input`
- Using the `Command Palette` item `ExecInput: Send input`

The entered text will then be sent to the process and also added to the build
output panel.

Multiple lines of input can be send by using <kbd>Shift</kbd>+<kbd>Enter</kbd>.

## Customization

This packages provides the command `exec_input`. Use this if you want to
customize the key bindings, menu items, etc.

[package-control]: https://packagecontrol.io/installation
[releases]: https://github.com/mheinzler/ExecInput/releases
