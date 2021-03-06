"""This is all the classes. card, piles and hand"""
from random import randrange
import funcs


INVALID_INPUT = 2

class NonRenderGame:
    """This is the whole game class without any rendering."""

    def __init__(self, max_cards):
        self.hand = NonRenderHand()
        self.piles = NonRenderPiles()
        self.score = 0
        self.multiplier = 1
        self.trashes = 2
        self.mix = True
        self.max_cards = max_cards

    def init_hand(self):
        """Initiate the hand with two cards"""
        for i in range(2):
            self.hand.add_card(NonRenderCard(randrange(6) + 1))

    def place_card(self, _place):
        """
        This function takes a number between 0-3 and places a card there if it can.
        It return true if it placed a card.
        This is only used in the msachine learning part of the program.
        """

        if len(self.piles.piles[_place]) < self.max_cards:
            self.piles.add_card(self.hand.cards[0], _place)
            self.hand.cards.pop(0)
            self.hand.add_card(NonRenderCard((randrange(6) + 1)))

            answer = self.piles.update(_place)
            self.score += answer[0]
            if answer[1]:
                self.piles.piles[_place] = []
                self.multiplier += 1
                self.mix = True
                self.trashes = 2
            return True
        elif self.piles.piles[_place][self.max_cards-1].value == self.hand.cards[0].value:
            self.piles.piles[_place][self.max_cards-1].value += 1
            self.piles.update(_place)
            self.hand.cards.pop(0)
            self.hand.add_card(NonRenderCard((randrange(6) + 1)))
            return True
        else:
            return False

    def check_game_over(self):
        """Function used for checking if game is over."""
        total_length = 0
        for current_pile in self.piles.piles:
            total_length += len(current_pile)

        return bool(total_length >= 24)

    def trash(self):
        """Throw away a card from the hand."""
        self.trashes -= 1
        self.hand.trash()

    def mix_hand(self):
        """Mixes the cards in the hand."""
        self.mix = False
        self.hand.mix()


class MLGame(NonRenderGame):
    """
    This is the normal game with machine learning related functions.
    """
    def get_network_inputs(self):
        """
        This function is for the machine learning.
        It gives back an array of length 24 with the values(1-x not to 2048)of all of the cards.
        """
        return_array = []

        # Add the pile values to the array
        for i in range(4):
            for j in range(6):
                try:
                    self.piles.piles[i][j]
                except IndexError:
                    return_array.append(0)
                else:
                    return_array.append(self.piles.piles[i][j].value/11)

        # Add the hand to the array
        for card in self.hand.cards:
            return_array.append(card.value)

        # Add the amount of trashes and if there is a mix
        return_array.append(self.trashes)
        if self.mix:
            return_array.append(1)
        else:
            return_array.append(0)

        return return_array

    def get_action_random(self):
        pass

    def get_action_highest(self):
        pass

class GameWithRender(NonRenderGame):
    """Game With render function."""

    def __init__(self, _max_card, _height, _width):
        super().__init__(_max_card)
        self.hand = Hand()
        self.piles = Piles()
        self.height = _height
        self.width = _width

    def init_hand(self):
        """Initiate the hand with two cards"""
        for i in range(2):
            self.hand.add_card(Card((randrange(6) + 1), 70, 100))

    def place_card(self, _place):
        """This function takes a number between 0-3 and places a card there if it can."""
        if len(self.piles.piles[_place]) < self.max_cards:
            self.piles.add_card(self.hand.cards[0], _place)
            self.hand.cards.pop(0)
            self.hand.add_card(Card((randrange(6) + 1), 70, 100))

            answer = self.piles.update(_place)
            self.score += answer[0]
            if answer[1]:
                self.piles.piles[_place] = []
                self.multiplier += 1
                self.mix = True
                self.trashes = 2
        elif self.piles.piles[_place][self.max_cards-1].value == self.hand.cards[0].value:
            self.piles.piles[_place][self.max_cards-1].value += 1
            self.piles.update(_place)
            self.hand.cards.pop(0)
            self.hand.add_card(Card((randrange(6) + 1), 70, 100))

    def render(self, font, screen, pygame):
        """Renders hand and piles."""
        self.piles.render(font, screen, pygame, self.width, self.height)
        self.hand.render(font, screen, pygame, self.height)

    def trash(self):
        """Throw away a card from the hand."""
        if self.trashes == 0:
            return INVALID_INPUT
        self.trashes -= 1
        self.hand.trash()
        return None


class NonRenderCard():
    """Just information about card without any rendering capabilities"""

    def __init__(self, _value):
        self.value = _value

    def get_value(self):
        """This gets the not power two value of the card"""
        return 2 ** self.value


class Card(NonRenderCard):
    """This is the class for a single card with rendering capabilities."""

    def __init__(self, _value, _width=70, _height=100, _canMove=False):
        super().__init__(_value)
        self.width = _width
        self.height = _height

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


class NonRenderPiles():
    """Nonrender pile class. Parent to piles"""

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
                        self.piles[update_pile_index]) - 1].get_value()
                    answer[0] += new_value

                    if new_value == 2048:
                        answer[1] = True

                else:
                    i = 1
                    break

        return answer

    def add_card(self, _card, _pile):
        """Adds a card object to one of the piles"""
        self.piles[_pile].append(_card)


class Piles(NonRenderPiles):
    """The class for the four piles in this game"""

    def render(self, _font, _screen, _pygame, _width, _height):
        """Render all the cards in the piles"""
        for i, current_pile in enumerate(self.piles):
            x_cord = funcs.translate(i, 0, 4, 30, _width)
            for j, current_card in enumerate(current_pile):
                y_cord = funcs.translate(j, 0, 8, 30, _height - 100)

                current_card.render(_font, _screen, x_cord, y_cord, 2, _pygame)


class NonRenderHand():
    """NonRender hand parent to hand. Which has rendering functoin"""

    def __init__(self):
        self.cards = []

    def add_card(self, _card):
        """Adds a card to the end of the hand"""
        self.cards.append(_card)

    def trash(self):
        """Removes the card at the front and adds one to the end"""
        self.cards.pop(0)
        self.add_card(NonRenderCard(randrange(6)+1))

    def mix(self):
        """Switches the values of all the cards in the hand"""
        for i in range(0, len(self.cards)):
            self.cards[i].value = randrange(6)+1


class Hand(NonRenderHand):
    """This is the class for the two cards in the corner"""

    def render(self, _font, screen, pygame, height):
        """Renders the hand"""
        idx = 0
        for val in reversed(self.cards):
            val.render(_font, screen, 50 + 35 * idx, height - 130, 2, pygame)
            idx += 1

    def trash(self):
        """Removes the card at the front and adds one to the end"""
        self.cards.pop(0)
        self.add_card(Card(randrange(6)+1, 70, 100))
