# Which operations to include
OPERATIONS = {
    "+": {"min": 1, "max": 99, "score": 100},
    "-": {"min": 1, "max": 99, "score": 200},
    "*": {"min": 0, "max": 10, "score": 200},
    "/": {"min": 1, "max": 10, "score": 300},  # generates exact divisions
}

TIME_NO_PENALTY = 5  # seconds
PENALTY_PER_SECOND = 10
TARGET_SCORE = 2500
