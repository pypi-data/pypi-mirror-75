from enum import Enum

# TODO: check buffer overflow with title


class BoxTypeIndices(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    TOP_RIGHT = 4
    TOP_LEFT = 5
    BOTTOM_LEFT = 6
    BOTTOM_RIGHT = 7
    LEFT_PADDER = 8
    RIGHT_PADDER = 9


class BoxTypes(Enum):
    LIGHT = "\u2500\u2500\u2502\u2502\u250C\u2510\u2514\u2518\u2524\u251C"
    HEAVY = "\u2501\u2501\u2503\u2503\u250F\u2513\u2517\u251B\u252B\u2523"
    DOUBLE = "\u2550\u2550\u2551\u2551\u2554\u2557\u255A\u255D\u2561\u255E"
    ROUND = "\u2500\u2500\u2502\u2502\u256D\u256E\u2570\u256F\u2524\u251C"
    FILL = "\u2584\u2580\u2590\u258c\u2597\u2596\u259D\u2598\u2596\u2597"

   # TODO: Dashed boxes don't look good, should they even exist?
    LIGHT_DOUBLE_DASHED = "\u254C\u254C\u254E\u254E\u250C\u2510\u2514\u2518\u2524\u251C"
    HEAVY_DOUBLE_DASHED = "\u254D\u254D\u254F\u254F\u250F\u2513\u2517\u251B\u252B\u2523"
    LIGHT_TRIPLE_DASHED = "\u2504\u2504\u2506\u2506\u250C\u2510\u2514\u2518\u2524\u251C"
    HEAVY_TRIPLE_DASHED = "\u2505\u2505\u2507\u2507\u250F\u2513\u2517\u251B\u252B\u2523"
    LIGHT_QUADRUPLE_DASHED = "\u2508\u2508\u2506\u2506\u250C\u2510\u2514\u2518\u2524\u251C"
    HEAVY_QUADRUPLE_DASHED = "\u2509\u2509\u2507\u2507\u250F\u2513\u2517\u251B\u252B\u2523"

    def getChar(self, index):
        return self.value[index.value]


def next_newline_index(string, start, end):
    for i in range(start, end):
        # TODO: handle other kinds of newlines?
        if string[i] == '\n':
            return i
    return -1


def set_title(text, title, start_index=2):
    for letter in title:
        text[start_index] = letter
        start_index += 1


# def count_newlines_at_end(text):
    # for


def bprint(
    text="",
    title="",
    width=80,
    box_type=BoxTypes.ROUND,
    print_func=print,
    stroke_func=lambda text: text,
    fill_func=lambda text: text
):
    line = [box_type.getChar(BoxTypeIndices.TOP)] * width
    line[0] = box_type.getChar(BoxTypeIndices.TOP_RIGHT)
    line[-1] = box_type.getChar(BoxTypeIndices.TOP_LEFT)
    if len(title) > 0:
        # Add Title
        title_to_replace = f"{box_type.getChar(BoxTypeIndices.LEFT_PADDER)} {title} {box_type.getChar(BoxTypeIndices.RIGHT_PADDER)}"
        set_title(line, title_to_replace)
        print_func(stroke_func("".join(line)))
        # Remove Title
        set_title(line, [box_type.getChar(BoxTypeIndices.TOP)]
                  * len(title_to_replace))
    else:
        print_func(stroke_func("".join(line)))

    padding = fill_func(" ")
    text_per_line = width - 4
    strlen = len(text)
    # TODO: handle other kinds of newlines?
    if text[-1] == "\n":
        strlen -= 1

    def get_line(text):
        return f"{stroke_func(box_type.getChar(BoxTypeIndices.LEFT))}{padding}{fill_func(text)}{padding}{stroke_func(box_type.getChar(BoxTypeIndices.RIGHT))}"

    end = 0
    buf = ""
    while end < strlen:
        previous_end = end
        end += text_per_line
        end = min(strlen, end)
        newline_index = next_newline_index(text, previous_end, end)
        if newline_index != -1:
            buf = text[previous_end:newline_index]
            end = newline_index + 1
        else:
            buf = text[previous_end:end]

        buf = buf.ljust(text_per_line, " ")
        print_func(get_line(buf))

    if text.endswith("\n"):
        print_func(get_line("".ljust(text_per_line)))

    if box_type.getChar(BoxTypeIndices.TOP) != box_type.getChar(BoxTypeIndices.BOTTOM):
        line = [box_type.getChar(BoxTypeIndices.BOTTOM)] * width
    line[0] = box_type.getChar(BoxTypeIndices.BOTTOM_LEFT)
    line[-1] = box_type.getChar(BoxTypeIndices.BOTTOM_RIGHT)
    print_func(stroke_func("".join(line)))
