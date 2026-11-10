import math
import random
from scipy.stats import chi2


N = 62  # Объем выборки, посчитан в ЛР 2.1
SIGMA_SQ_LAB_1_1 = 144.917  # Генеральная дисперсия из ЛР 1.1
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
sample = generate_sample(population, N)

s_sq = variance(sample)
k = N - 1
chi2_obs = k * s_sq / SIGMA_SQ_LAB_1_1

print(f"Число наблюдений: n = {N}")
print(f"Число степеней свободы: k = {k}")
print(f"Гипотетическая дисперсия из ЛР 1.1: σ0² = {SIGMA_SQ_LAB_1_1:.4f}")
print(f"Исправленная дисперсия выборки: s² = {s_sq:.4f}")
print(f"Наблюдаемое значение χ²-критерия: χ²_набл = {chi2_obs:.4f}")

print("\n=== Случай а) H1: D(X) > σ0² ===")
chi2_crit_a = chi2.ppf(1 - ALPHA, k)
print(f"Критическое значение χ²-критерия: χ²_кр = {chi2_crit_a:.4f}")
if chi2_obs < chi2_crit_a:
    print("Анализ результатов: H0 не отвергается (нет оснований считать D(X) > σ0²)")
else:
    print("Анализ результатов: H0 отвергается (D(X) > σ0²)")

print("\n=== Случай б) H1: D(X) != σ0² ===")
chi2_crit_b_low = chi2.ppf(ALPHA / 2, k)
chi2_crit_b_high = chi2.ppf(1 - ALPHA / 2, k)
print(f"Нижнее критическое значение: χ²_кр_ниж = {chi2_crit_b_low:.4f}")
print(f"Верхнее критическое значение: χ²_кр_верх = {chi2_crit_b_high:.4f}")
if chi2_crit_b_low < chi2_obs < chi2_crit_b_high:
    print("Анализ результатов: H0 не отвергается (нет оснований считать D(X) != σ0²)")
else:
    print("Анализ результатов: H0 отвергается (D(X) != σ0²)")

print("\n=== Случай в) H1: D(X) < σ0² ===")
chi2_crit_v = chi2.ppf(ALPHA, k)
print(f"Критическое значение χ²-критерия: χ²_кр = {chi2_crit_v:.4f}")
if chi2_obs > chi2_crit_v:
    print("Анализ результатов: H0 не отвергается (нет оснований считать D(X) < σ0²)")
else:
    print("Анализ результатов: H0 отвергается (D(X) < σ0²)")