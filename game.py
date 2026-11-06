import random
from collections import Counter, deque

MOVES = ("rock", "paper", "scissors")
RESULT_MESSAGES = {
    "win": "You win!",
    "lose": "You lose!",
    "tie": "It's a tie!",
}

# Counter-strategy mapping: what beats what
COUNTER_MOVES = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock",
}


class MoveHistory:
    """Optional helper for experimenting with your recent moves."""

    def __init__(self, max_rounds=10):
        # Keep only the most recent moves so the history stays small.
        self.moves = deque(maxlen=max_rounds)

    def remember(self, move):
        # Call this after a round has a valid move from you.
        if move in MOVES:
            self.moves.append(move)

    def most_common_move(self):
        # There is no pattern to report until a move has been recorded.
        if not self.moves:
            return None
        return Counter(self.moves).most_common(1)[0][0]


# Persistent tracker instance across rounds
history = MoveHistory()


def recognize_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    finger_tips = (8, 12, 16, 20)
    finger_pips = (6, 10, 14, 18)
    extended = [
        landmarks[tip].y < landmarks[pip].y
        for tip, pip in zip(finger_tips, finger_pips)
    ]

    if not any(extended):
        return "rock"
    if all(extended):
        return "paper"
    if extended == [True, True, False, False]:
        return "scissors"
    return None


def choose_computer_move():
    # If the player has established a pattern, play the counter to their favorite move
    frequent_move = history.most_common_move()
    if frequent_move:
        return COUNTER_MOVES[frequent_move]

    # Cold start: fallback to random choice when no valid history exists
    return random.choice(MOVES)


def determine_winner(player_move, computer_move):
    if player_move not in MOVES or computer_move not in MOVES:
        raise ValueError("Moves must be rock, paper, or scissors.")

    # Automatically log the valid player move to update the AI's history
    history.remember(player_move)

    if player_move == computer_move:
        return "tie"
    if (player_move, computer_move) in (
        ("rock", "scissors"),
        ("paper", "rock"),
        ("scissors", "paper"),
    ):
        return "win"
    return "lose"


def get_result_message(result):
    return RESULT_MESSAGES[result]


def update_score(result, player_score, computer_score):
    if result == "win":
        player_score += 1
    elif result == "lose":
        computer_score += 1
    elif result != "tie":
        raise ValueError("Result must be win, lose, or tie.")
    return player_score, computer_score