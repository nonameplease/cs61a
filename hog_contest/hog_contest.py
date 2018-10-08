"""
This is a minimal contest submission file. You may also submit the full
hog.py from Project 1 as your contest entry.

Only this file will be submitted. Make sure to include any helper functions
from `hog.py` that you'll need here! For example, if you have a function to
calculate Free Bacon points, you should make sure it's added to this file
as well.
"""

TEAM_NAME = "Let's play games"

def final_strategy(score, opponent_score):
    from dice import four_sided, six_sided, make_test_dice

    def expectation(n, score, opponent_score):
        average_turn = make_averaged(roll_dice, 1000)
        if (score + opponent_score) % 7 == 0:
            expected_value = average_turn(n, four_sided)
        else:
            expected_value = average_turn(n, six_sided)
        return expected_value

    def primenize(score):
        output = score
        prime_num = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
        for i in range(0,25):
            if score == prime_num[i]:
                output =prime_num[i+1]
        return output

    def free_bacon(opponent_score):
        max_digit = 0
        last_digit = 0
        while opponent_score > 0:
            last_digit = opponent_score % 10
            if last_digit > max_digit:
                max_digit = last_digit
            opponent_score = opponent_score // 10
        return max_digit + 1

    def select_dice(score, opponent_score):
        if (score + opponent_score) % 7 == 0:
            return four_sided
        else:
            return six_sided

    def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
        my_score = 0
        my_score = free_bacon(opponent_score)
        my_score = primenize(my_score)
        if opponent_score == 2 * (score + my_score):
            return 0
        elif my_score >= margin:
            return 0
        else:
            return num_rolls

    def is_swap(score0, score1):
        if score0 == 2 * score1 or score1 == 2 * score0:
            return True
        return False

    num_rolls = 6
    dice_num = 6
    margin = 11
    swing_swap_num_rolls = 6
    rolling_num_rolls = 6
    score_to_use_four_dice = 7 - (score + opponent_score) % 7
    free_bacon_points = primenize(free_bacon(opponent_score))
    score_difference = opponent_score / 2 - score
    score_to_negative_swap = (score / 2) - opponent_score
    if select_dice(score, opponent_score) == six_sided:
        dice_num = 6
    else:
        dice_num = 4
    if score > 90:
        margin = 9
    num_rolls = swap_strategy(score, opponent_score, margin, dice_num)

    Swing_swap_possible = False
    if score_difference == free_bacon_points:
        Swing_swap_possible = True
        swing_swap_num_rolls = 0
    elif score_difference == 1:
        Swing_swap_possible = True
        swing_swap_num_rolls = 10
    elif score_difference == 3:
        Swing_swap_possible = True
        swing_swap_num_rolls = 9

    Rolling_possible = False
    n = 10
    for n in range(1, 11, -1):
        if expectation(n, score, opponent_score) > free_bacon_points:
            rolling_num_rolls = n
            Rolling_possible = True

    if score + free_bacon_points >= 90 and not is_swap(free_bacon_points + score, opponent_score):
        return 0
    elif Swing_swap_possible:
        return swing_swap_num_rolls
    elif score_to_use_four_dice == free_bacon_points and score_to_negative_swap != free_bacon_points:
        return 0
    elif Rolling_possible and score <= 90:
        return rolling_num_rolls

    return num_rolls
