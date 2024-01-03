infMonkeys = """
                ╭╴                 
          ╷ ┌─╮ ┼ ╷ ┌─╮ ╷ ┼╴╭─╮    
          │ │ │ │ │ │ │ │ │ ├─┘    
          ╵ ╵ ╵ ╵ ╵ ╵ ╵ ╵ ╰╴╰─╯    
      ┌─┬─╮ ╭─╮ ┌─╮ │ ╷ ╭─╮ ╷ ╷ ╭─╮
      │ │ │ │ │ │ │ ├┬╯ ├─┘ │ │ ╰─╮
      ╵ ╵ ╵ ╰─╯ ╵ ╵ ╵╰╴ ╰─╯ ╰─┤ ╰─╯
                             ─╯    
"""

import random
import string
import time

def calculate_odds(target, characters):
    char_odds = 1 / len(characters)
    target_odds = char_odds ** len(target)
    average_turns = 1 / target_odds
    return average_turns

def get_player_initials():
    while True:
        initials = input("Enter your initials (3 letters): ").upper()
        if len(initials) == 3 and initials.isalpha():
            return initials
        else:
            print("Invalid input. Please enter exactly 3 letters.")

def log_result(file_path, initials, target, average_turns, actual_turns, score, all_results):
    new_score_rank = None
    new_high_score = False
    new_low_score = False

    # Add the new result to all_results
    all_results.append([initials, target, int(average_turns), actual_turns, score])

    # Convert the last element (score) to integer for sorting
    for result in all_results:
        result[-1] = int(result[-1])

    # Sort by score in descending order
    all_results.sort(key=lambda x: x[-1], reverse=True)

    # Find the rank of the new score
    for index, result in enumerate(all_results):
        if result[0] == initials and result[1] == target and result[-1] == score:
            new_score_rank = index + 1
            break

    # Check if it's a new high or low score
    if new_score_rank == 1:
        new_high_score = True
    elif new_score_rank == len(all_results):
        new_low_score = True

    # Save the updated results
    with open(file_path, 'w') as file:
        for result in all_results:
            file.write(",".join(map(str, result)) + "\n")

    return new_score_rank, new_high_score, new_low_score


def read_game_results(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return [line.strip().split(',') for line in lines]
    except FileNotFoundError:
        return []

def display_top_scores(results, latest_result=None, top_n=10, bottom_n=10):
    scores = [(int(result[-1]), result) for result in results]
    scores.sort(reverse=True)  # Sort by score in descending order

    print("\nHIGH SCORE:")
    time.sleep(0.05)
    print("{:<4} {:<8} {:<20} {:>10} {:<2}".format("Rank", "Initials", "Target", "Score", ""))
    time.sleep(0.05)
    print("-" * 46)  # Print a line to separate headers from data
    time.sleep(0.5)

    for i, (score, result) in enumerate(scores[:top_n]):
        rank = i + 1
        initials = result[0]
        target = result[1]
        # Compare initials, target, and score to determine if this is the latest result
        highlight = "*" if latest_result and (initials, target, score) == (latest_result[0], latest_result[1], latest_result[4]) else ""
        print("{:<4} {:<8} {:<20} {:>10} {:<2}".format(rank, initials, target, score, highlight))
        time.sleep(0.05)  # Delay for 0.05 seconds

    time.sleep(0.5)

    # Display the lowest scores
    print("\nLOWEST SCORES:")
    time.sleep(0.05)
    print("{:<4} {:<8} {:<20} {:>10} {:<2}".format("Rank", "Initials", "Target", "Score", ""))
    time.sleep(0.05)
    print("-" * 46)  # Print a line to separate headers from data
    time.sleep(0.5)

    for i, (score, result) in enumerate(scores[-bottom_n:], start=1):
        rank = len(scores) - bottom_n + i
        initials = result[0]
        target = result[1]
        # Compare initials, target, and score to determine if this is the latest result
        highlight = "*" if latest_result and (initials, target, score) == (latest_result[0], latest_result[1], latest_result[4]) else ""
        print("{:<4} {:<8} {:<20} {:>10} {:<2}".format(rank, initials, target, score, highlight))
        time.sleep(0.05)  # Delay for 0.05 seconds

    time.sleep (0.5)





def play_game():
    # Read and display top scores
    print(infMonkeys)
    time.sleep(1)
    game_results_path = "game_results.txt"
    game_results = read_game_results(game_results_path)
    display_top_scores(game_results)

    # Define the target string
    target = input('\nTarget word or phrase: ')
    characters = string.ascii_letters + string.punctuation + string.digits + ' '
    average_turns = calculate_odds(target, characters)

    print('Expected turns: ' + str(int(average_turns)))
    input('Press ENTER to begin')

    recent_chars = ''
    turn = 1

    start_time = time.time()  # Start timing

    while True:
        char = random.choice(characters)
        print(char, end='')
        recent_chars = (recent_chars + char)[-len(target):]
        turn += 1

        if recent_chars == target:
            end_time = time.time()  # End timing
            duration = end_time - start_time  # Calculate duration
            print(f"\n\nIt took {turn} characters and {duration:.2f} seconds to print {target}")
            time.sleep(1)
            
            # Right-align the results using string formatting
            print(f"{'Expected turns:':<20} {str(int(average_turns)):>10}")
            print(f"{'Actual turns:':<20} {str(turn):>10}")
            score = int(average_turns) - turn
            print(f"{'Your score:':<20} {str(score):>10}")

            # Log the result and get the rank
            time.sleep(1.5)
            print()
            player_initials = get_player_initials()
            new_rank, is_high_score, is_low_score = log_result(game_results_path, player_initials, target, average_turns, turn, score, game_results)
            latest_result = [player_initials, target, int(average_turns), turn, score]

            # Display special messages based on the rank
            if new_rank <= 10:
                print()
                print(f"Congratulations! You are now ranked {new_rank} on the high score list!")
                time.sleep(1)
            if is_high_score:
                print()
                print("Incredible! You've set a new high score!")
                time.sleep(1)
            if is_low_score:
                print()
                print("Oh no! You've set a new low score!")
                time.sleep(1)

            time.sleep(1)
            print()
            print("Result saved.")
            time.sleep(1)

            break  # Break out of the loop to finish the game round


def main():
    while True:
        play_game()

if __name__ == "__main__":
    main()