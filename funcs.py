def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def renderMultiline(text, x, y, _screen, _font):
    render_arr = str.splitlines(text)
    for i, current_text in enumerate(render_arr):
        txt = _font.render(
            current_text,
            True,
            (255, 255, 255)
        )
        _screen.blit(txt, (x, y + 20 * i))  # render the text
