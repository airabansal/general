#!/usr/bin/env python3
"""Rock-paper-scissors: play against the computer.

Best-of-N: first to win the most rounds after N rounds wins the match.
"""

import random

CHOICES = ["rock", "paper", "scissors"]

# Maps each choice to the choice it beats.
BEATS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}


def get_player_choice():
    """Prompt until the player enters rock, paper, or scissors (r/p/s accepted)."""
    shortcuts = {"r": "rock", "p": "paper", "s": "scissors"}
    while True:
        raw = input("Your move (rock/paper/scissors, or q to quit): ").strip().lower()
        if raw in ("q", "quit"):
            return None
        if raw in CHOICES:
            return raw
        if raw in shortcuts:
            return shortcuts[raw]
        print("  Invalid choice. Try again.")


def decide(player, computer):
    """Return 'player', 'computer', or 'tie'."""
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "player"
    return "computer"


def main():
    print("=== Rock, Paper, Scissors ===")
    player_score = 0
    computer_score = 0

    while True:
        player = get_player_choice()
        if player is None:
            break

        computer = random.choice(CHOICES)
        print(f"  You chose {player}, computer chose {computer}.")

        result = decide(player, computer)
        if result == "tie":
            print("  It's a tie!")
        elif result == "player":
            player_score += 1
            print("  You win this round!")
        else:
            computer_score += 1
            print("  Computer wins this round.")

        print(f"  Score -> You: {player_score}  Computer: {computer_score}\n")

    print("\n=== Final score ===")
    print(f"You: {player_score}  Computer: {computer_score}")
    if player_score > computer_score:
        print("You won the match!")
    elif computer_score > player_score:
        print("Computer won the match.")
    else:
        print("The match is a draw.")


if __name__ == "__main__":
    main()
