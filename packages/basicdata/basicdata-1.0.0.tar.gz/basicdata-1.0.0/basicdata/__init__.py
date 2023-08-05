lower_case_letters = [chr(i) for i in range(97, 123)]
upper_case_letters = [chr(i) for i in range(65, 91)]
letters = lower_case_letters + upper_case_letters
number_digits = [i for i in range(10)]
ascii_of_lower_case_letters = {chr(i): i for i in range(97, 123)}
ascii_of_upper_case_letters = {chr(i): i for i in range(65, 91)}
order_of_lower_case_letters = {chr(i): i - 96 for i in range(97, 123)}
order_of_upper_case_letters = {chr(i): i - 64 for i in range(65, 91)}
ascii_of_lower_case_letters_reverse = {i: chr(i) for i in range(97, 123)}
ascii_of_upper_case_letters_reverse = {i: chr(i) for i in range(65, 91)}
order_of_lower_case_letters_reverse = {i - 96: chr(i) for i in range(97, 123)}
order_of_upper_case_letters_reverse = {i - 64: chr(i) for i in range(65, 91)}
english_symbols = [
    '~', '`', '!', '@', '#', '$', '%', '^',
    '&', '*', '(', ')', '-', '_', '=', '+',
    '{', '}', '[', ']', '|', '\\', ':', ';',
    '"', "'", ',', '<', '>', '.', '?', '/'
]
chinese_symbols = [
    '~', '·', '！', '@', '#', '￥', '%', '……',
    '&', '*', '（', '）', '-', '——', '=', '+',
    '{', '}', '【', '】', '|', '、', '：', '；',
    '“', '‘', '，', '《', '》', '。', '？', '、'
]
symbols = english_symbols + chinese_symbols


def type_of_object(object):
    types = [bool, int, float, str, list, tuple, set, dict]
    types_str = ['int', 'float', 'str', 'list', 'tuple', 'set', 'dict', 'bool']
    for index, value in enumerate(types):
        if isinstance(object, value):
            return types_str[index]


def is_one_letter(object):
    if len(object) == 1:
        if object in letters:
            return True
        else:
            return False
    else:
        raise ValueError('the length of param object should be one')


def is_all_letter(object):
    lst = []
    for letter in object:
        if letter in letters:
            lst.append(True)
        else:
            lst.append(False)
    return all(lst)


def is_special_symbols(object):
    if len(object) == 1:
        if object in symbols:
            return True
        else:
            return False
    else:
        raise ValueError('the length of param object should be one')


def is_valid_phone_num(number: (str, int)):
    if len(number) == 11:
        if isinstance(number, str):
            pass
        elif isinstance(number, int):
            number = str(number)
        else:
            raise ValueError('number should be string or integer')
        lst = []
        for i, d in enumerate(number):
            if i == 0:
                if d == 1:
                    lst.append(True)
                else:
                    lst.append(False)
            else:
                if d in number_digits:
                    lst.append(True)
                else:
                    lst.append(False)
        return all(lst)
    else:
        raise ValueError('the length of the param number should be eleven')
