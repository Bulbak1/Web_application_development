import subprocess
import pytest
import math
import os

from fact import fact_it, fact_rec
from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list, process_list_lc, process_list_gen
from my_sum import my_sum
from email_validation import fun
from average_scores import compute_average_scores
from plane_angle import Point, plane_angle
from phone_number import sort_phone
from log_decorator import function_logger

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
    'test_data_it' :[
        (1, 1),
        (2, 2),
        (5, 120),
        (7, 5040),
        (10, 3628800),
        (0, "Error"),   # n < 1
        (-10, "Error"),  # n < 1
        (1010, "Error"),  # n >= 1000
    ],

    'test_data_rec' : [
        (1, 1),
        (2, 2),
        (5, 120),
        (7, 5040),
        (10, 3628800),
        (0, "Error"),   # n < 1
        (-7, "Error"),  # n < 1
        (1000, "Error"),  # n >= 1000
    ],

    'test_data_employee': [
        (("Иванов Иван Иванович", 50000), "Иванов Иван Иванович: 50000 ₽"),
        (("Петров Петр Петрович", 75000), "Петров Петр Петрович: 75000 ₽"),
        (("Сидорова Анна Сергеевна", 120000), "Сидорова Анна Сергеевна: 120000 ₽"),
        (("Имя Фамилия Отчество", 0), "Имя Фамилия Отчество: 0 ₽"),
        (("Тест Тестович", -5000), "Тест Тестович: -5000 ₽"),
        (("Иванов Иван Иванович",), "Иванов Иван Иванович: 100000 ₽"),
        (("Петров Петр Петрович",), "Петров Петр Петрович: 100000 ₽"),
        (("Сидорова Анна Сергеевна",), "Сидорова Анна Сергеевна: 100000 ₽"),
        (("",), ": 100000 ₽"),
    ],

    'test_data_sum_and_sub': [
        ((5, 3), (8, 2)),
        ((10, 7), (17, 3)),         
        ((-5, 3), (-2, -8)),         
        ((5, -3), (2, 8)),           
        ((-5, -3), (-8, -2)),        
        ((0, 5), (5, -5)),           
        ((5, 0), (5, 5)),            
        ((0, 0), (0, 0)),            
        ((2.5, 1.5), (4.0, 1.0)),    
        ((-2.5, 1.5), (-1.0, -4.0)), 
        ((1000000, 1), (1000001, 999999)),  
    ],

    'process_list': [
        (([1, 2, 3, 4, 5],), [1**3, 2**2, 3**3, 4**2, 5**3]),
        (([2, 4, 6, 8],), [4, 16, 36, 64]),
        (([1, 3, 5, 7],), [1, 27, 125, 343]),
        (([0],), [0]),
        (([-1, -2, -3, -4],), [-1, 4, -27, 16]),
        (([10],), [100]),
        (([1],), [1]),
        ((list(range(1, 1002)),), "Error"),
        (([],), "Error"),
    ],

    'my_sum': [
        ((1, 2), 3),
        ((1, 2, 3, 4, 5), 15),
        ((), 0),
        ((1.5, 2.5, 3.0), 7.0),
        ((-1, -2, -3), -6),
        ((5,), 5),
        ((1000, 2000, 3000), 6000),
        ((10, -5, 3, -2), 6),
    ],

    #python my_sum_argv.py 1 2 3 4 5
    # 15
    #python my_sum_argv.py 1.5 2.5 3.5
    # 7.5
    #python my_sum_argv.py 1
    # 1
    
    #python files_sort.py test_folder

    #python file_search.py file1.txt

    'test_email_validation': [
    # Корректные email
    ("lara@mospolytech.ru", True),
    ("brian-23@mospolytech.ru", True),
    ("britts_54@mospolytech.ru", True),
    ("user123@website.com", True),
    
    # Некорректные email
    ("lara@mospolytech.rrrr", False),  # >3
    ("lara@mospolytech.r12", False),   # с цифрами
    ("lara@.ru", False),                # нет website
    ("lara@mospolytechru", False),      # нет точки
    ("test@exam!ple.com", False),
    ],

    'fibonacci': [
        (1, [0]),              # 0^3 = 0
        (2, [0, 1]),           # 0^3, 1^3
        (3, [0, 1, 1]),        # 0, 1, 1
        (4, [0, 1, 1, 8]),     # 0, 1, 1, 2^3=8
        (5, [0, 1, 1, 8, 27]), # 0, 1, 1, 8, 3^3=27
        (6, [0, 1, 1, 8, 27, 125]),  # 5^3=125
        (7, [0, 1, 1, 8, 27, 125, 512]),  # 8^3=512
        (8, [0, 1, 1, 8, 27, 125, 512, 2197]),  # 13^3=2197
        (9, [0, 1, 1, 8, 27, 125, 512, 2197, 9261]),  # 21^3=9261
        (10, [0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304]),  # 34^3=39304
        (15, [0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304, 166375, 704969, 2985984, 12649337, 53582633]),
    ],

    'test_average_scores': [
        (([(89, 90, 78, 93, 80),
        (90, 91, 85, 88, 86),
        (91, 92, 83, 89, 90.5)],), 
        (90.0, 91.0, 82.0, 90.0, 85.5)),
        
        (([(85,), (90,), (95,)],), (90.0,)),
        
        (([(70, 80, 90)],), (70.0, 80.0, 90.0)),
        
        (([(75, 75), (75, 75)],), (75.0, 75.0)),

        (([],), "Error"),
        (([(1, 2), (3,)],), "Error"),
        (([(1, 2, 3)] * 101,), "Error"),
    ],

    'point_sub': [
        ((5, 3, 2, 1, 1, 1), (4, 2, 1)),
        ((-1, -2, -3, -4, -5, -6), (3, 3, 3)),
    ],

    'phone_number': [
        (["89991234567"], ["+7 (999) 123-45-67"]),      # начинается с 8
        (["9991234567"], ["+7 (999) 123-45-67"]),       # без префикса (10 цифр)
        (["+7(999)123-45-67"], ["+7 (999) 123-45-67"]), # уже с +7, но с символами
        
        (["89991234567", "84951112233"],
        ["+7 (495) 111-22-33", "+7 (999) 123-45-67"]),

        (["89998887766", "74952223344", "9261112233"],
        ["+7 (495) 222-33-44", "+7 (926) 111-22-33", "+7 (999) 888-77-66"]),
        
        (["8(916)5554433", "8(925)6667788", "8(977)8889999"],
        ["+7 (916) 555-44-33", "+7 (925) 666-77-88", "+7 (977) 888-99-99"]),
    ],

    'people_sort': [
        (["Mike Thomson 20 M", "Robert Bustle 32 M", "Andria Bustle 30 F"],
        ["Mr. Mike Thomson", "Ms. Andria Bustle", "Mr. Robert Bustle"]),

        (["John Doe 25 M", "Jane Smith 25 F"],
        ["Mr. John Doe", "Ms. Jane Smith"]),
        
        (["Ada Lovelace 30 F", "Marie Curie 35 F"],
        ["Ms. Ada Lovelace", "Ms. Marie Curie"]),
    ],

    'complex_operations': [
        # (c_real, c_imag, d_real, d_imag, ожидаемые результаты)
        ((2, 1, 5, 6), 
        ["7.00+7.00i", "-3.00-5.00i", "4.00+17.00i", "0.26-0.11i", "2.24+0.00i", "7.81+0.00i"]),
        
        ((1, 2, 3, 4),
        ["4.00+6.00i", "-2.00-2.00i", "-5.00+10.00i", "0.44+0.08i", "2.24+0.00i", "5.00+0.00i"]),
        
        ((5, 0, 2, 3),  # чисто действительное и комплексное
        ["7.00+3.00i", "3.00-3.00i", "10.00+15.00i", "0.77-1.15i", "5.00+0.00i", "3.61+0.00i"]),
        
        ((0, 1, 0, -1),  # чисто мнимые
        ["0.00+0.00i", "0.00+2.00i", "1.00+0.00i", "-1.00+0.00i", "1.00+0.00i", "1.00+0.00i"]),
    ],
    
}

