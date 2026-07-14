import numpy as np
import random
import time
import pandas as pd

# ---------------------- Benchmark Objective Functions ---------------------- #
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
#     "powell": (extended_powell_function, [-4, 5],0, 100),
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
# ------------------ Các hàm hỗ trợ seed protocol và xuất Excel ------------------ #
def validate_seed(seed, run=None, function_name=None):
    """
    Kiểm tra seed hợp lệ cho np.random.seed/random.seed.
    Seed phải nằm trong [0, 2**32 - 1].
    """
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


def check_seed_table(seed_table, num_runs, function_names):
    """Kiểm tra bảng seed đọc từ COCSOS có đủ và hợp lệ cho SOS."""
    required_cols = {"Run", "Function", "Seed"}
    missing = required_cols - set(seed_table.columns)
    if missing:
        raise ValueError(f"seed_table thiếu các cột: {missing}")

    seed_table = seed_table.copy()
    seed_table["Run"] = seed_table["Run"].astype(int)
    seed_table["Function"] = seed_table["Function"].astype(str)
    seed_table["Seed"] = seed_table.apply(
        lambda r: validate_seed(r["Seed"], r["Run"], r["Function"]), axis=1
    ).astype(int)

    expected_rows = int(num_runs) * len(function_names)
    if len(seed_table) != expected_rows:
        raise ValueError(
            f"seed_table phải có {expected_rows} dòng = num_runs * số_function, "
            f"nhưng hiện có {len(seed_table)} dòng. "
            "Hãy kiểm tra lại số function đang bật trong COCSOS và SOS có giống nhau không."
        )

    expected_pairs = {(run, str(fn)) for run in range(1, int(num_runs) + 1) for fn in function_names}
    actual_pairs = set(zip(seed_table["Run"], seed_table["Function"]))
    missing_pairs = expected_pairs - actual_pairs
    if missing_pairs:
        raise ValueError(
            f"seed_table thiếu cặp Run + Function so với danh sách function của SOS: "
            f"{sorted(missing_pairs)[:10]}"
        )

    if seed_table.duplicated(subset=["Run", "Function"]).any():
        raise ValueError("seed_table bị trùng cặp Run + Function.")

    if seed_table.duplicated(subset=["Run", "Seed"]).any():
        raise ValueError("Có seed bị trùng giữa các Function trong cùng một Run.")

    return seed_table


def load_seed_table_from_cocsos_excel(cocsos_summary_excel):
    """
    SOS đọc đúng bảng seed do COCSOS đã sinh và lưu.
    File COCSOS cần có sheet Function_Seeds hoặc Seed_Protocol với cột Run, Function, Seed.
    """
    preferred_sheets = ["Function_Seeds", "Seed_Protocol", "Run_Function_Seeds"]
    last_error = None

    for sheet_name in preferred_sheets:
        try:
            df_seed = pd.read_excel(cocsos_summary_excel, sheet_name=sheet_name)
            required = {"Run", "Function", "Seed"}
            if required.issubset(df_seed.columns):
                keep_cols = [c for c in [
                    "Algorithm", "Run", "Function", "Seed", "Seed Source",
                    "Dimension", "Bounds", "Pop Size", "Max Iter"
                ] if c in df_seed.columns]
                df_seed = df_seed[keep_cols].copy()
                df_seed["Run"] = df_seed["Run"].astype(int)
                df_seed["Function"] = df_seed["Function"].astype(str)
                df_seed["Seed"] = df_seed.apply(
                    lambda r: validate_seed(r["Seed"], r["Run"], r["Function"]), axis=1
                ).astype(int)
                return df_seed.sort_values(["Run", "Function"]).reset_index(drop=True)
        except Exception as exc:
            last_error = exc

    raise ValueError(
        "Không đọc được bảng seed từ file COCSOS. "
        "Cần sheet Function_Seeds hoặc Seed_Protocol có các cột Run, Function, Seed."
    ) from last_error


def get_function_seed(seed_table, run, function_name):
    """Lấy seed ứng với đúng cặp Run + Function từ bảng seed của COCSOS."""
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


