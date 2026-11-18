import math
import matplotlib.pyplot as plt

# Исходные данные: возраст (x)
X_ORIG = [13, 15, 18, 20, 23, 26, 31]
# Исходные данные: частоты (y)
Y_ORIG = [19, 14, 15, 10, 12, 8, 5]
# Точность округления для вывода
DECIMALS = 2
# Порог в процентах для разностей
THRESHOLD_PERCENT = 2
# Имя файла для сохранения графика
PLOT_FILENAME = 'plot.png'

def linear_interpolation(x, x_arr, y_arr):
    """Выполняет линейную интерполяцию
    Вход:
    x - точка, для которой нужно найти значение
    x_arr - список известных значений аргумента
    y_arr - список известных значений функции
    Выход:
    y - интерполированное значение функции
    """
    for i in range(len(x_arr) - 1):
        if x_arr[i] <= x <= x_arr[i+1]:
            return y_arr[i] + (y_arr[i+1] - y_arr[i]) / (x_arr[i+1] - x_arr[i]) * (x - x_arr[i])
    return y_arr[-1]

def structural_identification():
    """Выполняет структурную идентификацию по 7 видам зависимостей
    Выход:
    results - список словарей с результатами для каждой зависимости
    """
    x1, y1 = X_ORIG[0], Y_ORIG[0]
    xn, yn = X_ORIG[-1], Y_ORIG[-1]
    sum_y = sum(Y_ORIG)

    bar_xs_vals = []
    bar_ys_vals = []

    bar_xs_vals.append((x1 + xn) / 2)
    bar_ys_vals.append((y1 + yn) / 2)

    bar_xs_vals.append(math.sqrt(x1 * xn))
    bar_ys_vals.append(math.sqrt(y1 * yn))

    bar_xs_vals.append((x1 + xn) / 2)
    bar_ys_vals.append(math.sqrt(y1 * yn))

    bar_xs_vals.append(2 * x1 * xn / (x1 + xn))
    bar_ys_vals.append((y1 + yn) / 2)

    bar_xs_vals.append((x1 + xn) / 2)
    bar_ys_vals.append(2 * y1 * yn / (y1 + yn))

    bar_xs_vals.append(2 * x1 * xn / (x1 + xn))
    bar_ys_vals.append(2 * y1 * yn / (y1 + yn))

    bar_xs_vals.append(math.sqrt(x1 * xn))
    bar_ys_vals.append((y1 + yn) / 2)

    results = []
    for i in range(7):
        xs = bar_xs_vals[i]
        ys_bar = bar_ys_vals[i]
        ys_exp = linear_interpolation(xs, X_ORIG, Y_ORIG)
        delta = abs(ys_bar - ys_exp)
        percent = (delta / sum_y) * 100

        results.append({
            'id': i + 1,
            'xs': xs,
            'ys_bar': ys_bar,
            'ys_exp': ys_exp,
            'delta': delta,
            'percent': percent
        })
    return results

def polynomial_degree():
    """Определяет степень аппроксимирующего многочлена
    Выход:
    degree - степень многочлена
    diffs - список списков разностей
    """
    x_interp = list(range(X_ORIG[0], X_ORIG[-1] + 1))
    y_interp = [linear_interpolation(x, X_ORIG, Y_ORIG) for x in x_interp]
    sum_y = sum(Y_ORIG)
    threshold = sum_y * (THRESHOLD_PERCENT / 100)

    diffs = []
    current = y_interp
    while len(current) > 1:
        next_diff = [abs(current[i] - current[i+1]) for i in range(len(current)-1)]
        diffs.append(next_diff)
        current = next_diff

    degree = None
    for i, d in enumerate(diffs):
        if max(d) <= threshold:
            degree = i + 1
            break
    if degree is None:
        degree = len(diffs)
    return degree, diffs

def plot_data():
    """Строит график экспериментальных данных и сохраняет его в файл
    """
    plt.figure()
    plt.plot(X_ORIG, Y_ORIG, 'o-')
    for x, y in zip(X_ORIG, Y_ORIG):
        plt.text(x, y, f'({x}; {y})', ha='right')
    plt.grid(True)
    plt.title('График экспериментальных данных')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig(PLOT_FILENAME)
    plt.close()

def main():
    plot_data()
    results = structural_identification()
    print("Результаты структурной идентификации:")
    print(f"{'Номер':<7} | {'Структура':<15} | {'x_s':<7} | {'y_s_теор':<9} | {'y_s_эксп':<9} | {'Δ_s':<7} | {'Δ_s, %':<7}")
    print("-" * 80)
    structures = [
        "y = ax + b",
        "y = ax^b",
        "y = ab^x",
        "y = a + b/x",
        "y = 1/(ax + b)",
        "y = x/(ax + b)",
        "y = a*ln(x) + b"
    ]
    min_delta = float('inf')
    best_idx = -1
    for res in results:
        print(f"{res['id']:<7} | {structures[res['id']-1]:<15} | {res['xs']:<7.1f} | {res['ys_bar']:<9.1f} | {res['ys_exp']:<9.1f} | {res['delta']:<7.2f} | {res['percent']:<7.2f}")
        if res['delta'] < min_delta:
            min_delta = res['delta']
            best_idx = res['id']

    print(f"\nМинимальное отклонение: {min_delta:.2f}")
    print(f"Наилучшая зависимость: {structures[best_idx-1]}")
    print(f"Анализ результатов: H0 не отвергается, так как наилучшей зависимостью является {structures[best_idx-1]} с минимальным отклонением {min_delta:.2f}")

    degree, diffs = polynomial_degree()
    print("\nПоследовательные разности:")
    for i, d in enumerate(diffs):
        print(f"Δ{i+1}: {[round(val, 2) for val in d]}")

    print(f"\nПоказатель степени аппроксимирующего многочлена: {degree}")
    print(f"Анализ результатов: Выбрана степень {degree}, так как максимальное значение разности не превышает {THRESHOLD_PERCENT}% от суммы частот.")

if __name__ == "__main__":
    main()