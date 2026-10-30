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

# НОВОЕ: k1 и k2 считаем от реальных длин выборок, а не от константы N
k1 = len(sample1) - 1
k2 = len(sample2) - 1

print(f"Число наблюдений: n1 = {len(sample1)}, n2 = {len(sample2)}")
print(f"Число степеней свободы: k1 = {k1}, k2 = {k2}")
print(f"Исправленная дисперсия выборки 1: s1² = {s1_sq:.4f}")
print(f"Исправленная дисперсия выборки 2: s2² = {s2_sq:.4f}")

# НОВОЕ: F_набл одна и та же для обоих случаев — как и сказала преподша
f_obs = s1_sq / s2_sq
print(f"\nНаблюдаемое значение F-критерия: F_набл = s1²/s2² = {f_obs:.4f}")

print("\n=== Случай а) H1: D1 > D2 ===")
# НОВОЕ: k1 и k2 передаются в порядке выборок (числитель s1², знаменатель s2²)
f_crit_a = f.ppf(1 - ALPHA, k1, k2)
print(f"Критическое значение F-критерия: F_кр = {f_crit_a:.4f}")
print(f"Правило: H0 отвергается, если F_набл > F_кр (правосторонняя критическая область)")
print(f"Сравнение: {f_obs:.4f} {'>' if f_obs > f_crit_a else '<='} {f_crit_a:.4f}")
if f_obs > f_crit_a:
    print("Анализ результатов: H0 отвергается (D1 > D2)")
else:
    print("Анализ результатов: H0 не отвергается (нет оснований считать D1 > D2)")

print("\n=== Случай б) H1: D1 != D2 ===")
# НОВОЕ: двусторонний случай через ДВЕ критические границы, а не через перестановку дисперсий
# F_набл остаётся той же (s1²/s2²), меняются только критические значения
f_crit_b_low = f.ppf(ALPHA / 2, k1, k2)
f_crit_b_high = f.ppf(1 - ALPHA / 2, k1, k2)
print(f"Нижнее критическое значение: F_кр_ниж = {f_crit_b_low:.4f}")
print(f"Верхнее критическое значение: F_кр_верх = {f_crit_b_high:.4f}")
print(f"Правило: H0 отвергается, если F_набл вне интервала (F_кр_ниж; F_кр_верх)")
print(f"Сравнение: {f_crit_b_low:.4f} {'<' if f_obs > f_crit_b_low else '>='} {f_obs:.4f} {'<' if f_obs < f_crit_b_high else '>='} {f_crit_b_high:.4f}")
if f_obs < f_crit_b_low or f_obs > f_crit_b_high:
    if f_obs < f_crit_b_low:
        print("Анализ результатов: H0 отвергается (D1 != D2, причём s1² < s2²)")
    else:
        print("Анализ результатов: H0 отвергается (D1 != D2, причём s1² > s2²)")
else:
    print("Анализ результатов: H0 не отвергается (нет оснований считать D1 != D2)")