""" This is a copy of the 2048 solitaire app.
    I'm going to add a machine learning ai to this thing
    and see what score it can get later(hopefully): ) """

import random as ran
from time import sleep
import pygame

import cardclass
from funcs import render_multiline

print("Starting...")

pygame.init()

WIDTH = 500
HEIGHT = 400
RENDER = True


def main():
    """Just the main function of this game"""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    myfont = pygame.font.SysFont('Comic Sans MS', 20)

    hand = cardclass.Hand()
    piles = cardclass.Piles()

    score = 0
    multiplier = 1
    trashs = 2
    mix = True

    i = 0
    while i < 2:
        hand.add_card(cardclass.Card((ran.randrange(6) + 1), 70, 100))
        i += 1

    done = False
    while not done:
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                # Key 0 is 49 key 4 is 53
                if 49 <= event.key < 53:
                    current_key = event.key - 49
                    if len(piles.piles[current_key]) < 6:
                        piles.add_card(hand.cards[0], current_key)
                        hand.cards.pop(0)
                        hand.add_card(cardclass.Card(
                            (ran.randrange(6) + 1), 70, 100))

                        answer = piles.update(current_key)
                        score += answer[0]
                        if answer[1]:
                            piles.piles[current_key] = []
                            multiplier += 1
                            mix = True
                            trashs = 2

                    elif piles.piles[current_key][5].value == hand.cards[0].value:
                        piles.piles[current_key][5].value += 1
                        piles.update(current_key)
                        hand.cards.pop(0)
                        hand.add_card(cardclass.Card(
                            (ran.randrange(6) + 1), 70, 100))
                    total_length = 0
                    for current_pile in piles.piles:
                        total_length += len(current_pile)

                    if total_length >= 24:
                        screen.fill((0, 0, 0))
                        render_multiline("GAME OVER!\nYour score: {}".format(
                            score), WIDTH/2, HEIGHT/2, screen, myfont, (255, 255, 255))
                        done = True
                        game_over = True
                        break
                if trashs > 0 and event.key == pygame.K_t:
                    # Throw away a card. Press the key K to activate
                    trashs -= 1
                    hand.trash((ran.randrange(6) + 1))

                if mix and event.key == pygame.K_m:
                    # Mixes the cards in the hand. Press the key U to activate
                    mix = False
                    values = []
                    for i in range(2):
                        values.append(ran.randrange(6) + 1)
                    hand.mix(values)

        pygame.display.flip()
        screen.fill((50, 50, 50))  # Draw the background

        # Render the pile and hand
        piles.render(myfont, screen, pygame, WIDTH, HEIGHT)
        hand.render(myfont, screen, pygame, HEIGHT)

        render_multiline('Score: {}\nMultiplier: x{}\nTrashes: {}'.format(
            score, multiplier, trashs) + '\nMix: ' + str(mix),
                         WIDTH - 200, HEIGHT - 100, screen, myfont, (255, 255, 255))

        clock.tick(60)
        if done and game_over:
            sleep(2)


if __name__ == "__main__":
    main()
