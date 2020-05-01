"""This is all the classes. card, piles and hand"""
import funcs


class Card:
    """This is the class for a single card"""
    def __init__(self, _value, _width=70, _height=100, _canMove=False):
        self.value = _value
        self.width = _width
        self.height = _height

    def get_value(self):
        """This gets the not power two value of the card"""
        return 2 ** self.value

    def get_color(self):
        """Gets the color of the card. Will maybe be based on a color theme in the future"""
        translated = funcs.translate(self.value, 1, 12, 0, 255)
        return (
            translated,
            255 - translated,
            255 - translated
        )

    def render(self, _font, _screen, x_cord, y_cord, border, _pygame):
        """Render the card"""
        # Render the outline. Large them the card by 5 pixels.
        if border > 0:
            _pygame.draw.rect(_screen, (255, 255, 255), _pygame.Rect(
                (x_cord - border, y_cord - border),
                (self.width + 2*border, self.height + 2*border)
            ))

        # Render the actual card
        _pygame.draw.rect(
            _screen,
            self.get_color(),
            _pygame.Rect(
                (x_cord, y_cord),
                (self.width, self.height)
            )
        )

        current_text = _font.render(
            str(self.get_value()),
            True,
            (0, 0, 0)
        )
        _screen.blit(current_text, (x_cord, y_cord))  # render the text


class Piles():
    """The class for the four piles in this game"""
    def __init__(self):
        self.piles = [[], [], [], []]

    def update(self, update_pile_index):
        """This combines all the cards that can be combined in the specific pile"""
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
        """Render all the cards in the piles"""
        for i, current_pile in enumerate(self.piles):
            x_cord = funcs.translate(i, 0, 4, 30, _width)
            for j, current_card in enumerate(current_pile):
                y_cord = funcs.translate(j, 0, 8, 30, _height - 100)

                current_card.render(_font, _screen, x_cord, y_cord, 2, _pygame)

    def add_card(self, _card, _pile):
        """Adds a card object to one of the piles"""
        self.piles[_pile].append(_card)


class Hand():
    """This is the class for the two cards in the corner"""
    def __init__(self):
        self.cards = []

    def add_card(self, _card):
        """Adds a card to the end of the hand"""
        self.cards.append(_card)

    def render(self, _font, screen, pygame, height):
        """Renders the hand"""
        idx = 0
        for val in reversed(self.cards):
            val.render(_font, screen, 50 + 35 * idx, height - 130, 2, pygame)
            idx += 1

    def trash(self, new_num):
        """Removes the card at the front and adds one to the end"""
        self.cards.pop(0)
        self.add_card(Card(new_num, 70, 100))

    def mix(self, values):
        """Switches the values of all the cards in the hand"""
        for i in range(0, len(self.cards)):
            self.cards[i].value = values[i]
