import numpy as np
import random
import pandas as pd
import time
from scipy.stats import qmc
import math

# ------------------ Các hàm benchmark ------------------
def ackley_function(x):
    a, b, c = 20, 0.2, 2 * np.pi
    d = len(x)
    sum1 = np.sum(x**2)
    sum2 = np.sum(np.cos(c * x))
    return -a * np.exp(-b * np.sqrt(sum1 / d)) - np.exp(sum2 / d) + a + np.e

def alpine_function(x):
    return np.sum(np.abs(x * np.sin(x) + 0.1 * x))

def cigar_function(x):
    return x[0]**2 + 1e6 * np.sum(x[1:]**2)

def dixon_price_function(x):
    term1 = (x[0] - 1)**2
    i = np.arange(2, len(x)+1)
    term2 = np.sum(i * (2 * x[1:]**2 - x[:-1])**2)
    return term1 + term2

def elliptic_function(x):
    i = np.arange(1, len(x)+1)
    return np.sum((10**6)**((i-1)/(len(x)-1)) * x**2)

def exponential_function(x):
    return np.exp(1-(0.5 * np.sum(x**2)))

def griewank_function(x):
    return np.sum(x**2) / 4000 - np.prod(np.cos(x / np.sqrt(np.arange(1, len(x)+1)))) + 1

def icm_function(x):
    x = np.asarray(x)
    return len(x)*0.1 + (np.sum(x**2) - 0.1 * np.sum(np.cos(5.0 * np.pi * x)))

def levy_function(x):
    w = 1 + (x - 1) / 4
    term1 = np.sin(np.pi * w[0])**2
    term2 = np.sum((w[:-1] - 1)**2 * (1 + 10 * np.sin(np.pi * w[:-1] + 1)**2))
    term3 = (w[-1] - 1)**2 * (1 + np.sin(2 * np.pi * w[-1])**2)
    return term1 + term2 + term3

def michalewicz_function(x):
    m = 10
    i = np.arange(1, len(x)+1)
    return len(x) - np.sum(np.sin(x) * (np.sin(i * x**2 / np.pi))**(2*m))

def u_func(x, a=10, k=100, m=4):
    if x > a:
        return k * (x - a)**m
    elif x < -a:
        return k * (-x - a)**m
    else:
        return 0

def penalized_1_function(x):
    x = np.asarray(x)
    n = len(x)
    y = 1 + (x + 1)/4
    term1 = 10 * np.sin(np.pi * y[0])**2
    term2 = 0
    for i in range(n-1):
        term2 += (y[i] - 1)**2 * (1 + 10 * np.sin(np.pi * y[i+1])**2)
    term3 = (y[-1] - 1)**2
    U = np.sum([u_func(xi) for xi in x])
    return (np.pi / n) * (term1 + term2 + term3) + U

def u_func2(x, a=5, k=100, m=4):
    if x > a:
        return k * (x - a)**m
    elif x < -a:
        return k * (-x - a)**m
    else:
        return 0

def penalized_2_function(x):
    x = np.asarray(x)
    n = len(x)
    term1 = np.sin(3.0 * np.pi * x[0])**2
    term2 = 0
    for i in range(n-1):
        term2 += (x[i] - 1)**2 * (1 + np.sin(3.0 * np.pi * x[i+1])**2)
    term3 = (x[-1] - 1)**2 * (1 + np.sin(2.0 * np.pi * x[-1])**2)
    U = np.sum([u_func2(xi) for xi in x])
    return 0.1 * (term1 + term2 + term3) + U

