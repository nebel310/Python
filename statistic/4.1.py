import math
import scipy.stats as stats
import matplotlib.pyplot as plt

# Исходные данные (дискретный ряд из ЛР 1.1)
# Ключ - возраст (X), значение - частота (Y)
DISCRETE_DATA = {
    14: 49, 15: 53, 16: 236, 17: 126, 18: 806,
    19: 971, 20: 910, 21: 716, 22: 944, 23: 1071,
    24: 810, 25: 1050, 26: 980, 27: 1263, 28: 1113,
    29: 1340, 30: 734, 31: 1115, 32: 796, 33: 758,
    34: 869, 35: 676, 36: 1198, 37: 522, 38: 1006,
    39: 695, 40: 723, 41: 837, 42: 978, 43: 820,
    44: 1032, 45: 690, 46: 677, 47: 831, 48: 1026,
    49: 1060, 50: 150, 51: 188, 52: 193, 53: 47,
    54: 26, 55: 62, 56: 76, 57: 136, 58: 262,
    59: 74, 60: 266, 61: 226, 62: 139, 63: 183,
    64: 189, 65: 79, 66: 188, 67: 128, 69: 202,
    70: 26, 71: 85, 73: 17
}

# Уровень значимости (по заданию)
ALPHA = 0.05
# Имя файла для сохранения графика
PLOT_FILENAME = "correlation_field.png"
# Объем выборки (количество уникальных значений возраста, согласно примечанию)
N = len(DISCRETE_DATA)
# Списки значений X и Y для вычислений
X_VALUES = list(DISCRETE_DATA.keys())
Y_VALUES = list(DISCRETE_DATA.values())


def calculate_correlation(x_data, y_data):
    """Вычисляет ковариацию, СКО и коэффициент корреляции Пирсона
    Вход:
    x_data - список значений возраста (X)
    y_data - список значений частот (Y)
    Выход:
    cov_xy - выборочная ковариация
    std_x - выборочное СКО величины X
    std_y - выборочное СКО величины Y
    r_xy - выборочный коэффициент корреляции
    """
    n = len(x_data)
    
    mean_x = sum(x_data) / n
    mean_y = sum(y_data) / n
    
    sum_cov = 0.0
    sum_sq_x = 0.0
    sum_sq_y = 0.0
    
    for i in range(n):
        diff_x = x_data[i] - mean_x
        diff_y = y_data[i] - mean_y
        sum_cov += diff_x * diff_y
        sum_sq_x += diff_x ** 2
        sum_sq_y += diff_y ** 2
        
    cov_xy = sum_cov / n
    
    var_x = sum_sq_x / n
    var_y = sum_sq_y / n
    std_x = math.sqrt(var_x)
    std_y = math.sqrt(var_y)
    
    r_xy = cov_xy / (std_x * std_y)
    
    return cov_xy, std_x, std_y, r_xy


def interpret_correlation(r_xy):
    """Интерпретирует тесноту и направление линейной связи
    Вход:
    r_xy - выборочный коэффициент корреляции
    Выход:
    Текстовая интерпретация (строка)
    """
    abs_r = abs(r_xy)
    
    if abs_r == 1:
        strength = "функциональная"
    elif 0.7 < abs_r < 1:
        strength = "сильная"
    elif 0.5 < abs_r <= 0.7:
        strength = "заметная"
    elif 0.3 < abs_r <= 0.5:
        strength = "умеренная"
    elif 0 < abs_r <= 0.3:
        strength = "слабая"
    else:
        strength = "отсутствует"
        
    direction = "прямая" if r_xy > 0 else "обратная"
    
    return f"{strength}, {direction}"


def check_hypothesis(r_xy, n, alpha):
    """Проверяет гипотезу о значимости коэффициента корреляции
    Вход:
    r_xy - выборочный коэффициент корреляции
    n - объем выборки
    alpha - уровень значимости
    Выход:
    t_obs - наблюдаемое значение критерия Стьюдента
    t_crit - критическое значение критерия Стьюдента
    """
    t_obs = (r_xy * math.sqrt(n - 2)) / math.sqrt(1 - r_xy ** 2)
    
    df = n - 2
    t_crit = stats.t.ppf(1 - alpha / 2, df)
    
    return t_obs, t_crit


def plot_correlation_field(x_data, y_data, filename):
    """Строит и сохраняет корреляционное поле
    Вход:
    x_data - список значений возраста (X)
    y_data - список значений частот (Y)
    filename - имя файла для сохранения
    Выход:
    None (сохраняет файл)
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(x_data, y_data, color='black', s=30)
    plt.title('Корреляционное поле')
    plt.xlabel('Возраст преступника (X)')
    plt.ylabel('Частота совершаемых преступлений (Y)')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig(filename)
    plt.close()


def main():
    cov_xy, std_x, std_y, r_xy = calculate_correlation(X_VALUES, Y_VALUES)
    
    print("1. Линейная корреляционная зависимость:")
    print(f"Ковариация: {cov_xy:.4f}")
    print(f"СКО величины X: {std_x:.4f}")
    print(f"СКО величины Y: {std_y:.4f}")
    print(f"Выборочный коэффициент корреляции: {r_xy:.4f}")
    
    interpretation = interpret_correlation(r_xy)
    print(f"Интерпретация: Зависимость {interpretation}")
    print("-" * 50)
    
    t_obs, t_crit = check_hypothesis(r_xy, N, ALPHA)
    
    print("2. Проверка гипотезы о значимости коэффициента корреляции:")
    print(f"t_набл: {t_obs:.4f}")
    print(f"t_кр: {t_crit:.4f}")
    print(f"Сравнение: |{t_obs:.4f}| > {t_crit:.4f}")
    
    if abs(t_obs) > t_crit:
        print("Анализ результатов: H0 отвергается, так как |t_набл| > t_кр.")
        print("Выборочный коэффициент корреляции значимо отличается от нуля (X и Y коррелированы).")
    else:
        print("Анализ результатов: H0 не отвергается, так как |t_набл| < t_кр.")
        print("Выборочный коэффициент корреляции незначимо отличается от нуля.")
    print("-" * 50)
    
    plot_correlation_field(X_VALUES, Y_VALUES, PLOT_FILENAME)
    print(f"3. Корреляционное поле построено и сохранено в файл: {PLOT_FILENAME}")


if __name__ == "__main__":
    main()