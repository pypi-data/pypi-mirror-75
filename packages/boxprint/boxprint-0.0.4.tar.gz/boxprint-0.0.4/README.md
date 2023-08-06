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

## Configurations

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