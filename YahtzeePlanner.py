"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor

codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """

    max_score = 0
    for die_num in hand:
        temp_score = hand.count(die_num) * die_num
        if max_score < temp_score:
            max_score = temp_score
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    outcomes = [x for x in range(1, num_die_sides + 1)]
    new_rolls = gen_all_sequences(outcomes, num_free_dice)
    total_score = 0
    for roll in new_rolls:
        total_score += score(held_dice + roll)
    return float(total_score) / float(len(new_rolls))


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    answer_set = set([()])
    answer_set.add(hand)
    for dummy_length in range(len(hand), 0, -1):
        temp_set = answer_set.copy()
        for hold_choice in temp_set:
            if len(hold_choice) == dummy_length:
                new_seq = list(hold_choice)
                for dummy_idx in range(len(new_seq)):
                    del_seq = new_seq[:]
                    del del_seq[dummy_idx]
                    answer_set.add(tuple(del_seq))

    return answer_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """

    hold_set = gen_all_holds(hand)
    best_score = 0
    for chosen_hold in hold_set:
        chosen_value = expected_value(chosen_hold, num_die_sides, len(hand) - len(chosen_hold))
        if chosen_value > best_score:
            best_score = chosen_value
            best_hold = chosen_hold
    return (best_score, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 2)
    hand_score, hold = strategy(hand, num_die_sides)
    print
    "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()
# run_suite(expected_value)
# expected_value(2,6,2)

# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)