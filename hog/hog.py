"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled (capped at 11 - NUM_ROLLS).
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    num_of_iteration = num_rolls
    num_rolled = 0
    num_of_ones = 0
    num_sum = 0
    while num_of_iteration > 0:
        num_rolled = dice()
        num_sum += num_rolled
        if num_rolled == 1:
            num_of_ones += 1
        num_of_iteration -= 1
    if num_of_ones != 0:
        return min(num_of_ones, (11 - num_rolls))
    else:
        return num_sum
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    max_digit = 0
    last_digit = 0
    while opponent_score > 0:
        last_digit = opponent_score % 10
        if last_digit > max_digit:
            max_digit = last_digit
        opponent_score = opponent_score // 10
    return max_digit + 1
    # END PROBLEM 2


# Write your prime functions here!
def is_prime(x):
    if x == 1:
        return False
    i = 2
    while i < x:
        if x % i == 0:
            return False
        i += 1
    return True

def primenize(score):
    output = score
    prime_num = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
    for i in range(0,25):
        if score == prime_num[i]:
            output =prime_num[i+1]
    return output


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    my_score = 0
    if num_rolls == 0:
        my_score = free_bacon(opponent_score)
    else:
        my_score = roll_dice(num_rolls, dice)
    my_score = primenize(my_score)
    return my_score
    # END PROBLEM 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).
    """
    # BEGIN PROBLEM 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END PROBLEM 3

def is_swap(score0, score1):
    """Returns whether one of the scores is double the other.
    """
    # BEGIN PROBLEM 4
    if score0 == 2 * score1 or score1 == 2 * score0:
        return True
    return False
    # END PROBLEM 4

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        if player == 0:
            num_rolls = strategy0(score0, score1)
            if num_rolls == 0:
                score0 += primenize(free_bacon(score1))
            else:
                score0 += take_turn(num_rolls, score1, select_dice(score0, score1))
        else:
            num_rolls = strategy1(score1, score0)
            if num_rolls == 0:
                score1 += primenize(free_bacon(score0))
            else:
                score1 += take_turn(num_rolls, score0, select_dice(score1, score0))
        if is_swap(score0, score1):
            score0, score1 = score1, score0
        player = other(player)
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    score0 = 0
    while score0 < goal:
        score1 = 0
        while score1 < goal:
            num_rolls = strategy(score0, score1)
            check_strategy_roll(score0, score1, num_rolls)
            score1 += 1
        score0 += 1
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    def average(*args):
        total = 0
        for i in range(0, num_samples):
            total += fn(*args)
        total /= num_samples
        return total
    return average
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    num_rolls = 0
    average = 0
    n = 10
    roll_dice_average = make_averaged(roll_dice, num_samples)
    while n > 0:
        num = roll_dice_average(n, dice)
        if num >= average:
            average = num
            num_rolls = n
        n -= 1
    return num_rolls
    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(4) win rate:', average_win_rate(always_roll(4)))

    if False:  # Change to True to test always_roll(8)
        print('always_roll(1) win rate:', average_win_rate(always_roll(1)))

    if False:  # Change to True to test always_roll(8)
        print('always_roll(2) win rate:', average_win_rate(always_roll(2)))

    if False:  # Change to True to test always_roll(8)
        print('always_roll(3) win rate:', average_win_rate(always_roll(3)))

    if False:  # Change to True to test always_roll(8)
        print('always_roll(5) win rate:', average_win_rate(always_roll(5)))

    if False:  # Change to True to test always_roll(8)
        print('always_roll(6) win rate:', average_win_rate(always_roll(6)))

    if False:  # Change to True to test always_roll(8)
        print('always_roll(7) win rate:', average_win_rate(always_roll(7)))

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test always_roll(8)
        print('always_roll(9) win rate:', average_win_rate(always_roll(9)))

    if False:  # Change to True to test always_roll(8)
        print('always_roll(10) win rate:', average_win_rate(always_roll(10)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:
        print('final_strategy win rate: ', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    my_score = 0
    my_score = free_bacon(opponent_score)
    my_score = primenize(my_score)
    if my_score >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    my_score = 0
    my_score = free_bacon(opponent_score)
    my_score = primenize(my_score)
    if opponent_score == 2 * (score + my_score):
        return 0
    elif my_score >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    with a aid function expectation, which returns the expected value of rolling
    n numbers of dies by simulation of rowing 1000 times and take the average of
    the value. Then set all inintal value to default. The default strategy is
    swing strategy. Then if the total score of current score plus free bacon score
    exceed 100 and will not cause negatvie swing swap, then roll 0 die and win the
    game. Then determine the beneficial swing swap. If the total score of current
    score and free bacon score whill cause a beneficial swing swap, then roll
    0 die. Or if the addition of 1 point or 3 points will cause a swing swap,
    then roll 10 or 9 dies respectively. This is because rolling 10 dies and 9 dies
    have high enough possibilities of earning 1 point and 3 points. Then if the points
    earned by rolling 0 die will cause opponent use 4 sided die and the total score
    will not cause a negative swing swap, roll 0 die. Last, if the expected value
    of rolling dies is greater than points earned by rolling 0 die, roll smallest
    numbers of dies possible. For default strategy: roll 6 dies if using six
    sided die, and roll 4 dies if using four sided die. Using margin of 11 before
    score is 90 and use margin of 9 if score is greater than 90.
    """
    # BEGIN PROBLEM 11
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
    # END PROBLEM 11
check_strategy(final_strategy)


def expectation(n, score, opponent_score):
    average_turn = make_averaged(roll_dice, 1000)
    if (score + opponent_score) % 7 == 0:
        expected_value = average_turn(n, four_sided)
    else:
        expected_value = average_turn(n, six_sided)
    return expected_value



##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
