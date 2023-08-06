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

**Simple Usage**
```python
from boxprint import bprint, BoxTypes
from colors import *  # ansicolors

"""
@param width
  Max width of the box
@param box_type
  The type of the box (LIGHT, HEAVY, DOUBLE, ROUND)
@param print_func
  The print function to use
@param stroke_func
  How the box characters should be stroked
@param fill_func
  How the text characters should be filled
"""
bprint("hello_world", width=40, box_type=BoxTypes.HEAVY, print_func=print)
bprint("Text\nWith\nMultiple\nLines")
bprint(
    "\nhello_world\n",
    width=40,
    box_type=BoxTypes.FILL,
    stroke_func=lambda text: color(text, fg="blue"),
    fill_func=lambda text: color(text, bg="blue", fg="black")
)

buf = []
def print_to_buf(string):
  buf.append(string)

# Boxes apply 2 spaces of padding to the left and right width = (default=80 - 2*2)
bprint("Inner Box", width=76, print_func=print_to_buf)
inner_box = "".join(buf)

bprint(f"I am some text!\n{inner_box}", title="Outer Box")
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

▗▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▖
▐                                      ▌
▐ hello_world                          ▌
▐                                      ▌
▝▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▘

╭─┤ Outer Box ├────────────────────────────────────────────────────────────────╮
│                                                                              │
│ I am some text!                                                              │
│ ╭──────────────────────────────────────────────────────────────────────────╮ │
│ │ Inner Box                                                                │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---
**Debug**
```python
from boxprint import dprint

a_list_of_numbers = [1, 2, 3, 4, 5]
dprint(a_list_of_numbers)

a_list_of_numbers = None
dprint(a_list_of_numbers)
```
```
╭─┤ a_list_of_numbers ├────────────────────────────────────────────────────────╮
│                                                                              │
│ tests/test_debug.py:11                                                       │
│                                                                              │
│ type = <class 'list'>                                                        │
│ value = [1, 2, 3, 4, 5]                                                      │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─┤ a_list_of_numbers ├────────────────────────────────────────────────────────╮
│                                                                              │
│ tests/test_debug.py:14                                                       │
│                                                                              │
│ type = <class 'NoneType'>                                                    │
│ value = None                                                                 │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

**Current Stack**

```python
from boxprint import stprint

def my_function(param1, param2):
    local1 = [param1] * 4
    local2 = "a"
    stprint(width=60)

for i in range(5):
    my_function(i, i*3)
```
```
╭─┤ my_function - tests/test_stprint.py:35 ├───────────────╮
│                                                          │
│   param1 = 0                                             │
│   param2 = 0                                             │
│   local1 = [0, 0, 0, 0]                                  │
│   local2 = a                                             │
│                                                          │
╰──────────────────────────────────────────────────────────╯
╭─┤ my_function - tests/test_stprint.py:35 ├───────────────╮
│                                                          │
│   param1 = 1                                             │
│   param2 = 3                                             │
│   local1 = [1, 1, 1, 1]                                  │
│   local2 = a                                             │
│                                                          │
╰──────────────────────────────────────────────────────────╯
```