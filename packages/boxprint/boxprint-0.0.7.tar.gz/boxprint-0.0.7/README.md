# Boxprint

A small package to print boxes

## Usage

```python
from boxprint import bprint

bprint("hello world")
```
```
╭──────────────────────────────────────────────────────────────────────────────╮
│ Hello World                                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Examples

```python
from boxprint import bprint, BoxTypes

"""
@param width
  Max width of the box
@param box_type
  The type of the box (LIGHT, HEAVY, DOUBLE, ROUND)
@param print_func
  The print function to use
"""
bprint("hello_world", width=40, box_type=BoxTypes.HEAVY, print_func=print)
bprint("Text\nWith\nMultiple\nLines")
```
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Hello World                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

╭──────────────────────────────────────────────────────────────────────────────╮
│ Text                                                                         │
│ With                                                                         │
│ Multiple                                                                     │
│ Lines                                                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

```python
buf = []
def print_to_buf(string):
  buf.append(string)

# Boxes apply 2 spaces of padding to the left and right width = (default=80 - 2*2)
bprint("Inner Box", width=76, print_func=print_to_buf)
inner_box = "".join(buf)

bprint(f"I am some text!\n{inner_box}", title="Outer Box")
```
```
╭─┤ Outer Box ├────────────────────────────────────────────────────────────────╮
│                                                                              │
│ I am some text!                                                              │
│ ╭──────────────────────────────────────────────────────────────────────────╮ │
│ │ Inner Box                                                                │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
╰──────────────────────────────────────────────────────────────────────────────╯
```



**Solid Box**
```python
from colors import *  # ansicolors

bprint(
    "\nhello_world\n",
    width=40,
    box_type=BoxTypes.FILL,
    stroke_func=lambda text: color(text, fg="blue"),
    fill_func=lambda text: color(text, bg="blue", fg="black")
)
```
```
▗▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▖
▐                                      ▌
▐ hello_world                          ▌
▐                                      ▌
▝▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▘
```