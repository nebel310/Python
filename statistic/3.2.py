import math
import random
from scipy.stats import f


N = 62  # Объем выборки, посчитан в ЛР 2.1
ALPHA = 0.05  # Число альфа (допустимая вероятность ошибки)
DATA_FILE = 'data.txt'


def read_data(filename):
    """Читает числа из файла и возвращает список

    Вход:
        filename - путь к текстовому файлу с числами

    Выход:
        список чисел (float)
    """
    with open(filename, 'r', encoding='utf-8-sig') as f:
        text = f.read()
    numbers = []
    for token in text.replace(',', ' ').split():
        try:
            numbers.append(float(token))
        except ValueError:
            pass
    return numbers


def mean(data):
    """Вычисляет выборочное среднее

    Вход:
        data - список чисел

    Выход:
        среднее арифметическое (float)
    """
    return sum(data) / len(data)


def variance(data):
    """Вычисляет исправленную выборочную дисперсию со знаменателем n минус 1

    Вход:
        data - список чисел

    Выход:
        исправленная выборочная дисперсия s² (float)
    """
    m = mean(data)
    return sum((x - m) ** 2 for x in data) / (len(data) - 1)


def generate_sample(population, n):
    """Генерирует случайную выборку заданного объема с возвращением

    Вход:
        population - генеральная совокупность (список чисел)
        n - объем выборки (int)

    Выход:
        выборка - список чисел
    """
    return [random.choice(population) for _ in range(n)]


population = read_data(DATA_FILE)
sample1 = generate_sample(population, N)
sample2 = generate_sample(population, N)

s1_sq = variance(sample1)
s2_sq = variance(sample2)
k = N - 1

print(f"Число наблюдений: n1 = n2 = {N}")
print(f"Число степеней свободы: k1 = k2 = {k}")
print(f"Исправленная дисперсия выборки 1: s1² = {s1_sq:.4f}")
print(f"Исправленная дисперсия выборки 2: s2² = {s2_sq:.4f}")

print("\n=== Случай а) H1: D1 > D2 ===")
f_obs_a = s1_sq / s2_sq
f_crit_a = f.ppf(1 - ALPHA, k, k)
print(f"Наблюдаемое значение F-критерия: F_набл = {f_obs_a:.4f}")
print(f"Критическое значение F-критерия: F_кр = {f_crit_a:.4f}")
if f_obs_a > f_crit_a:
    print("Анализ результатов: H0 отвергается (D1 > D2)")
else:
    print("Анализ результатов: H0 не отвергается (нет оснований считать D1 > D2)")

print("\n=== Случай б) H1: D1 != D2 ===")
if s1_sq >= s2_sq:
    f_obs_b = s1_sq / s2_sq
else:
    f_obs_b = s2_sq / s1_sq
f_crit_b = f.ppf(1 - ALPHA / 2, k, k)
print(f"Наблюдаемое значение F-критерия: F_набл = {f_obs_b:.4f}")
print(f"Критическое значение F-критерия: F_кр = {f_crit_b:.4f}")
if f_obs_b > f_crit_b:
    print("Анализ результатов: H0 отвергается (D1 != D2)")
else:
    print("Анализ результатов: H0 не отвергается (нет оснований считать D1 != D2)")
