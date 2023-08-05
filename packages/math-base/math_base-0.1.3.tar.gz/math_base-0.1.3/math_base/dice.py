from .math_base import combination

DICE_FACE = 6


def probability_same_number(num_dice: int, num_same: int) -> float:
    """
    probability same number

    @param num_dice: number of dice
    @param num_same: number of same number
    """
    comb = combination(num_dice, num_dice)

    initial = (1 / DICE_FACE) ** num_same

    for i in range(5, num_same, -1):
        initial *= i / DICE_FACE

    return comb * initial

if __name__ == "__main__":
    ret = probability_same_number(5, 2)
    print(ret)
