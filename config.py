# Which operations to include
OPERATIONS = {
    "+": {"min": 1, "max": 99, "score": 150},
    "-": {"min": 1, "max": 99, "score": 200},
    "*": {"min": 0, "max": 10, "score": 200},
    "/": {"min": 1, "max": 10, "score": 300},
}

# Answering within this time gives full score, otherwise apply penalty
TIME_NO_PENALTY = 4  # seconds
# Score penalty per second after the no-penalty time
PENALTY_PER_SECOND = 12
# It will keep asking questions until the player reaches this score
TARGET_SCORE = 3500
# Repeat failes questions after this many questions in between
REPEAT_FAILED_AFTER = 10
