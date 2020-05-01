""" This is a copy of the 2048 solitaire app.
    I'm going to add a machine learning ai to this thing
    and see what score it can get later (hopefully) :)"""
import random as ran

import pygame

import cardclass
from funcs import renderMultiline

print("Starting...")

pygame.init()

WIDTH = 500
HEIGHT = 400

def main():
    """Just the main function"""
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
        hand.addCard(cardclass.Card((ran.randrange(6) + 1), 70, 100))
        i += 1
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                # Key 0 is 49 key 4 is 53
                if 49 <= event.key < 53:
                    current_key = event.key - 49
                    if len(piles.piles[current_key]) < 6:
                        piles.addCard(hand.cards[0], current_key)
                        hand.cards.pop(0)
                        hand.addCard(cardclass.Card(
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

                if trashs > 0 and event.key == pygame.K_t:
                    trashs -= 1
                    hand.trash((ran.randrange(6) + 1))

                if mix and event.key == pygame.K_m:
                    mix = False
                    values = []
                    for i in range(2):
                        values.append(ran.randrange(6) + 1)
                    hand.mix(values)

        pygame.display.flip()
        screen.fill((50, 50, 50))  # Draw the background

        piles.render(myfont, screen, pygame, WIDTH, HEIGHT)
        hand.render(myfont, screen, pygame, HEIGHT)

        renderMultiline("Score: " + str(score) + "\nMultiplier: " +
                        str(multiplier), WIDTH - 200, HEIGHT - 60, screen, myfont)

        clock.tick(60)


if __name__ == "__main__":
    main()
