import random
import time
import threading
from config import OPERATIONS, PENALTY_PER_SECOND, TARGET_SCORE, TIME_NO_PENALTY

# This assigns an scopre to the operation based on the difficulty of the question
def rate_score_operation(a, op, b, answer, base_score):
    score_penalty = 0
    easy_numbers = (0, 1, 10)

    # print(f"⏱️ Evaluating score for: {a} {op} {b} = {answer} (base score: {base_score})")

    if op == "+":
        if a in easy_numbers:
            score_penalty += base_score // 3
        if b in easy_numbers:
            score_penalty += base_score // 3
        if answer in easy_numbers:
            score_penalty += base_score // 3
        if a > 100:
            score_penalty -= base_score * 2
        elif a > 50:
            score_penalty -= base_score
        if b > 100:
            score_penalty -= base_score * 2
        elif b > 50:
            score_penalty -= base_score
    elif op == "-":
        if b in easy_numbers:
            score_penalty += base_score // 3
        if answer in easy_numbers:
            score_penalty += base_score // 3
        if a > 100:
            score_penalty -= base_score
        elif a > 50:
            score_penalty -= base_score // 2
        if b > 100:
            score_penalty -= base_score
        elif b > 50:
            score_penalty -= base_score // 2
    elif op == "*":
        if a in easy_numbers:
            score_penalty += base_score // 3
        if b in easy_numbers:
            score_penalty += base_score // 3
    elif op == "/":
        if b == 1:
            score_penalty += base_score // 2
        elif b == 10:
            score_penalty += base_score // 3
        if answer in easy_numbers:
            score_penalty += base_score // 3

    # debug print
    # print(f"⏱️ Base score: {base_score}, score penalty: {score_penalty}")
    return base_score - score_penalty

def generate_question():
    op = random.choice(list(OPERATIONS.keys()))
    cfg = OPERATIONS[op]

    a = random.randint(cfg["min"], cfg["max"])
    b = random.randint(cfg["min"], cfg["max"])

    if op == "+":
        answer = a + b
    elif op == "-":
        answer = a
        a = a + b  # Ensure non-negative result
    elif op == "*":
        answer = a * b
    elif op == "/":
        answer = random.randint(cfg["min"], cfg["max"])
        a = answer * b  # Ensure exact division

    score = rate_score_operation(a, op, b, answer, cfg["score"])

    return f"{a} {op} {b}", answer, score

def main():
    my_score = 0
    failed_stack = []
    q_counter = 0

    print("\n🎯 Math Game (Ctrl+C to exit)")
    global_start = time.time()

    while my_score < TARGET_SCORE:
        q_counter += 1
        if failed_stack and failed_stack[0][0] < q_counter - 5:  # retry questions after 3 new ones
            _, text, answer, score = failed_stack.pop(0)
        else:
            text, answer, score = generate_question()
        q = (f"\n[{my_score}/{TARGET_SCORE}] Question 🤔 {text} = ")

        start = time.time()
        user_input = input(q)
        time_taken = time.time() - start

        try:
            user_input = int(user_input)
        except:
            print(f"⚠️ Invalid input: {user_input}. Expected a number.")
            continue

        if user_input == answer:
            penalty_time = max(0, time_taken - TIME_NO_PENALTY)
            this_score = max((score - int(penalty_time * PENALTY_PER_SECOND)), 0)
            # debug print:
            # print(f"⏱️ Time taken: {time_taken:.2f}s, penalty time: {penalty_time:.2f}s, base score: {score}, final score: {this_score}")
            my_score += this_score
            print(f"✅ Correcte! (temps: {time_taken:.2f}s, puntuació: {this_score})")
        else:
            print(f"❌ Error! La resposta correcta és: {answer}, i no pas {user_input}")
            failed_stack.append((q_counter, text, answer, score))

    global_time = time.time() - global_start
    print(f"\n🏁 Final! Puntuació: {my_score}, temps total: {global_time:.2f}s, questions: {q_counter}")


if __name__ == "__main__":
    main()
