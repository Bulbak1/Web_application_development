import subprocess
import pytest

# Для Windows
INTERPRETER = 'python'
# Для MAC
# INTERPRETER = 'python3'

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'python_if_else': [
        ('0', 'Неверное значение'),
        ('101', 'Неверное значение'),
        ('1', 'Weird'),
        ('4', 'Not Weird'),
        ('3', 'Weird'),
        ('6','Weird'),
        ('22', 'Not Weird'),
        ('100', 'Not Weird')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3.0', '-1.0', '2.0']),
        (['10', '5'], ['15.0', '5.0', '50.0']),
        (['1', '1'], ['2.0', '0.0', '1.0']),  
        (['1010', '1010'], ['2020.0', '0.0', '1020100.0']),
        (['10000000000', '10000000000'], ['20000000000.0', '0.0', '1e+20']),
        (['1', '10000000000'], ['10000000001.0', '-9999999999.0', '10000000000.0']),
        (['1000', '500'], ['1500.0', '500.0', '500000.0']),
        (['999', '1'], ['1000.0', '998.0', '999.0']),
        (['0', '5'], ['Неверное значение']), # a < 1
        (['5', '0'], ['Неверное значение']), # b < 1
        (['10000000001', '5'], ['Неверное значение']), # a > 10^10
        (['5', '10000000001'], ['Неверное значение']), # b > 10^10
    ],

    'division': [
        (['3', '5'], ['0', '0.6']),
        (['10', '2'], ['5', '5.0']),
        (['7', '3'], ['2', '2.3333333333333335']),
        
        (['5', '0'], ['Деление на ноль!', 'Деление на ноль!']),
        (['0', '0'], ['Деление на ноль!', 'Деление на ноль!']),
        
        (['-10', '3'], ['-4', '-3.3333333333333335']),
        (['10', '-3'], ['-4', '-3.3333333333333335']),
        (['-10', '-3'], ['3', '3.3333333333333335']),
        
        (['1000', '7'], ['142', '142.85714285714286']),
        (['0', '5'], ['0', '0.0']),
    ],

    'loops': [
        (['1'], ['0']),
        (['20'], [ '0', '1', '4', '9', '16', '25', '36', '49', '64', '81','100', '121', '144', '169', '196', '225', '256', '289', '324', '361']),
        (['3'], ['0', '1', '4']),
        (['2'], ['0', '1']),
        (['4'], ['0', '1', '4', '9']),
        (['5'], ['0', '1', '4', '9', '16']),
        (['6'], ['0', '1', '4', '9', '16', '25']),
        (['7'], ['0', '1', '4', '9', '16', '25', '36']),
        (['8'], ['0', '1', '4', '9', '16', '25', '36', '49']),
        (['9'], ['0', '1', '4', '9', '16', '25', '36', '49', '64']),
        (['10'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81']),
        (['11'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81', '100']),
        (['12'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81', '100', '121']),
        (['13'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81', '100', '121', '144']),
        (['14'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81', '100', '121', '144', '169']),
        (['15'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81', '100', '121', '144', '169', '196']),
        (['0'], ['Неверное значение']),  # n < 1
        (['21'], ['Неверное значение']),  # n > 20
    ],

    'print_function': [
        (['1'], '1'),
        (['20'], '1234567891011121314151617181920'),
        (['2'], '12'),
        (['3'], '123'),
        (['4'], '1234'),
        (['5'], '12345'),
        (['6'], '123456'),
        (['7'], '1234567'),
        (['8'], '12345678'),
        (['9'], '123456789'),
        (['10'], '12345678910'),
        (['11'], '1234567891011'),
        (['12'], '123456789101112'),
        (['13'], '12345678910111213'),
        (['14'], '1234567891011121314'),
        (['15'], '123456789101112131415'),
        (['0'], 'Неверное значение'),  # n < 1
        (['21'], 'Неверное значение'),  # n > 20
    ],

    'second_score': [
        (['5', '2 3 6 6 5'], '5'),
        (['3', '1 2 3'], '2'),
        (['4', '10 20 30 40'], '30'),
        (['6', '5 5 5 4 4 3'], '4'),
        (['7', '100 200 300 400 500'], '400'),
        (['5', '10 10 8 7 6'], '8'),
        (['6', '9 9 9 5 4 3'], '5'),
        (['2', '1 2'], '1'),
        (['2', '5 5'], 'Ошибка: недостаточно уникальных значений'),
    ],

    'nested_list': [
        # Пример из условия
        (['5', 'Гарри', '37.21', 'Берри', '37.21', 'Тина', '37.2', 'Акрити', '41', 'Харш', '39'], ['Берри', 'Гарри']),

        # Один студент со второй оценкой
        (['3', 'Иван', '3.0', 'Мария', '4.0', 'Петр', '5.0'], ['Мария']),
        
        # Несколько студентов с одинаковой второй оценкой
        (['4', 'Анна', '4.5', 'Борис', '3.5', 'Виктор', '4.5', 'Глеб', '4.0'], ['Глеб']),
        
        # Минимальное количество студентов
        (['2', 'Алиса', '2.0', 'Боб', '3.0'], ['Боб']),
        
        # Максимальное количество студентов
        (['5', 'a', '1.0', 'b', '2.0', 'c', '2.0', 'd', '3.0', 'e', '4.0'], ['b', 'c']),
        
        # Отрицательные оценки
        (['4', 'Первый', '-1.0', 'Второй', '-2.0', 'Третий', '0.0', 'Четвертый', '1.0'], ['Первый']),
        
        # Очень близкие оценки
        (['4', 'A', '3.3333333', 'B', '3.3333334', 'C', '3.3333335', 'D', '3.3333336'], ['B']),

        (['5', 'Денис', '1.0', 'Иван', '2.0', 'Петр', '2.0', 'Мария', '2.0', 'Анна', '3.0'],['Иван','Мария','Петр']),

        (['6', 'Денис', '1.0', 'Иван', '2.0', 'Петр', '2.0', 'Мария', '2.0', 'Анна', '3.0', 'Борис', '3.5'],['Ошибка: количество студентов должно быть от 2 до 5']),

        (['1', 'Тест', '5.0'], ['Ошибка: количество студентов должно быть от 2 до 5']),
        
        # Все оценки одинаковые - должно вызвать ошибку
        (['3', 'Один', '5.0', 'Два', '5.0', 'Три', '5.0'], ['Ошибка: недостаточно уникальных оценок']),
    ],

    'lists': [
        # Пример из условия
        (['12', 'insert 0 5', 'insert 1 10', 'insert 0 6', 'print',
        'remove 6', 'append 9', 'append 1', 'sort', 'print',
        'pop', 'reverse', 'print'],
        ['[6, 5, 10]', '[1, 5, 9, 10]', '[9, 5, 1]']),
        
        # Только print пустого списка
        (['1', 'print'],['[]']),
        
        # Все команды по одной
        (['7', 'append 5', 'append 3', 'sort', 'print', 'pop', 'reverse', 'print'],
        ['[3, 5]', '[3]']),
        
        # insert в начало и конец 
        (['6', 'insert 0 1', 'insert 1 2', 'insert 2 3', 'print', 'insert 0 0', 'print'],['[1, 2, 3]', 
        '[0, 1, 2, 3]']),
        
        # неверная команда
        (['1', 'invalid'],['Неизвестная команда: invalid']),
        
        # аргумент не целое число
        (['1', 'append abc'],['Ошибка: аргумент должен быть целым числом']),
    ],

    'swap_case': [
        (['Www.MosPolytech.ru'], 'wWW.mOSpOLYTECH.RU'),
        (['Pythonist 2'], 'pYTHONIST 2'),
        (['HelloWorld'], 'hELLOwORLD'),
        (['abcdef'], 'ABCDEF'),
        (['ABCDEF'], 'abcdef'),
        (['PyThOn'], 'pYtHoN'),
        (['TeXt'], 'tExT'),
        (['123456'], '123456'),
        (['!@#$%'], '!@#$%'),
        (['Hello123!'], 'hELLO123!'),
        (['Hello World'], 'hELLO wORLD'),
        (['Python'], 'pYTHON'), 
        (['МосПолитех'], 'мОСпОЛИТЕХ'),
        (['Hello, Мир! 123'], 'hELLO, мИР! 123'),
        (['a' * 1000], 'A' * 1000),  # Максимальная длина 1000
        (['A' * 1000], 'a' * 1000),  # Максимальная длина 1000
        
        # Проверка ограничения длины (больше 1000)
        (['a' * 1001], 'Ошибка: длина строки должна быть от 1 до 1000 символов'),
        (['a'], 'A'),
    ],

    'split_and_join': [
        # Пример из условия
        (['this is a string'], 'this-is-a-string'),
        (['hello'], 'hello'),
        # Несколько пробелов
        (['a   b   c'], 'a-b-c'),
        (['multiple    spaces    here'], 'multiple-spaces-here'),
        # Пробелы в начале и конце
        (['  leading spaces'], 'leading-spaces'),
        (['trailing spaces  '], 'trailing-spaces'),
        (['  both sides  '], 'both-sides'),
        # Пустая строка
        ([''], ''),
        # Только пробелы
        (['   '], ''),
        # Специальные символы
        (['hello, world!'], 'hello,-world!'),
        (['a b c d'], 'a-b-c-d'),
        (['привет мир'], 'привет-мир'),
        (['Москва Питер'], 'Москва-Питер'),
        (['word ' * 500], '-'.join(['word'] * 500)),
    ],

    'anagram': [
        (['listen', 'silent'], 'YES'),
        (['abc', 'cba'], 'YES'),
        (['aabb', 'abab'], 'YES'),
        (['123', '321'], 'YES'),
        (['!@#', '#@!'], 'YES'),
        (['abc', 'def'], 'NO'),
        (['hello', 'world'], 'NO'),
        (['abc', 'abcd'], 'NO'),  # разная длина
        (['aab', 'abb'], 'NO'),
    ],

    'metro': [
        (['1', '10 20', '15'], '1'),
        (['1', '10 20', '5'], '0'),
        (['1', '10 20', '10'], '1'),
        (['3', '5 15', '10 20', '25 35', '12'], '2'),
        (['4', '0 10', '5 15', '20 30', '25 35', '10'], '2'),
        (['2', '10 20', '15 25', '22'], '1'),
        (['0', '5'], '0'),
        (['1', '20 10', '15'], 'Ошибка: время входа (20) должно быть меньше времени выхода (10)'),
    ],

    'minion_game': [
        (['BANANA'], 'Stuart 12'),
        (['AEIOU'], 'Kevin 15'),
        (['BCDFG'], 'Stuart 15'),
        (['A'], 'Kevin 1'),
        (['B'], 'Stuart 1'),
        (['ABC'], 'Draw'),
        (['A' * 1000000], 'Kevin 500000500000'),

        (['banana'], 'Error'),
        (['BANANA123'], 'Error'),
        (['A' * 1000001], 'Error'),
    ],

    'is_leap': [
        #Граница минимум
        (['1900'], 'False'),
        
        #Граница максимум
        (['100000'], 'True'),
        
        #Делится на 400
        (['2000'], 'True'),
        
        #Делится на 400
        (['2400'], 'True'),
        
        # Делится на 100, но не на 400
        (['2100'], 'False'),
        
        # Делится на 100, но не на 400
        (['2200'], 'False'),
        
        # Делится на 4, но не на 100
        (['2016'], 'True'),
        
        # Делится на 4, но не на 100
        (['2020'], 'True'),
        
        # Делится на 4, но не на 100
        (['2024'], 'True'),
        
        # Не делится на 4
        (['2017'], 'False'),
        
        # Не делится на 4
        (['2019'], 'False'),
        
        # Год вне диапазона < 1900
        (['1899'], 'Error'),
        
        # Год вне диапазона > 100000
        (['100001'], 'Error'),   
    ],

    'happiness': [
        (['3 2', '1 5 3', '3 1', '5 7'], '1'),
        (['5 2', '1 1 1 2 2', '1 2', '3 4'], '5'),# Повторяющиеся элементы
        (['3 2', '1 2', '3 1', '5 7'], 'Error'),# несовпадение длины массива
        (['3 2', '1 1000000000 10000000000', '3 1', '5 7'], 'Error'),# элемент вне диапазона
        (['3 2', '1 5 3', '3 1', '1 7'], 'Error'), # множества пересекаются
        (['0 2', '1 5 3', '3 1', '5 7'], 'Error'), # n вне диапазона
        (['5 0', '1 2 3', '1', '2'], 'Error'),#m < 1
        (['0 5', '1', '1', '2'], 'Error'),#n < 1
        (['1 1', '1', '1', '2'], '1'),#граница
        (['3 3', '1000000000 1000000000 1000000000', '1000000000 999999999 999999998', '1 2 3'], '3')#граница
    ],

    'pirate_ship': [
        
    # ТЕСТ 1: Один груз, полностью помещается
        (['10 1', 'Золото 5 100'], 'Золото 5 100'),# Один груз, полностью помещается
        (['10 1', 'Золото 20 100'], 'Золото 10 50.00'),# Один груз, частично
        (['15 2', 'Золото 5 100', 'Серебро 8 120'], 'Золото 5 100\nСеребро 8 120'),# Несколько грузов, все помещаются
        (['15 3', 'Платина 6 180', 'Золото 5 100', 'Серебро 8 120'], 'Платина 6 180\nЗолото 5 100\nСеребро 4 60.00'),# Несколько грузов, последний частично
        (['10 3', 'Алмазы 4 80', 'Золото 4 60', 'Серебро 4 40'], 'Алмазы 4 80\nЗолото 4 60\nСеребро 2 20.00'),# Сортировка по ценности (более ценные грузы идут первыми)
        (['0 2', 'Золото 5 100', 'Серебро 8 120'], ''), # Грузоподъёмность 0
    ],

    'matrix_mult': [
        (['2', '1 2', '3 4', '5 6', '7 8'], ['19 22', '43 50']),  # граница: минимум n=2
        (['2', '1 0', '0 1', '2 3', '4 5'], ['2 3', '4 5']),
        (['3', '1 2 3', '4 5 6', '7 8 9', '9 8 7', '6 5 4', '3 2 1'], ['30 24 18', '84 69 54', '138 114 90']),
        (['10', '1 0 0 0 0 0 0 0 0 0', '0 1 0 0 0 0 0 0 0 0', '0 0 1 0 0 0 0 0 0 0', '0 0 0 1 0 0 0 0 0 0', '0 0 0 0 1 0 0 0 0 0', '0 0 0 0 0 1 0 0 0 0', '0 0 0 0 0 0 1 0 0 0', '0 0 0 0 0 0 0 1 0 0', '0 0 0 0 0 0 0 0 1 0', '0 0 0 0 0 0 0 0 0 1',
        '1 2 3 4 5 6 7 8 9 10', '10 9 8 7 6 5 4 3 2 1', '1 1 1 1 1 1 1 1 1 1', '2 2 2 2 2 2 2 2 2 2', '3 3 3 3 3 3 3 3 3 3', '4 4 4 4 4 4 4 4 4 4', '5 5 5 5 5 5 5 5 5 5', '6 6 6 6 6 6 6 6 6 6', '7 7 7 7 7 7 7 7 7 7', '8 8 8 8 8 8 8 8 8 8'], 
        ['1 2 3 4 5 6 7 8 9 10', '10 9 8 7 6 5 4 3 2 1', '1 1 1 1 1 1 1 1 1 1', '2 2 2 2 2 2 2 2 2 2', '3 3 3 3 3 3 3 3 3 3', '4 4 4 4 4 4 4 4 4 4', '5 5 5 5 5 5 5 5 5 5', '6 6 6 6 6 6 6 6 6 6', '7 7 7 7 7 7 7 7 7 7', '8 8 8 8 8 8 8 8 8 8']),  # граница: максимум n=10
        (['1'], ['Error']),  # n < 2
        (['11'], ['Error']),  # n > 10    
    ]
}

def test_hello_world():
    assert run_script('hello_world.py') == 'Hello, world!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['second_score'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested_list(input_data, expected):
    assert run_script('nested_list.py', input_data) == '\n'.join(expected)

@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_lists(input_data, expected):
    assert run_script('lists.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['swap_case'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['split_and_join'])
def test_split_and_join(input_data, expected):
    assert run_script('split_and_join.py', input_data) == expected

def test_max_word():
    result = run_script('max_word.py', [])
    expected = "сосредоточенности"
    assert result.strip() == expected

def test_price_sum():
    result = run_script('price_sum.py')
    assert result == '6842.84 5891.06 6810.90'

@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['metro'])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['minion_game'])
def test_minion_game(input_data, expected):
    assert run_script('minion_game.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['pirate_ship'])
def test_pirate_ship(input_data, expected):
    result = run_script('pirate_ship.py', input_data)
    assert result == expected

@pytest.mark.parametrize("input_data, expected", test_data['matrix_mult'])
def test_matrix_mult(input_data, expected):
    assert run_script('matrix_mult.py', input_data).split('\n') == expected