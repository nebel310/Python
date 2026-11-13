import math

# Интервальный ряд (из ЛР 1.1)
# Середины интервалов (X)
INTERVAL_X = [18.5, 27.5, 36.5, 45.5, 54.5, 63.5, 72.5]
# Частоты (Y)
INTERVAL_Y = [4811, 9476, 7243, 7951, 1140, 1472, 330]
# Ширина интервала (разница между верхней и нижней границей)
INTERVAL_WIDTH = 9

# Дискретный ряд (из ЛР 1.1) для расчета коэффициента Спирмена
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


def calculate_variances(x_mids, freqs, h):
    """Вычисляет внутригрупповую, межгрупповую и общую дисперсию
    Вход:
    x_mids - список середин интервалов
    freqs - список частот
    h - ширина интервала
    Выход:
    d_intra - внутригрупповая дисперсия
    d_inter - межгрупповая дисперсия
    d_total - общая дисперсия
    mean_x - общая средняя
    """
    n = len(x_mids)
    total_n = 0
    for f in freqs:
        total_n += f

    sum_xf = 0.0
    for i in range(n):
        sum_xf += x_mids[i] * freqs[i]
    mean_x = sum_xf / total_n

    sum_inter = 0.0
    for i in range(n):
        sum_inter += (x_mids[i] - mean_x)**2 * freqs[i]
    d_inter = sum_inter / total_n

    d_intra = (h**2) / 12

    d_total = d_intra + d_inter

    return d_intra, d_inter, d_total, mean_x


def calculate_correlation_ratio(d_inter, d_total):
    """Вычисляет корреляционное отношение
    Вход:
    d_inter - межгрупповая дисперсия
    d_total - общая дисперсия
    Выход:
    eta - корреляционное отношение
    """
    eta = math.sqrt(d_inter / d_total)
    return eta


def get_ranks(values):
    """Вычисляет ранги значений (средний ранг при совпадениях)
    Вход:
    values - список чисел
    Выход:
    список рангов
    """
    n = len(values)
    sorted_vals = sorted(values)
    ranks = []
    for v in values:
        count = 0
        total_rank = 0
        for i in range(n):
            if sorted_vals[i] == v:
                count += 1
                total_rank += (i + 1)
        avg_rank = total_rank / count
        ranks.append(avg_rank)
    return ranks


def calculate_spearman(x_vals, y_vals):
    """Вычисляет коэффициент ранговой корреляции Спирмена
    Вход:
    x_vals - список значений X
    y_vals - список значений Y
    Выход:
    R - коэффициент Спирмена
    """
    n = len(x_vals)
    nx = get_ranks(x_vals)
    ny = get_ranks(y_vals)
    
    sum_d2 = 0.0
    for i in range(n):
        d = nx[i] - ny[i]
        sum_d2 += d**2
        
    R = 1 - (6 * sum_d2) / (n * (n**2 - 1))
    return R


def main():
    d_intra, d_inter, d_total, mean_x = calculate_variances(INTERVAL_X, INTERVAL_Y, INTERVAL_WIDTH)
    
    print("1. Расчет дисперсий на основе интервального ряда:")
    print(f"Внутригрупповая дисперсия: {d_intra:.4f}")
    print(f"Межгрупповая дисперсия: {d_inter:.4f}")
    print(f"Общая дисперсия: {d_total:.4f}")
    print(f"Проверка формулы: {d_intra:.4f} + {d_inter:.4f} = {d_total:.4f}")
    print("-" * 50)
    
    eta = calculate_correlation_ratio(d_inter, d_total)
    print("2. Корреляционное отношение:")
    print(f"Корреляционное отношение: {eta:.4f}")
    print(f"Анализ результатов: Связь сильная, так как {eta:.4f} > 0.7")
    print("-" * 50)
    
    x_discrete = list(DISCRETE_DATA.keys())
    y_discrete = list(DISCRETE_DATA.values())
    R = calculate_spearman(x_discrete, y_discrete)
    
    print("3. Коэффициент ранговой корреляции Спирмена:")
    print(f"Коэффициент Спирмена: {R:.4f}")
    print(f"Анализ результатов: Связь {'сильная, обратная' if R < -0.7 else 'умеренная' if R < -0.3 else 'слабая'}, так как |{R:.4f}| {'>' if abs(R) > 0.7 else '<'} 0.7")
    print("-" * 50)


if __name__ == "__main__":
    main()