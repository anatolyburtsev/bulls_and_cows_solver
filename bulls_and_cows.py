__author__ = 'onotole'
import itertools
import logging
import config
import time
import doctest
import random

logging.basicConfig(format=config.logging_format, level=config.logging_level, filename=config.logging_filename)


def set_from_integer(number):
    """
    get set with digits from number
    >>> set_from_integer(1111)
    {'1'}

    # here should be more complicated test, but I don't know how to compare set in doctest:
    #according doctest: {'1', '2' } != {'2', '1'}
    """
    result_set = set()
    for letter in str(number):
            result_set.add(letter)
    return result_set


def check_number_for_numeral(number, numeral=0):
    """
    count how many times numeral includes in number
    >>> check_number_for_numeral(1231139, 1)
    3
    """

    count = 0
    numeral = str(numeral)
    for i in str(number):
        if i == numeral:
            count += 1
    return count


def generate_number_without_repetition(digits=4):
    """
    generate random number withour repetition, ex. 1234
    >>> 999 < generate_number_without_repetition(4) < 10000
    True
    >>> len(set_from_integer(generate_number_without_repetition(4)))
    4
    """
    assert digits < 10
    digits_list = list(range(1,10))
    result = random.choice(digits_list)
    digits_list.remove(result)
    digits_list.append(0)
    while len(str(result)) != digits:
        result *= 10
        next_digit = random.choice(digits_list)
        digits_list.remove(next_digit)
        result += next_digit
    return result


def generate_available_integers_list(digits=4):
    start_time = time.time()
    result_list = []
    for i in range(10 ** (digits-1), 10 ** digits):
        uniq_set = set_from_integer(i)
        if len(uniq_set) == digits:
            result_list.append(i)

    logging.debug("sequence generated in " + str(time.time() - start_time) + " sec!")
    return result_list


def check_two_numbers_for_bulls(number1, number2):
    """
    return count of digits which match in value and position in both numbers
    >>> check_two_numbers_for_bulls(1234, 5214)
    2
    >>> check_two_numbers_for_bulls(1234, 5678)
    0
    >>> check_two_numbers_for_bulls(1234, 2341)
    0
    >>> check_two_numbers_for_bulls(7890, 7890)
    4
    """
    count = 0
    num1 = str(number1)
    num2 = str(number2)
    for i in range(max(len(num1), len(num2))):
        if num1[i] == num2[i]:
            count += 1
    return count


def check_two_numbers_for_cows_and_bulls(number1, number2):
    """
    return count of digits which match in value in both numbers. Included bulls
    >>> check_two_numbers_for_cows_and_bulls(1234, 5214)
    3
    >>> check_two_numbers_for_cows_and_bulls(1234, 2341)
    4
    >>> check_two_numbers_for_cows_and_bulls(1234, 7890)
    0
    """
    cows = 0
    num1 = set_from_integer(number1)
    num2 = set_from_integer(number2)
    return len(num1 & num2)


def compare_two_numbers(number1, number2):
    bulls = check_two_numbers_for_bulls(number1, number2)
    cows = check_two_numbers_for_cows_and_bulls(number1, number2) - bulls
    return [bulls, cows]


def reduce_available_list_with_bulls_and_cows(number, bulls, cows, available_numbers_list):
    """
    check all numbers in list for match with pattern
    >>> reduce_available_list_with_bulls_and_cows(1234, 1, 2, [1234,1235, 1326,2318])
    [1326]
    >>> reduce_available_list_with_bulls_and_cows(1620, 1, 1, [1620, 1623, 9140, 9143])
    [9140]
    """
    assert type(available_numbers_list) == list
    result_list = []
    for i in available_numbers_list:
        if compare_two_numbers(number, i) == [bulls, cows]:
            result_list.append(i)
    return result_list


def start_game():
    current_available_list = generate_available_integers_list()
    steps = 1
    while len(current_available_list) > 0:
        print("\nnow " + str(len(current_available_list)) + " numbers in list of available numbers")
        number = random.choice(current_available_list)
        print("I guess it's number: " + str(number))
        try:
            bulls = int(input("bulls:"))
            cows = int(input("cows:"))
        except ValueError:
            print("don't try to cheat me, enter just numbers!")
            continue

        if bulls + cows > len(str(number)) or bulls < 0 or cows < 0:
            print("don't try to cheat me, enter correct numbers of bulls and cows!")
            continue

        if bulls == len(str(number)):
            print("\nYES!!! I'm sexy and I know it!")
            print("win in " + str(steps) + " steps!")
            logging.info("win in " + str(steps) + " steps!")
            return True

        current_available_list.remove(number)
        current_available_list = reduce_available_list_with_bulls_and_cows(number, bulls, cows, current_available_list)
        if len(current_available_list) == 1:
            print("\nYES!!! I know!!! I know!!!")
            print("It's number: " + str(current_available_list[0]))
            logging.info("win in " + str(steps) + " steps!")
            return True
        steps += 1
    print("It's looks like somebody tried to cheat me! ATATATA")

if __name__ == '__main__':
    doctest.testmod()
    start_game()
