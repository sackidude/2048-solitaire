"""All the functions in this projet"""

def translate(value, left_min, left_max, right_min, right_max):
    """This maps a value from one range to another. TY to the guy on stackoverflow"""
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)


def render_multiline(text, _x, _y, _screen, _font, color):
    """A function for rendering several line strings"""
    render_arr = str.splitlines(text)
    for i, current_text in enumerate(render_arr):
        txt = _font.render(
            current_text,
            True,
            color
        )
        _screen.blit(txt, (_x, _y + 20 * i))  # render the text