# ------------------ SOS Algorithm với Parasitism, seed protocol và lưu OF ban đầu ------------------ #
def SOS(obj_func, bounds, dim, pop_size=50, max_iter=1000, seed=None):
    """
    SOS có bổ sung seed protocol và lưu thông tin OF ban đầu.

    initial_info trả về gồm:
    - Seed đang dùng
    - Quần thể ngẫu nhiên ban đầu ngay sau np.random.uniform
    - Giá trị OF của từng cá thể ban đầu
    - Cá thể có OF tốt nhất trong quần thể ngẫu nhiên ban đầu
    - Giá trị OF tốt nhất ban đầu

    Ghi chú công bằng với COCSOS:
    - Với cùng seed, bounds, dim, pop_size, quần thể initial random của SOS sẽ giống
      quần thể pop_random_initial của COCSOS trước khi COCSOS áp dụng CO.
    - Sau bước khởi tạo, hai thuật toán sẽ khác nhau nên kết quả cuối không bắt buộc giống nhau.
    """
    if seed is not None:
        set_random_seed(seed)

    lower_bound = np.array([bounds[0]] * dim)
    upper_bound = np.array([bounds[1]] * dim)
    start_time = time.time()

    # ==============================================================
    # 1) Khởi tạo dân số ngẫu nhiên ban đầu
    # ==============================================================
    initial_random_population = np.random.uniform(lower_bound, upper_bound, (pop_size, dim))
    initial_random_of = np.array([obj_func(ind) for ind in initial_random_population])

    initial_best_idx = int(np.argmin(initial_random_of))
    initial_best_solution = initial_random_population[initial_best_idx].copy()
    initial_best_of = float(initial_random_of[initial_best_idx])

    initial_info = {
        "Seed": int(seed) if seed is not None else None,
        "Initial Random Population": initial_random_population.copy(),
        "Initial Random OF": initial_random_of.copy(),
        "Initial Best Index": initial_best_idx,
        "Initial Best Individual": initial_best_solution.copy(),
        "Initial Best OF": initial_best_of,
    }

    # ==============================================================
    # 2) SOS 
    # ==============================================================
    population = initial_random_population.copy()
    fitness = initial_random_of.copy()

    best_idx = int(np.argmin(fitness))
    best_solution = population[best_idx].copy()
    best_value = float(fitness[best_idx])

    best_fitness_history = [best_value]

    for iteration in range(1, max_iter + 1):
        # ---------------- Mutualism phase ----------------
        for i in range(pop_size):
            best_idx = int(np.argmin(fitness))
            best_solution = population[best_idx].copy()
            partner_idx = np.random.choice([j for j in range(pop_size) if j != i])
            mutual_vector = (population[i] + population[partner_idx]) / 2.0

            bf1, bf2 = np.random.randint(1, 3, size=2)
            r1 = np.random.rand(dim)
            r2 = np.random.rand(dim)
            new_ind1 = population[i] + r1 * (best_solution - mutual_vector * bf1)
            new_ind2 = population[partner_idx] + r2 * (best_solution - mutual_vector * bf2)

            new_ind1 = np.clip(new_ind1, lower_bound, upper_bound)
            new_ind2 = np.clip(new_ind2, lower_bound, upper_bound)

            new_fitness1 = obj_func(new_ind1)
            new_fitness2 = obj_func(new_ind2)

            if new_fitness1 < fitness[i]:
                population[i] = new_ind1
                fitness[i] = new_fitness1
            if new_fitness2 < fitness[partner_idx]:
                population[partner_idx] = new_ind2
                fitness[partner_idx] = new_fitness2

            # ---------------- Commensalism phase ----------------
            partner_idx = np.random.choice([j for j in range(pop_size) if j != i])
            r3 = np.random.uniform(-1, 1, dim)
            new_ind = population[i] + r3 * (best_solution - population[partner_idx])
            new_ind = np.clip(new_ind, lower_bound, upper_bound)
            new_fitness = obj_func(new_ind)
            if new_fitness < fitness[i]:
                population[i] = new_ind
                fitness[i] = new_fitness

            # ---------------- Parasitism phase ----------------
            partner_idx = np.random.choice([j for j in range(pop_size) if j != i])
            parasite_vector = population[i].copy()
            n_changes = int(np.ceil(np.random.rand() * dim))
            pick_dims = np.random.choice(dim, size=n_changes, replace=False)
            parasite_vector[pick_dims] = np.random.uniform(lower_bound[pick_dims], upper_bound[pick_dims])

            fitness_parasite = obj_func(parasite_vector)
            if fitness_parasite < fitness[partner_idx]:
                population[partner_idx] = parasite_vector
                fitness[partner_idx] = fitness_parasite

        best_idx = int(np.argmin(fitness))
        best_solution = population[best_idx].copy()
        best_value = float(fitness[best_idx])

        best_fitness_history.append(best_value)

        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_value}")

    elapsed_time = time.time() - start_time
    return best_solution, best_value, elapsed_time, best_fitness_history, initial_info