@pytest.mark.parametrize("n, expected", test_data['test_data_it'])
def test_fact_it(n, expected):
    assert fact_it(n) == expected

@pytest.mark.parametrize("n, expected", test_data['test_data_rec'])
def test_fact_rec(n, expected):
    assert fact_rec(n) == expected

@pytest.mark.parametrize("args, expected", test_data['test_data_employee'])
def test_show_employee(args, expected):
    assert show_employee(*args) == expected

@pytest.mark.parametrize("args, expected", test_data['test_data_sum_and_sub'])
def test_sum_and_sub(args, expected):
    assert sum_and_sub(*args) == expected

@pytest.mark.parametrize("args, expected", test_data['process_list'])
def test_process_list(args, expected):
    result = process_list(*args)
    if expected == "Error":
        assert result == "Error"
    else:
        assert result == expected

@pytest.mark.parametrize("args, expected", test_data['process_list'])
def test_process_list_lc(args, expected):
    result = process_list_lc(*args)
    if expected == "Error":
        assert result == "Error"
    else:
        assert result == expected

@pytest.mark.parametrize("args, expected", test_data['process_list'])
def test_process_list_gen(args, expected):
    result = process_list_gen(*args)
    if expected == "Error":
        gen_list = list(result)
        assert gen_list[0] == "Error"
    else:
        assert list(result) == expected

@pytest.mark.parametrize("args, expected", test_data['my_sum'])
def test_my_sum(args, expected):
    assert my_sum(*args) == expected

@pytest.mark.parametrize("email, expected", test_data['test_email_validation'])
def test_email_validation(email, expected):
    assert fun(email) == expected

@pytest.mark.parametrize("n, expected", test_data['fibonacci'])
def test_fibonacci_cubes(n, expected):
    from fibonacci import fibonacci, cube
    result = list(map(cube, fibonacci(n)))
    assert result == expected

