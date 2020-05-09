"""
This is a copy of the 2048 solitaire app.
I'm going to add a machine learning ai to this thing
and see what score it can get later(hopefully): )
"""


def main():
    """
    Main function.
    Just decides if you are going to
    * play a normal game,
    * start machine learning
    * or loads a saved checkpoint in the current directory
    """
    input_text = input("Normal Game or Machine learning or replay checkpoint file[N/M/]: ")

    if input_text == "M":
        import os
        from machine_learning.machinelearning import machine_learning
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'machine_learning/config.txt')
        machine_learning(config_path)
    elif input_text == "N":
        import normalgame
        normalgame.normal_game()
    else:
        from machine_learning.replaycheckpoint import replay_checkpoint
        from machine_learning.machinelearning import eval_genomes
        import os
        from machine_learning.machinelearning import machine_learning
        import neat
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'machine_learning/config.txt')
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
        checkpoint_str = input("Type the checkpoint filename: ")
        max_cards = int(input("Enter the max card amout: "))
        width = int(input("Enter the width: "))
        height = int(input("Enter the height: "))
        replay_checkpoint(checkpoint_str, eval_genomes, config, max_cards, width, height)


if __name__ == "__main__":
    main()