def extended_powell_function(x):
    x = np.asarray(x)
    n = len(x)

    s = 0
    for k in range(n // 4):
        i1 = 4*k
        i2 = 4*k + 1
        i3 = 4*k + 2
        i4 = 4*k + 3
        term1 = (x[i1] + 10*x[i2])**2
        term2 = 5*(x[i3] - x[i4])**2
        term3 = (x[i2] - 2*x[i3])**4
        term4 = 10*(x[i1] - x[i4])**4
        s += term1 + term2 + term3 + term4
    return s

def rastrigin_function(x):
    A = 10
    return A * len(x) + np.sum(x**2 - A * np.cos(2 * np.pi * x))

def rosenbrock_function(x):
    return np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

def rotated_hyper_ellipsoid(x):
    x = np.asarray(x)
    s = 0
    for i in range(len(x)):
        s += np.sum(x[:i+1])**2
    return s

def salomon_function(x):
    x = np.asarray(x)
    r = np.sqrt(np.sum(x**2))
    return 1 - np.cos(2.0 * np.pi * r) + 0.1 * r

def schwefel_function(x):
    return 418.982887272434 * len(x) - np.sum(x * np.sin(np.sqrt(np.abs(x))))

def schwefel_1_20(x):
    x = np.asarray(x)
    return np.sum(np.abs(x))

def schwefel_2_21(x):
    x = np.asarray(x)
    return np.max(np.abs(x))

def schwefel_2_22(x):
    x = np.asarray(x)
    abs_x = np.abs(x)
    return np.sum(abs_x) + np.prod(abs_x)

def sphere_function(x):
    return np.sum(x**2)

def step_function(x):
    return np.sum(np.floor(x + 0.5)**2)

# def styblinski_tang_function(x):
#     x = np.asarray(x)
#     return 39.1661657037714*len(x) + 0.5 * np.sum(x**4 - 16*x**2 + 5*x)
def styblinski_tang_function(x):
    x = np.asarray(x)
    return 39.16616572302271*len(x) + 0.5 * np.sum(x**4 - 16*x**2 + 5*x)

def sum_power_function(x):
    return np.sum(np.abs(x)**(np.arange(1, len(x)+1)+1))

def sum_squares_function(x):
    return np.sum(np.arange(1, len(x)+1) * x**2)

def quartic_function(x):
    return np.sum(np.arange(1, len(x)+1) * x**4)

def weierstrass_function(x, a=0.5, b=3, kmax=20):
    x = np.asarray(x)
    n = len(x)
    sum_1 = 0.0
    for i in range(n):
        for k in range(kmax + 1):
            sum_1 += (a**k) * np.cos(2.0 * np.pi * (b**k) * (x[i] + 0.5))
    sum_2 = 0.0
    for k in range(kmax + 1):
        sum_2 += (a**k) * np.cos(2.0 * np.pi * (b**k) * 0.5)
    return sum_1 - n * sum_2

def zakharov_function(x):
    sum1 = np.sum(x**2)
    sum2 = np.sum(0.5 * np.arange(1, len(x)+1) * x)
    return sum1 + sum2**2 + sum2**4
def schaffer_function(x):
    X = np.asarray(x, dtype=float)
    S = np.sum(X**2, axis=-1)           
    vals = 0.5 + (np.sin(S)**2 - 0.5) / (1.0 + 0.001*S)**2

    return vals

# -------------------- Functions Dictionary --------------------
# functions = {
#     "ackley": (ackley_function, [-100, 100],0, 100),
#     "alpine": (alpine_function, [-100, 100],0, 100),
#     "cigar": (cigar_function, [-100, 100],0,100),
#     "dixon_price": (dixon_price_function, [-10, 10],0, 100),
#     "elliptic": (elliptic_function, [-100, 100],0, 100),
#     "exponential": (exponential_function, [-10, 10],0, 100),
#     "griewank": (griewank_function, [-600, 600], 0,100),
#     "ICM": (icm_function, [-100, 100], 0,100),
#     "levy": (levy_function, [-10, 10], 0,100),
#     "michalewicz": (michalewicz_function, [0, np.pi],0, 100),
#     "penalized_1": (penalized_1_function, [-50, 50],0, 100),
#     "penalized_2": (penalized_2_function, [-50, 50],0, 100),
#     "powell": (extended_powell_function, [-4, 5],0, 30),
#     "rastrigin": (rastrigin_function, [-100, 100], 0,100),
#     "rosenbrock": (rosenbrock_function, [-10, 10],0, 100),
#     "rotated_hyper_ellipsoid": (rotated_hyper_ellipsoid, [-100, 100],0,100),
#     "salomon": (salomon_function, [-100, 100], 0,100),
#     "schaffer": (schaffer_function, [-100, 100], 0,100),
#     "schwefel": (schwefel_function, [-500, 500],0, 100),
#     "schwefel_1_20": (schwefel_1_20, [-100, 100], 0,100),
#     "schwefel_2_21": (schwefel_2_21,[-100, 100],0, 100),
#     "schwefel_2_22": (schwefel_2_22, [-10, 10], 0,100),
#     "sphere": (sphere_function, [-100, 100],0, 100),
#     "step": (step_function, [-100, 100], 0,100),
#     "styblinski_tang": (styblinski_tang_function, [-5, 5],0, 100),
#     "sum_power": (sum_power_function, [-10, 10], 0,100),
#     "sum_squares": (sum_squares_function, [-10, 10], 0,100),
#     "quartic": (quartic_function, [-10, 10],0, 100),
#     "weierstrass": (weierstrass_function, [-1, 1],0, 100),
#     "zakharov": (zakharov_function, [-5, 10], 0,100)
#  }

# functions = {
#     "ackley": (ackley_function, [-100, 100], 0, 50),
#     "alpine": (alpine_function, [-100, 100], 0, 50),
#     "cigar": (cigar_function, [-100, 100], 0, 50),
#     "dixon_price": (dixon_price_function, [-10, 10], 0, 50),
#     "elliptic": (elliptic_function, [-100, 100], 0, 50),
#     "exponential": (exponential_function, [-10, 10], 0, 50),
#     "griewank": (griewank_function, [-600, 600], 0, 50),
#     "ICM": (icm_function, [-100, 100], 0, 50),
#     "levy": (levy_function, [-10, 10], 0, 50),
#     "michalewicz": (michalewicz_function, [0, np.pi], 0, 50),
#     "penalized_1": (penalized_1_function, [-50, 50], 0, 50),
#     "penalized_2": (penalized_2_function, [-50, 50], 0, 50),
#     "powell": (extended_powell_function, [-4, 5], 0, 50),
#     "rastrigin": (rastrigin_function, [-100, 100], 0, 50),
#     "rosenbrock": (rosenbrock_function, [-10, 10], 0, 50),
#     "rotated_hyper_ellipsoid": (rotated_hyper_ellipsoid, [-100, 100], 0, 50),
#     "salomon": (salomon_function, [-100, 100], 0, 50),
#     "schaffer": (schaffer_function, [-100, 100], 0, 50),
#     "schwefel": (schwefel_function, [-500, 500], 0, 50),
#     "schwefel_1_20": (schwefel_1_20, [-100, 100], 0, 50),
#     "schwefel_2_21": (schwefel_2_21, [-100, 100], 0, 50),
#     "schwefel_2_22": (schwefel_2_22, [-10, 10], 0, 50),
#     "sphere": (sphere_function, [-100, 100], 0, 50),
#     "step": (step_function, [-100, 100], 0, 50),
#     "styblinski_tang": (styblinski_tang_function, [-5, 5], 0, 50),
#     "sum_power": (sum_power_function, [-10, 10], 0, 50),
#     "sum_squares": (sum_squares_function, [-10, 10], 0, 50),
#     "quartic": (quartic_function, [-10, 10], 0, 50),
#     "weierstrass": (weierstrass_function, [-1, 1], 0, 50),
#     "zakharov": (zakharov_function, [-5, 10], 0, 50)
# }
functions = {
    # "ackley": (ackley_function, [-100, 100], 0, 30),
    # "alpine": (alpine_function, [-100, 100], 0, 30),
    # "cigar": (cigar_function, [-100, 100], 0, 30),
    # "dixon_price": (dixon_price_function, [-10, 10], 0, 30),
    # "elliptic": (elliptic_function, [-100, 100], 0, 30),
    # "exponential": (exponential_function, [-10, 10], 0, 30),
    # "griewank": (griewank_function, [-600, 600], 0, 30),
    # "ICM": (icm_function, [-100, 100], 0, 30),
    # "levy": (levy_function, [-10, 10], 0, 30),
    # "michalewicz": (michalewicz_function, [0, np.pi], 0, 30),
    # "penalized_1": (penalized_1_function, [-50, 50], 0, 30),
    # "penalized_2": (penalized_2_function, [-50, 50], 0, 30),
    # "powell": (extended_powell_function, [-4, 5], 0, 30),
    # "rastrigin": (rastrigin_function, [-100, 100], 0, 30),
    # "rosenbrock": (rosenbrock_function, [-10, 10], 0, 30),
    # "rotated_hyper_ellipsoid": (rotated_hyper_ellipsoid, [-100, 100], 0, 30),
    # "salomon": (salomon_function, [-100, 100], 0, 30),
    # "schaffer": (schaffer_function, [-100, 100], 0, 30),
    # "schwefel": (schwefel_function, [-500, 500], 0, 30),
    # "schwefel_1_20": (schwefel_1_20, [-100, 100], 0, 30),
    # "schwefel_2_21": (schwefel_2_21, [-100, 100], 0, 30),
    # "schwefel_2_22": (schwefel_2_22, [-10, 10], 0, 30),
    # "sphere": (sphere_function, [-100, 100], 0, 30),
    # "step": (step_function, [-100, 100], 0, 30),
    "styblinski_tang": (styblinski_tang_function, [-5, 5], 0, 50),
    # "sum_power": (sum_power_function, [-10, 10], 0, 30),
    # "sum_squares": (sum_squares_function, [-10, 10], 0, 30),
    # "quartic": (quartic_function, [-10, 10], 0, 30),
    # "weierstrass": (weierstrass_function, [-1, 1], 0, 30),
    # "zakharov": (zakharov_function, [-5, 10], 0, 30)
}
# ----- Hàm random_select -----
def random_select(pop, i):
    candidates = [k for k in range(len(pop)) if k != i]
    return np.random.choice(candidates)

def co_population(pop, lb, ub, iteration, max_iter):
    pop_size, dim = pop.shape
    lb = np.array(lb)
    ub = np.array(ub)
    c = (lb + ub) / 2  # trung tâm của miền tìm kiếm
    new_pop = np.zeros_like(pop)
    
    # Tính tỉ lệ tiến triển
    ratio = iteration / max_iter

    # Xác định xác suất chọn ứng viên dựa trên kết quả của Table 1:
    if 0 <= ratio <= 0.224:  # Giai đoạn ban đầu: ưu tiên khám phá (QO cao)
        P_reo = 0.01
        P_qr  = 0.01
        P_qo  = 0.54 + 1.92 * ratio
    elif ratio > 0.723:      # Giai đoạn cuối: ưu tiên khai thác (QR cao)
        P_reo = 0.01
        P_qr  = 0.97
        P_qo  = 0.01
    else:                    # Giai đoạn trung gian: nội suy tuyến tính
        P_reo = 0.01
        P_qr  = -0.42 + 1.92 * ratio
        P_qo  = 1.4 - 1.92 * ratio
    
    # Duyệt qua từng cá thể trong quần thể
    for i in range(pop_size):
        x = pop[i]
        x_op = lb + ub - x  # Basic Opposite

        # Sinh ngẫu nhiên để chọn chiến lược
        r = random.random()

        if r < P_reo:
            # CHIẾN LƯỢC REO (Reflected Extended Opposition)
            x_eo = np.zeros(dim)
            for j in range(dim):
                if x[j] < c[j]:
                    x_eo[j] = random.uniform(x_op[j], ub[j])
                else:
                    x_eo[j] = random.uniform(lb[j], x_op[j])
            chosen = lb + ub - x_eo  # x_reo

        elif r < P_reo + P_qr:
            # CHIẾN LƯỢC QR (Quasi-Reflection)
            x_qr = np.zeros(dim)
            for j in range(dim):
                if x[j] < c[j]:
                    x_qr[j] = random.uniform(x[j], c[j])
                else:
                    x_qr[j] = random.uniform(c[j], x[j])
            chosen = x_qr

        elif r < P_reo + P_qr + P_qo:
            # CHIẾN LƯỢC QO (Quasi-Opposition)
            x_qo = np.zeros(dim)
            for j in range(dim):
                if x[j] < c[j]:
                    x_qo[j] = random.uniform(c[j], x_op[j])
                else:
                    x_qo[j] = random.uniform(x_op[j], c[j])
            chosen = x_qo

        else:
            # CHIẾN LƯỢC EO (Extended Opposition)
            x_eo = np.zeros(dim)
            for j in range(dim):
                if x[j] < c[j]:
                    x_eo[j] = random.uniform(x_op[j], ub[j])
                else:
                    x_eo[j] = random.uniform(lb[j], x_op[j])
            chosen = x_eo

        # Ép biên đảm bảo nghiệm nằm trong miền [lb, ub]
        new_pop[i] = np.clip(chosen, lb, ub)
    
    return new_pop

def chaotic_local_search(best_sol, best_fit, pop, obj_func, lb, ub, local_search_limit=20):
    x = np.random.rand()    
    r = 4.0
    candidate = best_sol.copy()
    candidate_fit = best_fit

    pop_size, dim = pop.shape
    # chuyển lb/ub về dạng vector nếu cần
    lb_vec = np.array(lb)
    ub_vec = np.array(ub)

    for _ in range(local_search_limit):
        # logistic map
        x = r * x * (1 - x)
        chaotic_factor = x - 0.5

        # chọn hai cá thể ngẫu nhiên từ pop
        i, j = np.random.choice(pop_size, size=2, replace=False)
        xi = pop[i]
        xj = pop[j]

        # perturbation population-based
        perturb = chaotic_factor * (xi - xj)
        new_sol = candidate + perturb
        new_sol = np.clip(new_sol, lb_vec, ub_vec)

        new_fit = obj_func(new_sol)
        if new_fit < candidate_fit:
            candidate, candidate_fit = new_sol.copy(), new_fit

    return candidate, candidate_fit


# ------ Các hàm hỗ trợ seed và xuất Excel -----
def validate_seed(seed, run=None, function_name=None):
    try:
        seed = int(seed)
    except Exception as exc:
        raise ValueError(
            f"Seed không chuyển được sang int: {seed!r} "
            f"| Run={run}, Function={function_name}"
        ) from exc

    max_seed = int(np.iinfo(np.uint32).max)
    if seed < 0 or seed > max_seed:
        raise ValueError(
            f"Seed không hợp lệ: {seed} | Run={run}, Function={function_name}. "
            f"Seed phải nằm trong khoảng 0 đến {max_seed}."
        )
    return seed


def set_random_seed(seed):
    seed = validate_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    return seed


def make_function_seed_table(num_runs=50, function_names=None):
    """
    Cơ chế seed đơn giản cho COCSOS:
    - Mỗi cặp Run + Function được cấp đúng 1 seed riêng.
    - Seed được sinh ngẫu nhiên hợp lệ trong [0, 2**32 - 1].
    - Bảng seed này được lưu ra Excel để SOS đọc lại đúng seed tương ứng.
    """
    if function_names is None:
        function_names = list(functions.keys())

    rng = np.random.default_rng()
    total = int(num_runs) * len(function_names)
    seeds = []
    used = set()

    while len(seeds) < total:
        safe_max_seed = 2**31 - 1
        s = int(rng.integers(0, safe_max_seed + 1))
        if s not in used:
            used.add(s)
            seeds.append(s)

    records = []
    k = 0
    for run in range(1, int(num_runs) + 1):
        for func_name in function_names:
            records.append({
                "Run": run,
                "Function": str(func_name),
                "Seed": validate_seed(seeds[k], run, func_name),
            })
            k += 1

    return pd.DataFrame(records)


def check_seed_table(seed_table, num_runs, function_names):
    """Kiểm tra bảng seed đủ và hợp lệ trước khi chạy thuật toán."""
    required_cols = {"Run", "Function", "Seed"}
    missing = required_cols - set(seed_table.columns)
    if missing:
        raise ValueError(f"seed_table thiếu các cột: {missing}")

    seed_table["Run"] = seed_table["Run"].astype(int)
    seed_table["Function"] = seed_table["Function"].astype(str)
    seed_table["Seed"] = seed_table["Seed"].apply(validate_seed).astype(int)

    expected_rows = int(num_runs) * len(function_names)
    if len(seed_table) != expected_rows:
        raise ValueError(
            f"seed_table phải có {expected_rows} dòng = num_runs * số_function, "
            f"nhưng hiện có {len(seed_table)} dòng."
        )

    expected_pairs = {(run, str(fn)) for run in range(1, int(num_runs) + 1) for fn in function_names}
    actual_pairs = set(zip(seed_table["Run"], seed_table["Function"]))
    missing_pairs = expected_pairs - actual_pairs
    if missing_pairs:
        raise ValueError(f"seed_table thiếu cặp Run + Function: {sorted(missing_pairs)[:10]}")

    if seed_table.duplicated(subset=["Run", "Function"]).any():
        raise ValueError("seed_table bị trùng cặp Run + Function.")

    if seed_table.duplicated(subset=["Run", "Seed"]).any():
        raise ValueError("Có seed bị trùng giữa các Function trong cùng một Run.")

    return seed_table


def get_function_seed(seed_table, run, function_name):
    """Lấy seed ứng với đúng cặp Run + Function từ seed_table."""
    row = seed_table[
        (seed_table["Run"].astype(int) == int(run)) &
        (seed_table["Function"].astype(str) == str(function_name))
    ]
    if row.empty:
        raise ValueError(f"Không tìm thấy seed cho Run={run}, Function={function_name}")
    return validate_seed(row.iloc[0]["Seed"], run, function_name)


def array_to_excel_string(arr, precision=12):
    """Chuyển vector nghiệm sang chuỗi để ghi gọn vào Excel."""
    return np.array2string(
        np.asarray(arr),
        precision=precision,
        separator=', ',
        max_line_width=10_000
    )


def safe_sheet_name(name, suffix=""):
    """Tạo tên sheet Excel hợp lệ, tối đa 31 ký tự."""
    invalid_chars = ['\\', '/', '*', '?', ':', '[', ']']
    safe = str(name)
    for ch in invalid_chars:
        safe = safe.replace(ch, '_')
    max_len = 31 - len(suffix)
    return safe[:max_len] + suffix


# ------ COCSOS -----
def COCSOS(obj_func, bounds, dim, pop_size=50, max_iter=1000, seed=None):
    if seed is not None:
        set_random_seed(seed)

    start_time = time.time()
    lb = np.array([bounds[0]] * dim)
    ub = np.array([bounds[1]] * dim)

    # ==============================================================
    # 1) Khởi tạo dân số ngẫu nhiên ban đầu
    # ==============================================================
    pop_random_initial = np.random.uniform(lb, ub, (pop_size, dim))
    fitness_random_initial = np.array([obj_func(ind) for ind in pop_random_initial])

    initial_best_idx = int(np.argmin(fitness_random_initial))
    initial_best_sol = pop_random_initial[initial_best_idx].copy()
    initial_best_fit = float(fitness_random_initial[initial_best_idx])

    initial_info = {
        "Seed": int(seed) if seed is not None else None,
        "Initial Random Population": pop_random_initial.copy(),
        "Initial Random OF": fitness_random_initial.copy(),
        "Initial Best Index": initial_best_idx,
        "Initial Best Individual": initial_best_sol.copy(),
        "Initial Best OF": initial_best_fit,
    }

    # ==============================================================
    # 2) COCSOS tiếp tục dùng quần thể ban đầu này để tạo CO population
    # ==============================================================
    pop = co_population(pop_random_initial.copy(), lb, ub, iteration=0, max_iter=max_iter)
    fitness = np.array([obj_func(ind) for ind in pop])

    best_idx = np.argmin(fitness)
    best_sol = pop[best_idx].copy()
    best_fit = fitness[best_idx]
    best_fitness_history = [initial_best_fit]

    for iteration in range(1, max_iter + 1):
        # ===== Mutualism Phase =====
        for i in range(pop_size):
            best_idx = np.argmin(fitness)
            best_sol = pop[best_idx].copy()
            j = random_select(pop, i)
            mutual = (pop[i] + pop[j]) / 2.0
            bf1, bf2 = np.random.randint(1, 3, size=2)

            r1_val = np.random.rand(dim)
            new_ind1 = pop[i] + r1_val * (best_sol - bf1 * mutual)
            new_ind1 = np.clip(new_ind1, lb, ub)
            new_fit1 = obj_func(new_ind1)
            if new_fit1 < fitness[i]:
                pop[i] = new_ind1
                fitness[i] = new_fit1

            r2_val = np.random.rand(dim)
            new_ind2 = pop[j] + r2_val * (best_sol - bf2 * mutual)
            new_ind2 = np.clip(new_ind2, lb, ub)
            new_fit2 = obj_func(new_ind2)
            if new_fit2 < fitness[j]:
                pop[j] = new_ind2
                fitness[j] = new_fit2

            # ===== Commensalism Phase =====
            j = random_select(pop, i)
            r1 = np.random.uniform(-1, 1, dim)
            new_ind = pop[i] + r1 * (best_sol - pop[j])
            new_ind = np.clip(new_ind, lb, ub)
            new_fit = obj_func(new_ind)
            if new_fit < fitness[i]:
                pop[i] = new_ind
                fitness[i] = new_fit

            # ===== Parasitism Phase =====
            host_idx = np.random.choice([j for j in range(pop_size) if j != i])
            parasite_vector = pop[i].copy()
            n_changes = int(np.ceil(np.random.rand() * dim))
            pick_dims = np.random.choice(dim, size=n_changes, replace=False)

            for d_idx in pick_dims:
                parasite_vector[d_idx] = np.random.uniform(lb[d_idx], ub[d_idx])

            fitness_parasite = obj_func(parasite_vector)
            if fitness_parasite < fitness[host_idx]:
                pop[host_idx] = parasite_vector
                fitness[host_idx] = fitness_parasite

        # ===== Opposition Phase using Comprehensive Opposition (CO) =====
        if np.random.rand() < 0.4:
            co_pop2 = co_population(pop, lb, ub, iteration, max_iter)
            combined = np.vstack((pop, co_pop2))
            fitness_combined = np.array([obj_func(ind) for ind in combined])
            best_indices = np.argsort(fitness_combined)[:pop_size]
            pop = combined[best_indices]
            fitness = fitness_combined[best_indices]

        # Cập nhật best solution trước khi Chaotic Local Search
        best_idx = np.argmin(fitness)
        pre_cls_best_idx = np.argmin(fitness)
        if fitness[best_idx] < best_fit:
            best_sol = pop[best_idx].copy()
            best_fit = fitness[best_idx]

        # ============= Chaotic Local Search =============
        improved_sol, improved_fit = chaotic_local_search(
            best_sol, best_fit, pop, obj_func, lb, ub, local_search_limit=20
        )
        if improved_fit < best_fit:
            idx = pre_cls_best_idx        
            pop[idx] = improved_sol
            fitness[idx] = improved_fit
            best_sol = improved_sol.copy()
            best_fit = improved_fit

        best_idx_now = np.argmin(fitness)
        if fitness[best_idx_now] < best_fit:
            best_sol = pop[best_idx_now].copy()
            best_fit = fitness[best_idx_now]
        best_fitness_history.append(best_fit)

        best_fitness_history.append(best_fit)
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fit}")

    elapsed_time = time.time() - start_time
    print(f"Algorithm finished in {elapsed_time:.4f} seconds.")

    return best_sol, best_fit, elapsed_time, best_fitness_history, initial_info


