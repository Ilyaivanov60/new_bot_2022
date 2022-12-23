from utils import get_bot_number, play_random_numbers


def test_get_bot_number():
    user_number = 10
    assert (user_number - 10) <= get_bot_number(user_number) <= (user_number + 10)


def test_play_random_numbers_win():
    assert play_random_numbers(10, 5) == "Ваше число 10, мое 5, вы выйграли!"


def test_play_random_numbers_lose():
    assert play_random_numbers(5, 10) == "Ваше число 5, мое 10, вы проиграли!"


def test_play_random_numbers_even():
    assert play_random_numbers(5, 5) == "Ваше число 5, мое 5, ничья!"
