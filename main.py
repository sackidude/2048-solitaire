""" This is a copy of the 2048 solitaire app.
    I'm going to add a machine learning ai to this thing
    and see what score it can get later(hopefully): ) """

import normalgame
import machinelearning

def main():
    """Main function. just decides if you are going to boot normal game or machine learning"""
    input_text = input("Normal Game or Machine learning: [N/M]")

    if input_text == "M":
        machinelearning.machine_learning()
    else:
        normalgame.normal_game()

if __name__ == "__main__":
    main()