# ------ Hàm run_all_benchmarks_excel: chạy 50 lần và xuất ra file Excel kết quả ------
def run_all_benchmarks_excel(
    excel_filename_prefix,
    num_runs=50,
    pop_size=50,
    max_iter=1000,
):
    """
    Chạy COCSOS nhiều lần và tự sinh seed theo từng cặp Run + Function.

    Cơ chế đơn giản:
    1) COCSOS tự tạo bảng seed: mỗi Function trong mỗi Run có 1 seed riêng.
    2) Trước khi chạy từng Function, code reset np.random và random bằng seed đó.
    3) Bảng seed được lưu vào file <prefix>_ALL_SUMMARY.xlsx, sheet Function_Seeds.
    4) SOS chỉ cần đọc sheet Function_Seeds này để lấy lại đúng seed tương ứng.

    Nhờ vậy, với cùng Run + Function + Seed + bounds + dim + pop_size,
    SOS và COCSOS có cùng quần thể khởi tạo ngẫu nhiên ban đầu.
    """
    function_names = list(functions.keys())

    # COCSOS là thuật toán chạy trước, nên nó tự sinh bảng seed và lưu lại.
    seed_table = make_function_seed_table(num_runs=num_runs, function_names=function_names)
    seed_table = check_seed_table(seed_table, num_runs=num_runs, function_names=function_names)

    all_summary_records = []
    all_seed_records = []

    experiment_info_df = pd.DataFrame({
        "Item": [
            "Algorithm",
            "Number of independent runs",
            "Population size",
            "Maximum iterations",
            "Seed source",
            "Seed protocol",
            "Random libraries reset",
            "Reproducibility condition"
        ],
        "Value": [
            "COCSOS",
            int(num_runs),
            int(pop_size),
            int(max_iter),
            "Generated once by COCSOS and saved to sheet Function_Seeds",
            "Each Run + Function pair uses one recorded seed.",
            "np.random.seed(seed) and random.seed(seed)",
            "SOS must read the same Function_Seeds sheet and use the same Function + Run seed."
        ]
    })

    for run in range(1, int(num_runs) + 1):
        results = []
        histories = {}
        initial_infos = {}
        seed_records_this_run = []

        print(f"========== COCSOS Run {run}/{num_runs} ==========")

        for name, (func, bound, global_min, dim) in functions.items():
            function_seed = get_function_seed(seed_table, run, name)

            print(f"Running function: {name} | Run = {run} | Seed = {function_seed}")
            best_sol, best_val, elapsed_time, best_history, initial_info = COCSOS(
                obj_func=func,
                bounds=bound,
                dim=dim,
                pop_size=pop_size,
                max_iter=max_iter,
                seed=function_seed,
            )

            result_row = {
                "Algorithm": "COCSOS",
                "Run": run,
                "Function": name,
                "Seed": function_seed,
                "Dimension": dim,
                "Bounds": str(bound),
                "Pop Size": pop_size,
                "Max Iter": max_iter,
                "Initial Best Index": initial_info["Initial Best Index"] + 1,
                "Initial Best OF": initial_info["Initial Best OF"],
                "Initial Best Individual": initial_info["Initial Best Individual"],
                "Best Solution": best_sol,
                "Best Fitness": best_val,
                "Theoretical Global Min": global_min,
                "Running Time (s)": elapsed_time,
            }
            results.append(result_row)
            all_summary_records.append(result_row.copy())

            histories[name] = best_history
            initial_infos[name] = initial_info

            seed_row = {
                "Algorithm": "COCSOS",
                "Run": run,
                "Function": name,
                "Seed": function_seed,
                "Seed Source": "Generated by COCSOS",
                "Dimension": dim,
                "Bounds": str(bound),
                "Pop Size": pop_size,
                "Max Iter": max_iter,
            }
            seed_records_this_run.append(seed_row)
            all_seed_records.append(seed_row.copy())

        summary_df = pd.DataFrame(results)
        summary_df["Initial Best Individual"] = summary_df["Initial Best Individual"].apply(array_to_excel_string)
        summary_df["Best Solution"] = summary_df["Best Solution"].apply(array_to_excel_string)

        seed_df = pd.DataFrame(seed_records_this_run)

        file_name = f"{excel_filename_prefix}_run_{run}.xlsx"
        with pd.ExcelWriter(file_name) as writer:
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
            experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

            for func_name, initial_info in initial_infos.items():
                init_pop = initial_info["Initial Random Population"]
                init_of = initial_info["Initial Random OF"]

                coord_cols = [f"x{j + 1}" for j in range(init_pop.shape[1])]
                df_init = pd.DataFrame(init_pop, columns=coord_cols)
                df_init.insert(0, "Initial Random OF", init_of)
                df_init.insert(0, "Individual", np.arange(1, len(init_pop) + 1))
                df_init.insert(0, "Seed", initial_info["Seed"])
                df_init.insert(0, "Run", run)
                df_init.insert(1, "Function", func_name)

                sheet_name = safe_sheet_name(func_name, suffix="_InitOF")
                df_init.to_excel(writer, sheet_name=sheet_name, index=False)

            for func_name, best_fitness_history in histories.items():
                df_history = pd.DataFrame({
                    "Iteration": np.arange(0, len(best_fitness_history)),
                    "Best Fitness": best_fitness_history,
                })
                sheet_name = safe_sheet_name(func_name)
                df_history.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Results for COCSOS run {run} exported to {file_name}\n")

    all_summary_df = pd.DataFrame(all_summary_records)
    if not all_summary_df.empty:
        all_summary_df["Initial Best Individual"] = all_summary_df["Initial Best Individual"].apply(array_to_excel_string)
        all_summary_df["Best Solution"] = all_summary_df["Best Solution"].apply(array_to_excel_string)

    all_seed_df = pd.DataFrame(all_seed_records)
    function_seed_df = seed_table.copy()
    if "Seed Source" not in function_seed_df.columns:
        function_seed_df["Seed Source"] = "Generated by COCSOS"

    all_file_name = f"{excel_filename_prefix}_ALL_SUMMARY.xlsx"
    with pd.ExcelWriter(all_file_name) as writer:
        all_summary_df.to_excel(writer, sheet_name="All_Summary", index=False)
        all_seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        function_seed_df.to_excel(writer, sheet_name="Function_Seeds", index=False)
        # Giữ thêm sheet này để dễ nhìn, dù hiện nay nó chứa seed theo từng Function.
        function_seed_df.to_excel(writer, sheet_name="Run_Function_Seeds", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

    print(f"All COCSOS runs summary exported to {all_file_name}")
    return function_seed_df


if __name__ == "__main__":
    excel_filename_prefix = "COCSOS_runs_seed_protocol_50dim"

    # Chạy chính thức 50 lần.
    run_all_benchmarks_excel(
        excel_filename_prefix,
        num_runs=50,
        pop_size=50,
        max_iter=1000,
    )