@pytest.mark.parametrize("args, expected", test_data['test_average_scores'])
def test_average_scores(args, expected):
    result = compute_average_scores(*args)
    if expected == "Error":
        assert result == "Error"
    else:
        # Округляем до 1 знака для сравнения
        rounded_result = tuple(round(r, 1) for r in result)
        assert rounded_result == expected

def test_average_scores_boundary_max():
    scores = [tuple([50.0] * 100) for _ in range(100)]  # граница: максимум X=100, N=100
    result = compute_average_scores(scores)
    assert result != "Error" and len(result) == 100

#--------------------------------------тесты для plane_angle---------------------------------------------------
def test_parallel_planes():
    A = Point(0, 0, 0)
    B = Point(1, 0, 0)
    C = Point(0, 1, 0)
    D = Point(1, 1, 0)
    assert round(plane_angle(A, B, C, D), 1) == 0.0

def test_example_from_task():
    A = Point(0, 0, 0)
    B = Point(1, 0, 0)
    C = Point(0, 1, 0)
    D = Point(0, 0, 1)
    assert round(plane_angle(A, B, C, D), 1) == 54.7

@pytest.mark.parametrize("input_data, expected", test_data['point_sub'])
def test_point_sub(input_data, expected):
    p1 = Point(input_data[0], input_data[1], input_data[2])
    p2 = Point(input_data[3], input_data[4], input_data[5])
    p3 = p1 - p2
    assert (p3.x, p3.y, p3.z) == expected

def test_point_dot():
    p1 = Point(1, 2, 3)
    p2 = Point(4, 5, 6)
    assert p1.dot(p2) == 32

def test_point_cross():
    p1 = Point(1, 0, 0)
    p2 = Point(0, 1, 0)
    p3 = p1.cross(p2)
    assert (p3.x, p3.y, p3.z) == (0, 0, 1)

def test_point_absolute():
    p = Point(3, 4, 0)
    assert p.absolute() == 5.0

def test_point_zero_vector():
    p = Point(0, 0, 0)
    assert p.absolute() == 0.0


@pytest.mark.parametrize("phones, expected", test_data['phone_number'])
def test_phone_number(phones, expected):
    result = sort_phone(phones)
    assert result == expected

@pytest.mark.parametrize("input_data, expected", test_data['people_sort'])
def test_people_sort(input_data, expected):
    n = str(len(input_data))
    result = run_script("people_sort.py", [n] + input_data)
    assert result.split('\n') == expected

@pytest.mark.parametrize("nums, expected", test_data['complex_operations'])
def test_complex_operations(nums, expected):
    from complex_numbers import Complex
    c_real, c_imag, d_real, d_imag = nums
    c = Complex(c_real, c_imag)
    d = Complex(d_real, d_imag)
    
    results = [
        str(c + d),
        str(c - d), 
        str(c * d),
        str(c / d),
        str(c.mod()),
        str(d.mod())
    ]
    
    assert results == expected

    #--------------------------------------
from circle_square_mk import circle_square_mk
def test_circle_square_mk_small():
    result = circle_square_mk(2, 5000)
    expected = math.pi * 4  # π * 4 ≈ 12.57
    assert abs(result - expected) < 2.0

def test_circle_square_mk_medium():
    #Тест со средним радиусом
    result = circle_square_mk(3, 10000)
    expected = math.pi * 9  # π * 9 ≈ 28.27
    assert abs(result - expected) < 3.0

def test_circle_square_mk_large():
    #Тест с большим радиусом
    result = circle_square_mk(5, 20000)
    expected = math.pi * 25  # π * 25 ≈ 78.54
    assert abs(result - expected) < 5.0

def test_circle_square_mk_zero():
    #Тест с нулевым радиусом
    result = circle_square_mk(0, 1000)
    assert result == 0

#----------------------log_decorator--------------------------

def test_log_decorator_writes_file(tmp_path):
    log_file = str(tmp_path / "test.log")

    @function_logger(log_file)
    def multiply(x, y):
        return x * y

    result = multiply(4, 7)
    assert result == 28
    assert os.path.exists(log_file)
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'multiply' in content
    assert '(4, 7)' in content
    assert '28' in content

def test_log_decorator_no_return(tmp_path):
    log_file = str(tmp_path / "test.log")

    @function_logger(log_file)
    def do_nothing():
        """Функция без возврата значения"""
        x = 42  # какая-то операция без return

    result = do_nothing()
    assert result is None
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'do_nothing' in content
    assert '-' in content  

def test_log_decorator_kwargs(tmp_path):
    log_file = str(tmp_path / "test.log")

    @function_logger(log_file)
    def greet(name="World"):
        return f"Hello, {name}!"

    result = greet(name="Test")
    assert result == "Hello, Test!"
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'greet' in content
    assert "name" in content

def test_log_decorator_multiple_calls(tmp_path):
    log_file = str(tmp_path / "test.log")

    @function_logger(log_file)
    def square(x):
        return x * x

    square(3)
    square(5)
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content.count('square') == 2
