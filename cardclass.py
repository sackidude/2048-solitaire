import funcs


class Card:

    def __init__(self, _value, _width=70, _height=100, _canMove=False):
        self.value = _value
        self.width = _width
        self.height = _height
        self.canMove = _canMove

    def getValue(self):
        return (2 ** self.value)

    def getColor(self):
        translated = funcs.map(self.value, 1, 12, 0, 255)
        return (
            translated,
            255 - translated,
            255 - translated
        )

    def render(self, _font, _screen,  x_cord, y_cord, border, _pygame):
        # Render the outline. Large them the card by 5 pixels.
        if(border > 0):
            _pygame.draw.rect(_screen, (255, 255, 255), _pygame.Rect(
                (x_cord - border, y_cord - border),
                (self.width + 2*border, self.height + 2*border)
            ))

        # Render the actual card
        _pygame.draw.rect(
            _screen,
            self.getColor(),
            _pygame.Rect(
                (x_cord, y_cord),
                (self.width, self.height)
            )
        )

        currentText = _font.render(
            str(self.getValue()),
            True,
            (0, 0, 0)
        )
        _screen.blit(currentText, (x_cord, y_cord))  # render the text


class Piles():
    def __init__(self):
        self.piles = [[], [], [], []]

    def update(self, update_pile_index):
        answer = [0, False]

        for i in range(len(self.piles[update_pile_index]), 0, -1):
            current_card_i = i - 1

            if current_card_i > 0:
                current_pile = self.piles[update_pile_index]

                if current_pile[current_card_i].value == current_pile[current_card_i - 1].value:
                    del self.piles[update_pile_index][-1]
                    current_pile[len(
                        self.piles[update_pile_index]) - 1].value += 1
                    new_value = current_pile[len(
                        self.piles[update_pile_index]) - 1].getValue()
                    answer[0] += new_value

                    if new_value == 2048:
                        answer[1] = True

                else:
                    i = 1
                    break

        return answer

    def render(self, _font, _screen, _pygame, _width, _height):

        for i, current_pile in enumerate(self.piles):
            x = funcs.map(i, 0, 4, 30, _width)
            for j, current_card in enumerate(current_pile):
                y = funcs.map(j, 0, 8,
                              30, _height - 100)

                current_card.render(_font, _screen, x, y, 2, _pygame)

    def addCard(self, _card, _pile):
        self.piles[_pile].append(_card)


class Hand():
    def __init__(self):
        self.cards = []

    def addCard(self, _card):
        self.cards.append(_card)

    def render(self, _font, screen, pygame, height):
        idx = 0
        for val in reversed(self.cards):
            val.render(_font, screen, 50 + 35 * idx, height - 130, 2, pygame)
            idx += 1

    def trash(self, new_num):
        self.cards.pop(0)
        self.addCard(Card(new_num, 70, 100))

    def mix(self, values):
        for i in range(0, len(self.cards)):
            self.cards[i].value = values[i]