# ------------------ Chạy thuật toán SOS cho tất cả các hàm và xuất kết quả ra Excel ------------------ #
def run_sos_for_all_functions(
    excel_filename_prefix,
    cocsos_seed_excel="COCSOS_runs_seed_protocol_ALL_SUMMARY.xlsx",
    pop_size=50,
    max_iter=1000,
):
    """
    Chạy SOS bằng đúng seed do COCSOS đã sinh.

    Cơ chế đơn giản:
    1) COCSOS chạy trước và lưu bảng seed ở sheet Function_Seeds.
    2) SOS đọc file COCSOS_runs_seed_protocol_ALL_SUMMARY.xlsx.
    3) Với từng Run + Function, SOS lấy đúng seed tương ứng.
    4) SOS reset np.random và random bằng seed đó trước khi khởi tạo quần thể.

    Nhờ vậy, SOS và COCSOS dùng cùng quần thể khởi tạo ngẫu nhiên ban đầu
    cho cùng một Function trong cùng một Run.
    """
    function_names = list(functions.keys())

    seed_table = load_seed_table_from_cocsos_excel(cocsos_seed_excel)
    num_runs = int(seed_table["Run"].max())
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
            "SOS",
            int(num_runs),
            int(pop_size),
            int(max_iter),
            cocsos_seed_excel,
            "SOS reads the seed generated by COCSOS for each Run + Function pair.",
            "np.random.seed(seed) and random.seed(seed)",
            "For each Function + Run, SOS uses the same recorded seed as COCSOS before initial population generation."
        ]
    })

    for run in range(1, int(num_runs) + 1):
        results_summary = []
        history_dict = {}
        initial_infos = {}
        seed_records_this_run = []

        print(f"\n***** SOS Run {run}/{num_runs} *****")

        for func_name, (obj_func, bounds, global_min, dim) in functions.items():
            function_seed = get_function_seed(seed_table, run, func_name)

            print(f"Running function: {func_name} | Run = {run} | Seed = {function_seed}")

            best_solution, best_value, elapsed_time, best_fitness_history, initial_info = SOS(
                obj_func=obj_func,
                bounds=bounds,
                dim=dim,
                pop_size=pop_size,
                max_iter=max_iter,
                seed=function_seed,
            )

            print(f"Initial best OF for {func_name}: {initial_info['Initial Best OF']:.12f}")
            print(f"Optimal solution for {func_name}: {best_solution}")
            print(f"Function value at optimal solution: {best_value:.12f}")
            print(f"Global minimum value: {global_min}")
            print(f"Running Time: {elapsed_time:.4f} seconds")
            print('-' * 60)

            result_row = {
                "Algorithm": "SOS",
                "Run": run,
                "Function": func_name,
                "Seed": function_seed,
                "Dimension": dim,
                "Bounds": str(bounds),
                "Pop Size": pop_size,
                "Max Iter": max_iter,
                "Initial Best Index": initial_info["Initial Best Index"] + 1,
                "Initial Best OF": initial_info["Initial Best OF"],
                "Initial Best Individual": initial_info["Initial Best Individual"],
                "Best Solution": best_solution,
                "Best Fitness": best_value,
                "Global Minimum": global_min,
                "Running Time (s)": elapsed_time,
            }
            results_summary.append(result_row)
            all_summary_records.append(result_row.copy())

            history_dict[func_name] = best_fitness_history
            initial_infos[func_name] = initial_info

            seed_row = {
                "Algorithm": "SOS",
                "Run": run,
                "Function": func_name,
                "Seed": function_seed,
                "Seed Source": "Read from COCSOS Function_Seeds",
                "Dimension": dim,
                "Bounds": str(bounds),
                "Pop Size": pop_size,
                "Max Iter": max_iter,
            }
            seed_records_this_run.append(seed_row)
            all_seed_records.append(seed_row.copy())

        df_summary = pd.DataFrame(results_summary)
        df_summary["Initial Best Individual"] = df_summary["Initial Best Individual"].apply(array_to_excel_string)
        df_summary["Best Solution"] = df_summary["Best Solution"].apply(array_to_excel_string)
        df_seed = pd.DataFrame(seed_records_this_run)

        excel_filename = f"{excel_filename_prefix}_run_{run}.xlsx"
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
            df_seed.to_excel(writer, sheet_name='Seed_Protocol', index=False)
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

            for func_name, hist in history_dict.items():
                df_hist = pd.DataFrame({
                    'Iteration': range(len(hist)),
                    'Best Fitness': hist,
                })
                sheet_name = safe_sheet_name(func_name)
                df_hist.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Results have been exported to {excel_filename}")

    all_summary_df = pd.DataFrame(all_summary_records)
    if not all_summary_df.empty:
        all_summary_df["Initial Best Individual"] = all_summary_df["Initial Best Individual"].apply(array_to_excel_string)
        all_summary_df["Best Solution"] = all_summary_df["Best Solution"].apply(array_to_excel_string)

    all_seed_df = pd.DataFrame(all_seed_records)
    function_seed_df = seed_table.copy()
    if "Seed Source" not in function_seed_df.columns:
        function_seed_df["Seed Source"] = "Read from COCSOS Function_Seeds"

    all_file_name = f"{excel_filename_prefix}_ALL_SUMMARY.xlsx"
    with pd.ExcelWriter(all_file_name, engine='openpyxl') as writer:
        all_summary_df.to_excel(writer, sheet_name="All_Summary", index=False)
        all_seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        function_seed_df.to_excel(writer, sheet_name="Function_Seeds", index=False)
        function_seed_df.to_excel(writer, sheet_name="Run_Function_Seeds", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

    print(f"All SOS runs summary exported to {all_file_name}")
    return function_seed_df


# ------------------ Main ------------------ #
if __name__ == "__main__":
    excel_filename_prefix = "SOS_runs_seed_protocol_50dim"

    cocsos_seed_excel = "COCSOS_runs_seed_protocol_50dim_ALL_SUMMARY.xlsx"
    run_sos_for_all_functions(
        excel_filename_prefix=excel_filename_prefix,
        cocsos_seed_excel=cocsos_seed_excel,
        pop_size=50,
        max_iter=1000,
    )

