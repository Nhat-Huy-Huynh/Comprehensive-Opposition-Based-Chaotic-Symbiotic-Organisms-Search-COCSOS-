import time
import numpy as np
import random
import math
import pandas as pd  # Dùng để xuất kết quả ra Excel

# ------------------ Dữ liệu và hàm của bài toán TDS ------------------
D = 42
I_data = [3621, 4597, 3984, 4382, 3319, 2647, 2497,
          4695, 2943, 3568, 4342, 4195, 3402, 4606, 4712,
          2225, 1875, 8426, 3998, 7662, 8384, 1950, 4910,
          2296, 2289, 2300, 2011, 2525, 8346, 1736, 2867,
          2069, 2305, 1715, 2095, 3283, 3301, 1403, 1434,
          3140, 1971, 3295]
I_data_backup = [1233, [1477,743], [853,743], [1111,1463,1808],
                 922, [1548,1100], [1397,1100], [1424,1463,1808],
                 [1397,1548], 1175, [1424,1111,1808], [1503,753],
                 1009, [1475,753], [853,1477], [1320,905],
                 [969,905], [1372,642,681], [1424,1111,1463],
                 [599,642,681], [599,1372,681], [979,970],
                 [1475,1503], [1326,970], [969,1320], [1192,1109],
                 [903,1109], [1828,697], [599,1372,642], [1039,697],
                 [1039,1828], [1162,907], [1326,979], [809,907],
                 [903,1192], 882, 910, 1403, 1434, 745,
                 [809,1162], 896]
backup_pairs = [(0,5),(1,3),(1,15),(2,0),(2,15),(3,6),(3,11),(3,19),
                (4,1),(5,7),(5,9),(6,4),(6,9),(7,2),(7,11),(7,19),
                (8,4),(8,7),(9,13),(10,2),(10,6),(10,19),(11,12),(11,23),
                (12,8),(13,10),(13,23),(14,0),(14,3),(15,17),(15,25),
                (16,14),(16,25),(17,18),(17,21),(17,29),(18,2),(18,6),
                (18,11),(19,16),(19,21),(19,29),(20,16),(20,18),(20,29),
                (21,22),(21,33),(22,10),(22,12),(23,20),(23,33),(24,14),
                (24,17),(25,27),(25,35),(26,24),(26,35),(27,28),(27,31),
                (28,16),(28,18),(28,21),(29,26),(29,31),(30,26),(30,28),
                (31,32),(31,41),(32,20),(32,22),(33,30),(33,41),(34,24),
                (34,27),(35,37),(36,34),(37,39),(38,36),(39,40),(40,30),
                (40,32),(41,38)]
CT = [160,240,160,240,160,120,120,240,120,160,240,240,160,240,
      240,120,80,320,160,320,320,80,240,120,120,120,120,120,320,
      80,120,120,120,80,120,160,160,80,80,160,80,160]
CTI = 0.2


# ------------------ Thiết lập biên biến tìm kiếm ------------------
TDS_LOWER_BOUND = 0.1
TDS_UPPER_BOUND = 1.1
PS_LOWER_BOUND = 0.5
PS_UPPER_BOUND = 2.5
A_LOWER_BOUND = 0.14
A_UPPER_BOUND = 80.0
B_LOWER_BOUND = 0.02
B_UPPER_BOUND = 2.0

PS_ROUND_DIGITS = 5
A_STEP = 0.01
B_STEP = 0.01

def build_bounds_vector(bounds, dim):
    """
    SOS muốn dùng cùng seed và sinh cùng quần thể ban đầu phải dùng đúng hàm này
    hoặc đúng cùng thứ tự lb/ub bên dưới.
    """
    expected_dim = 2 * D + 2
    if int(dim) != expected_dim:
        raise ValueError(f"dim phải bằng 2*D+2 = {expected_dim}, nhưng hiện là {dim}")

    lb_TDS = np.array([bounds[0]] * D)
    ub_TDS = np.array([bounds[1]] * D)
    lb_PS = np.array([PS_LOWER_BOUND] * D)
    ub_PS = np.array([PS_UPPER_BOUND] * D)
    lb_extra = np.array([A_LOWER_BOUND, B_LOWER_BOUND])
    ub_extra = np.array([A_UPPER_BOUND, B_UPPER_BOUND])

    lb = np.concatenate((lb_TDS, lb_PS, lb_extra))
    ub = np.concatenate((ub_TDS, ub_PS, ub_extra))
    return lb, ub


# ------------------ Hàm tính thời gian hoạt động của relay ------------------
def time_operation(TDS, Ipickup, I, A, B):
    ratio = I / Ipickup
    return TDS * (A / (ratio ** B - 1))


def get_backup_current(primary_idx, count):
    backup_data = I_data_backup[primary_idx]
    if isinstance(backup_data, list):
        return backup_data[count % len(backup_data)] if backup_data else None
    return backup_data


def check_constraints(x) -> float:
    alpha_backup = 500
    alpha_primary_time = 56000

    TDS_values = x[:D]
    PS_values = x[D:2 * D]
    A = x[2 * D]
    B = x[2 * D + 1]

    primary_times = [
        time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B)
        for i in range(D)
    ]

    penalty = 0.0
    for t in primary_times:
        penalty += alpha_primary_time * (max(0.0, 0.015 - t) ** 2)

    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        if backup_current is None:
            continue

        T_primary = primary_times[primary_idx]
        T_backup = time_operation(
            TDS_values[backup_idx],
            CT[backup_idx] * PS_values[backup_idx],
            backup_current,
            A,
            B,
        )
        violation = max(0.0, CTI - (T_backup - T_primary))
        penalty += alpha_backup * violation ** 2

    return penalty


def objective_function(x):
    # x có độ dài 2*D+2: TDS (0:D), PS (D:2*D), A và B (cuối vector)
    TDS_values = x[:D]
    PS_values = x[D:2 * D]
    A = x[2 * D]
    B = x[2 * D + 1]

    primary_times = [
        time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B)
        for i in range(D)
    ]
    primary_obj = sum(primary_times)
    penalty = check_constraints(x)
    return primary_obj + penalty


# ------------------ Hàm hỗ trợ rời rạc hóa PS ------------------
def quantize_solution(x):
    """
    - TDS: giữ liên tục
    - PS : làm tròn theo PS_ROUND_DIGITS
    - A  : rời rạc bước A_STEP = 0.01
    - B  : rời rạc bước B_STEP = 0.01
    """
    x = np.asarray(x, dtype=float)

    # TDS giữ liên tục
    tds = x[:D]

    # PS làm tròn 5 chữ số sau dấu phẩy, giống cơ chế seed protocol hiện tại
    ps_cont = x[D:2 * D]
    ps_quant = np.clip(
        np.round(ps_cont * (10 ** PS_ROUND_DIGITS)) / (10 ** PS_ROUND_DIGITS),
        PS_LOWER_BOUND,
        PS_UPPER_BOUND,
    )

    # A rời rạc theo bước 0.01
    A_cont = x[2 * D]
    A_quant = np.clip(
        np.round((A_cont - A_LOWER_BOUND) / A_STEP) * A_STEP + A_LOWER_BOUND,
        A_LOWER_BOUND,
        A_UPPER_BOUND,
    )
    A_quant = np.round(A_quant, 10)

    # B rời rạc theo bước 0.01
    B_cont = x[2 * D + 1]
    B_quant = np.clip(
        np.round((B_cont - B_LOWER_BOUND) / B_STEP) * B_STEP + B_LOWER_BOUND,
        B_LOWER_BOUND,
        B_UPPER_BOUND,
    )
    B_quant = np.round(B_quant, 10)

    return np.concatenate((tds, ps_quant, [A_quant, B_quant]))


# ------------------ Các hàm hỗ trợ seed và xuất Excel ------------------
def validate_seed(seed, run=None):
    """Đảm bảo seed hợp lệ cho np.random.seed và random.seed."""
    try:
        seed = int(seed)
    except Exception as exc:
        raise ValueError(f"Seed không chuyển được sang int: {seed!r} | Run={run}") from exc

    max_seed = int(np.iinfo(np.uint32).max)
    if seed < 0 or seed > max_seed:
        raise ValueError(
            f"Seed không hợp lệ: {seed} | Run={run}. "
            f"Seed phải nằm trong khoảng 0 đến {max_seed}."
        )
    return seed


def set_random_seed(seed, run=None):
    """
    Reset cả hai bộ sinh số ngẫu nhiên đang dùng trong code:
    - numpy.random
    - random của Python
    """
    seed = validate_seed(seed, run=run)
    np.random.seed(seed)
    random.seed(seed)
    return seed


def make_run_seed_table(num_runs=50, master_seed=None):
    """
    Sinh bảng seed cho bài toán 15-bus:
    - Mỗi Run có đúng 1 seed riêng.
    - Seed nằm trong [0, 2**31 - 1] để tránh lỗi số âm khi lưu/đọc Excel.
    - Nếu master_seed=None: mỗi lần chạy tạo bảng seed mới.
    - Nếu muốn tái tạo đúng cùng bảng seed: đặt master_seed cố định, ví dụ 2026.
    """
    if master_seed is None:
        rng = np.random.default_rng()
        seed_source = "Generated by COCSOS 15-bus AB-variable code"
    else:
        master_seed = validate_seed(master_seed)
        rng = np.random.default_rng(master_seed)
        seed_source = f"Generated by COCSOS 15-bus AB-variable code with master_seed={master_seed}"

    safe_max_seed = 2 ** 31 - 1
    seeds = []
    used = set()
    while len(seeds) < int(num_runs):
        s = int(rng.integers(0, safe_max_seed + 1))
        s = validate_seed(s, run=len(seeds) + 1)
        if s not in used:
            used.add(s)
            seeds.append(s)

    return pd.DataFrame({
        "Algorithm": ["COCSOS"] * int(num_runs),
        "Problem": ["Relay_TDS_PS_AB_Optimization_15bus"] * int(num_runs),
        "Run": list(range(1, int(num_runs) + 1)),
        "Seed": [int(s) for s in seeds],
        "Seed Source": [seed_source] * int(num_runs),
    })


def check_seed_table(seed_table, num_runs):
    """Kiểm tra bảng seed đủ số dòng, không trùng Run và seed hợp lệ."""
    required_cols = {"Run", "Seed"}
    missing = required_cols - set(seed_table.columns)
    if missing:
        raise ValueError(f"seed_table thiếu các cột: {missing}")

    seed_table = seed_table.copy()
    seed_table["Run"] = seed_table["Run"].astype(int)
    seed_table["Seed"] = seed_table.apply(
        lambda row: validate_seed(row["Seed"], run=row["Run"]), axis=1
    ).astype(int)

    if len(seed_table) != int(num_runs):
        raise ValueError(
            f"seed_table phải có {int(num_runs)} dòng = số lần chạy, "
            f"nhưng hiện có {len(seed_table)} dòng."
        )

    expected_runs = set(range(1, int(num_runs) + 1))
    actual_runs = set(seed_table["Run"])
    missing_runs = expected_runs - actual_runs
    if missing_runs:
        raise ValueError(f"seed_table thiếu Run: {sorted(missing_runs)}")

    if seed_table.duplicated(subset=["Run"]).any():
        raise ValueError("seed_table bị trùng Run.")

    if seed_table.duplicated(subset=["Seed"]).any():
        raise ValueError("Có seed bị trùng giữa các lần chạy.")

    return seed_table.sort_values("Run").reset_index(drop=True)


def get_run_seed(seed_table, run):
    """Lấy seed ứng với đúng Run."""
    row = seed_table[seed_table["Run"].astype(int) == int(run)]
    if row.empty:
        raise ValueError(f"Không tìm thấy seed cho Run={run}")
    return validate_seed(row.iloc[0]["Seed"], run=run)


def array_to_excel_string(arr, precision=12):
    """Chuyển vector nghiệm sang chuỗi để ghi gọn vào Excel summary."""
    return np.array2string(
        np.asarray(arr),
        precision=precision,
        separator=", ",
        max_line_width=10_000,
    )


def make_initial_population_df(initial_info, run, seed, dim):
    """
    Tạo bảng quần thể khởi tạo ngẫu nhiên ban đầu TRƯỚC bước CO.
    Đây là sheet quan trọng để kiểm tra SOS/thuật toán khác có cùng quần thể ban đầu hay không.
    """
    init_pop = initial_info["Initial Random Population"]
    init_of = initial_info["Initial Random OF"]

    coord_cols = [f"x{j + 1}" for j in range(dim)]
    df_init = pd.DataFrame(init_pop, columns=coord_cols)
    df_init.insert(0, "Initial Random OF", init_of)
    df_init.insert(0, "Individual", np.arange(1, len(init_pop) + 1))
    df_init.insert(0, "Seed", int(seed))
    df_init.insert(0, "Run", int(run))
    return df_init


def make_initialization_summary_df(initial_info, run, seed):
    return pd.DataFrame({
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Initial Random Best Index": [initial_info["Initial Best Index"] + 1],
        "Initial Random Best OF": [initial_info["Initial Best OF"]],
        "Initial Random Best Individual": [array_to_excel_string(initial_info["Initial Best Individual"])],
        "CO Initial Best Index": [initial_info["CO Initial Best Index"] + 1],
        "CO Initial Best OF": [initial_info["CO Initial Best OF"]],
        "CO Initial Best Individual": [array_to_excel_string(initial_info["CO Initial Best Individual"])],
    })


# ------------------ Các hàm hỗ trợ trong thuật toán COCSOS ------------------
def random_select(pop, i):
    candidates = [k for k in range(len(pop)) if k != i]
    return np.random.choice(candidates)


def co_population(pop, lb, ub, iteration, max_iter):
    pop_size, dim = pop.shape
    lb = np.array(lb)
    ub = np.array(ub)
    c = (lb + ub) / 2
    new_pop = np.zeros_like(pop)

    ratio = iteration / max_iter

    if 0 <= ratio <= 0.224:
        P_reo = 0.01
        P_qr = 0.01
        P_qo = 0.54 + 1.92 * ratio
    elif ratio > 0.723:
        P_reo = 0.01
        P_qr = 0.97
        P_qo = 0.01
    else:
        P_reo = 0.01
        P_qr = -0.42 + 1.92 * ratio
        P_qo = 1.4 - 1.92 * ratio

    for i in range(pop_size):
        x = pop[i]
        x_op = lb + ub - x
        r = random.random()

        if r < P_reo:
            x_eo = np.zeros(dim)
            for j in range(dim):
                if x[j] < c[j]:
                    x_eo[j] = random.uniform(x_op[j], ub[j])
                else:
                    x_eo[j] = random.uniform(lb[j], x_op[j])
            chosen = lb + ub - x_eo

        elif r < P_reo + P_qr:
            x_qr = np.zeros(dim)
            for j in range(dim):
                if x[j] < c[j]:
                    x_qr[j] = random.uniform(x[j], c[j])
                else:
                    x_qr[j] = random.uniform(c[j], x[j])
            chosen = x_qr

        elif r < P_reo + P_qr + P_qo:
            x_qo = np.zeros(dim)
            for j in range(dim):
                if x[j] < c[j]:
                    x_qo[j] = random.uniform(c[j], x_op[j])
                else:
                    x_qo[j] = random.uniform(x_op[j], c[j])
            chosen = x_qo

        else:
            x_eo = np.zeros(dim)
            for j in range(dim):
                if x[j] < c[j]:
                    x_eo[j] = random.uniform(x_op[j], ub[j])
                else:
                    x_eo[j] = random.uniform(lb[j], x_op[j])
            chosen = x_eo

        new_pop[i] = np.clip(chosen, lb, ub)

    return new_pop


def chaotic_local_search(best_solution, best_fitness, pop, obj_func, lb, ub, local_search_limit=20):
    x = np.random.rand()
    r = 4.0
    candidate = best_solution.copy()
    candidate_fit = best_fitness

    pop_size, dim = pop.shape
    lb_vec = np.array(lb)
    ub_vec = np.array(ub)

    for _ in range(local_search_limit):
        x = r * x * (1 - x)
        chaotic_factor = x - 0.5

        i, j = np.random.choice(pop_size, size=2, replace=False)
        xi = pop[i]
        xj = pop[j]

        perturb = chaotic_factor * (xi - xj)
        new_sol = candidate + perturb
        new_sol = np.clip(new_sol, lb_vec, ub_vec)
        new_sol = quantize_solution(new_sol)
        new_fit = obj_func(new_sol)
        if new_fit < candidate_fit:
            candidate, candidate_fit = new_sol.copy(), new_fit

    return candidate, candidate_fit


def print_detailed_results(best_solution, best_fitness):
    print("\nBest solution found:")
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2 * D]
    A = best_solution[2 * D]
    B = best_solution[2 * D + 1]

    print("TDS values:")
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        print(f"Relay {i + 1}: TDS = {TDS_values[i]:.4f} sec, I_pickup = {I_pickup:.2f} A")
    print("\nPS values:")
    for i in range(D):
        print(f"Relay {i + 1}: PS = {PS_values[i]:.4f} A")
    print(f"\nA = {A:.4f}, B = {B:.4f}")
    print(f"\nBest fitness: {best_fitness:.6f}")

    print("\nOperation times for each relay:")
    primary_times = [
        time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B)
        for i in range(D)
    ]
    for i, t in enumerate(primary_times):
        print(f"Relay {i + 1}: {t:.4f} sec")

    print("\nChecking coordination for backup pairs:")
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        primary_time = primary_times[primary_idx]
        backup_time = time_operation(
            TDS_values[backup_idx],
            CT[backup_idx] * PS_values[backup_idx],
            backup_current,
            A,
            B,
        )
        if backup_time - primary_time >= CTI:
            print(f"Backup relay {backup_idx + 1} coordinated with primary relay {primary_idx + 1}: Success")
        else:
            print(f"Backup relay {backup_idx + 1} failed to coordinate with primary relay {primary_idx + 1}: Failure")


# ------------------ Thuật toán COCSOS có seed protocol ------------------
def COCSOS(obj_func, bounds, dim, pop_size=100, max_iter=3000, seed=None, run=None):
    """
    COCSOS cho bài toán 15-bus tối ưu TDS, PS, A, B.
    """
    if seed is not None:
        seed = set_random_seed(seed, run=run)

    start_time = time.time()
    lb, ub = build_bounds_vector(bounds, dim)

    # ==============================================================
    # 1) Khởi tạo ngẫu nhiên ban đầu bằng seed của Run hiện tại
    # ==============================================================
    pop_random_initial = np.random.uniform(lb, ub, (pop_size, dim))
    pop_random_initial = np.array([quantize_solution(ind) for ind in pop_random_initial])
    fitness_random_initial = np.array([obj_func(ind) for ind in pop_random_initial])

    initial_best_idx = int(np.argmin(fitness_random_initial))
    initial_best_sol = pop_random_initial[initial_best_idx].copy()
    initial_best_fit = float(fitness_random_initial[initial_best_idx])

    # ==============================================================
    # 2) COCSOS 
    # ==============================================================
    pop = co_population(pop_random_initial.copy(), lb, ub, iteration=0, max_iter=max_iter)
    pop = np.array([quantize_solution(ind) for ind in pop])
    fitness = np.array([obj_func(ind) for ind in pop])

    co_best_idx = int(np.argmin(fitness))
    co_best_sol = pop[co_best_idx].copy()
    co_best_fit = float(fitness[co_best_idx])

    initial_info = {
        "Run": int(run) if run is not None else None,
        "Seed": int(seed) if seed is not None else None,
        "Initial Random Population": pop_random_initial.copy(),
        "Initial Random OF": fitness_random_initial.copy(),
        "Initial Best Index": initial_best_idx,
        "Initial Best Individual": initial_best_sol.copy(),
        "Initial Best OF": initial_best_fit,
        "CO Initial Population": pop.copy(),
        "CO Initial OF": fitness.copy(),
        "CO Initial Best Index": co_best_idx,
        "CO Initial Best Individual": co_best_sol.copy(),
        "CO Initial Best OF": co_best_fit,
    }

    best_idx = co_best_idx
    best_sol = co_best_sol.copy()
    best_fit = co_best_fit

    # Iteration 0 = best OF của quần thể khởi tạo ngẫu nhiên ban đầu trước CO.
    best_fitness_history = [initial_best_fit]

    for iteration in range(1, max_iter + 1):
        for i in range(pop_size):
            best_idx = int(np.argmin(fitness))
            best_sol_current = pop[best_idx].copy()

            # Mutualism Phase
            j = random_select(pop, i)
            mutual = (pop[i] + pop[j]) / 2.0
            bf1, bf2 = np.random.randint(1, 3, size=2)

            r1_val = np.random.rand(dim)
            new_ind1 = pop[i] + r1_val * (best_sol_current - bf1 * mutual)
            new_ind1 = np.clip(new_ind1, lb, ub)
            new_ind1 = quantize_solution(new_ind1)
            new_fit1 = obj_func(new_ind1)
            if new_fit1 < fitness[i]:
                pop[i] = new_ind1
                fitness[i] = new_fit1

            r2_val = np.random.rand(dim)
            new_ind2 = pop[j] + r2_val * (best_sol_current - bf2 * mutual)
            new_ind2 = np.clip(new_ind2, lb, ub)
            new_ind2 = quantize_solution(new_ind2)
            new_fit2 = obj_func(new_ind2)
            if new_fit2 < fitness[j]:
                pop[j] = new_ind2
                fitness[j] = new_fit2

            # Commensalism Phase
            j = random_select(pop, i)
            r = np.random.uniform(-1, 1, dim)
            new_ind = pop[i] + r * (best_sol_current - pop[j])
            new_ind = np.clip(new_ind, lb, ub)
            new_ind = quantize_solution(new_ind)
            new_fit = obj_func(new_ind)
            if new_fit < fitness[i]:
                pop[i] = new_ind
                fitness[i] = new_fit

            # Parasitism Phase
            host_idx = random_select(pop, i)
            parasite_vec = pop[i].copy()
            n_changes = int(np.ceil(np.random.rand() * dim))
            pick_dims = np.random.choice(dim, size=n_changes, replace=False)
            for d in pick_dims:
                parasite_vec[d] = np.random.uniform(lb[d], ub[d])
            parasite_vec = np.clip(parasite_vec, lb, ub)
            parasite_vec = quantize_solution(parasite_vec)
            parasite_fit = obj_func(parasite_vec)
            if parasite_fit < fitness[host_idx]:
                pop[host_idx] = parasite_vec
                fitness[host_idx] = parasite_fit

        # Opposition Phase using Comprehensive Opposition
        if np.random.rand() < 0.4:
            co_pop2 = co_population(pop, lb, ub, iteration, max_iter)
            combined = np.vstack((pop, co_pop2))
            combined = np.array([quantize_solution(ind) for ind in combined])
            fitness_combined = np.array([obj_func(ind) for ind in combined])
            best_indices = np.argsort(fitness_combined)[:pop_size]
            pop = combined[best_indices]
            fitness = fitness_combined[best_indices]

        best_idx = int(np.argmin(fitness))
        if fitness[best_idx] < best_fit:
            best_sol = pop[best_idx].copy()
            best_fit = float(fitness[best_idx])

        # Chaotic Local Search
        improved_sol, improved_fit = chaotic_local_search(best_sol,best_fit,pop,obj_func,lb,ub,local_search_limit=20)
        if improved_fit < best_fit:
            best_sol = improved_sol.copy()
            best_fit = float(improved_fit)

        worst_idx = int(np.argmax(fitness))
        if fitness[worst_idx] > best_fit:
            pop[worst_idx] = best_sol.copy()
            fitness[worst_idx] = best_fit

        best_fitness_history.append(float(best_fit))
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fit}")

    elapsed_time = time.time() - start_time
    print_detailed_results(best_sol, best_fit)
    print(f"Algorithm finished in {elapsed_time:.4f} seconds.")
    return best_sol, float(best_fit), elapsed_time, best_fitness_history, initial_info


# ------------------ Hàm xuất kết quả ra Excel ------------------
def export_results_to_excel(
    best_solution,
    best_fitness,
    elapsed_time,
    best_fitness_history,
    initial_info,
    seed,
    run,
    filename="optimization_results.xlsx",
    pop_size=None,
    max_iter=None,
):
    # Fitness History Sheet
    stages = ["Initial Random Best OF before CO"] + [f"After iteration {i}" for i in range(1, len(best_fitness_history))]
    df_fitness = pd.DataFrame({
        "Run": int(run),
        "Seed": int(seed),
        "Iteration": list(range(0, len(best_fitness_history))),
        "Stage": stages,
        "Best Fitness": best_fitness_history,
        "Elapsed Time (sec)": elapsed_time,
    })

    # Relay Details Sheet
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2 * D]
    A = best_solution[2 * D]
    B = best_solution[2 * D + 1]

    relay_data = []
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        op_time = time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B)
        relay_data.append({
            "Relay": i + 1,
            "TDS": TDS_values[i],
            "PS": PS_values[i],
            "A": A,
            "B": B,
            "I_pickup": I_pickup,
            "Operation Time": op_time,
        })
    df_relays = pd.DataFrame(relay_data)

    # Backup Coordination Sheet
    primary_times = [
        time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B)
        for i in range(D)
    ]
    backup_records = []
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        if backup_current is None:
            continue
        primary_time = primary_times[primary_idx]
        backup_time = time_operation(
            TDS_values[backup_idx],
            CT[backup_idx] * PS_values[backup_idx],
            backup_current,
            A,
            B,
        )
        coordination_time = backup_time - primary_time
        status = "Success" if coordination_time >= CTI else "Failure"
        backup_records.append({
            "Primary Relay": primary_idx + 1,
            "Backup Relay": backup_idx + 1,
            "Backup Current": backup_current,
            "Primary Operation Time": primary_time,
            "Backup Operation Time": backup_time,
            "Coordination Time": coordination_time,
            "CTI": CTI,
            "Status": status,
        })
    df_backup = pd.DataFrame(backup_records)

    df_summary = pd.DataFrame({
        "Algorithm": ["COCSOS"],
        "Problem": ["Relay_TDS_PS_AB_Optimization_15bus"],
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Dimension": [len(best_solution)],
        "D_Relay": [D],
        "Pop Size": [pop_size],
        "Max Iter": [max_iter],
        "Initial Random Best Index": [initial_info["Initial Best Index"] + 1],
        "Initial Random Best OF": [initial_info["Initial Best OF"]],
        "Initial Random Best Individual": [array_to_excel_string(initial_info["Initial Best Individual"])],
        "CO Initial Best Index": [initial_info["CO Initial Best Index"] + 1],
        "CO Initial Best OF": [initial_info["CO Initial Best OF"]],
        "CO Initial Best Individual": [array_to_excel_string(initial_info["CO Initial Best Individual"])],
        "Elapsed Time (sec)": [elapsed_time],
        "Best Fitness": [best_fitness],
        "Best Solution": [array_to_excel_string(best_solution)],
        "Best A": [A],
        "Best B": [B],
    })

    df_seed = pd.DataFrame({
        "Algorithm": ["COCSOS"],
        "Problem": ["Relay_TDS_PS_AB_Optimization_15bus"],
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Seed Source": ["Generated by COCSOS and saved in Run_Seeds sheet"],
        "Random libraries reset": ["np.random.seed(seed) and random.seed(seed)"],
        "Reproducibility condition": [
            "Use the same Run seed, bounds, dim=2*D+2, pop_size, quantize_solution, objective_function, and relay data."
        ],
    })

    df_initial_pop = make_initial_population_df(
        initial_info=initial_info,
        run=run,
        seed=seed,
        dim=len(best_solution),
    )

    df_init_summary = make_initialization_summary_df(
        initial_info=initial_info,
        run=run,
        seed=seed,
    )

    df_experiment = pd.DataFrame({
        "Item": [
            "Algorithm",
            "Problem",
            "Run",
            "Seed",
            "Population size",
            "Maximum iterations",
            "TDS bounds",
            "PS bounds",
            "A bounds",
            "B bounds",
            "Relay count D",
            "Total dimension",
            "Decision variable order",
            "Seed protocol",
            "Initial population sheet",
            "Initial OF definition",
            "Fitness History Iteration 0",
            "Random libraries reset",
            "Important fairness note for SOS",
        ],
        "Value": [
            "COCSOS",
            "Relay_TDS_PS_AB_Optimization_15bus",
            int(run),
            int(seed),
            pop_size,
            max_iter,
            str((TDS_LOWER_BOUND, TDS_UPPER_BOUND)),
            str((PS_LOWER_BOUND, PS_UPPER_BOUND)),
            str((A_LOWER_BOUND, A_UPPER_BOUND)),
            str((B_LOWER_BOUND, B_UPPER_BOUND)),
            D,
            len(best_solution),
            "[TDS_1..TDS_D, PS_1..PS_D, A, B]",
            "Each independent run uses one recorded seed.",
            "Initial_Random_Pop",
            "Objective function value of each individual in the initial random population before CO.",
            "Initial Random Best OF before CO.",
            "np.random.seed(seed) and random.seed(seed)",
            "SOS must read the same Run_Seeds sheet and use the same Run seed before initialization with identical bounds/dim/pop_size/quantize_solution.",
        ],
    })

    with pd.ExcelWriter(filename) as writer:
        df_summary.to_excel(writer, sheet_name="Summary", index=False)
        df_seed.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        df_experiment.to_excel(writer, sheet_name="Experiment_Info", index=False)
        df_init_summary.to_excel(writer, sheet_name="Initialization_Summary", index=False)
        df_initial_pop.to_excel(writer, sheet_name="Initial_Random_Pop", index=False)
        df_fitness.to_excel(writer, sheet_name="Fitness History", index=False)
        df_relays.to_excel(writer, sheet_name="Relay Details", index=False)
        df_backup.to_excel(writer, sheet_name="Backup Coordination", index=False)

    print(f"Results exported to {filename}")
    return df_summary.iloc[0].to_dict()


# ------------------ Chạy thuật toán COCSOS nhiều lần và xuất Excel ------------------
if __name__ == "__main__":
    bounds = (TDS_LOWER_BOUND, TDS_UPPER_BOUND)  # Miền cho TDS
    pop_size = 50
    max_iter = 5000
    total_dim = 2 * D + 2  # TDS (D), PS (D), A và B (2)
    num_runs = 20         # Khi chạy chính thức nên đổi thành 50

    excel_filename_prefix = "COCSOS_15bus_TOF_newPS_AB_chung_seed_protocol"

    master_seed = None

    # 1) Sinh seed khác nhau cho từng run và kiểm tra hợp lệ.
    seed_table = make_run_seed_table(num_runs=num_runs, master_seed=master_seed)
    seed_table = check_seed_table(seed_table, num_runs=num_runs)

    all_summary_records = []
    all_seed_records = []

    experiment_info_df = pd.DataFrame({
        "Item": [
            "Algorithm",
            "Problem",
            "Number of independent runs",
            "Population size",
            "Maximum iterations",
            "TDS bounds",
            "PS bounds",
            "A bounds",
            "B bounds",
            "Relay count D",
            "Total dimension",
            "Decision variable order",
            "Seed source",
            "Seed generation range",
            "Seed protocol",
            "Random libraries reset",
            "Initial population saved",
            "Initial OF saved",
            "Fitness History Iteration 0",
            "Reproducibility condition",
        ],
        "Value": [
            "COCSOS",
            "Relay_TDS_PS_AB_Optimization_15bus",
            int(num_runs),
            int(pop_size),
            int(max_iter),
            str(bounds),
            str((PS_LOWER_BOUND, PS_UPPER_BOUND)),
            str((A_LOWER_BOUND, A_UPPER_BOUND)),
            str((B_LOWER_BOUND, B_UPPER_BOUND)),
            D,
            total_dim,
            "[TDS_1..TDS_D, PS_1..PS_D, A, B]",
            "Generated once by COCSOS and saved to sheet Run_Seeds",
            "0 to 2**31 - 1, valid for np.random.seed and safe for Excel/signed int32",
            "Each Run uses one recorded seed.",
            "np.random.seed(seed) and random.seed(seed)",
            "Yes, sheet Initial_Random_Pop in each run file",
            "Yes, column Initial Random OF in sheet Initial_Random_Pop",
            "Initial Random Best OF before CO",
            "SOS must read the same Run_Seeds sheet and use the same Run seed before initialization with identical bounds/dim/pop_size/quantize_solution/objective_function/data.",
        ],
    })

    # 2) Chạy nhiều lần. Mỗi run dùng 1 seed riêng và lưu seed + quần thể ban đầu.
    for run in range(1, int(num_runs) + 1):
        run_seed = get_run_seed(seed_table, run)

        print(f"\n======== COCSOS RUN {run} / {num_runs} | Seed = {run_seed} ========")
        best_solution, best_fitness, elapsed_time, history, initial_info = COCSOS(
            objective_function,
            bounds,
            total_dim,
            pop_size=pop_size,
            max_iter=max_iter,
            seed=run_seed,
            run=run,
        )

        print("\nBest solution found:")
        print("TDS values:")
        print(best_solution[:D])
        print("PS values:")
        print(best_solution[D:2 * D])
        A = best_solution[2 * D]
        B = best_solution[2 * D + 1]
        print(f"A = {A:.4f}, B = {B:.4f}")
        print(f"Initial Random Best OF = {initial_info['Initial Best OF']:.6f}")
        print(f"CO Initial Best OF = {initial_info['CO Initial Best OF']:.6f}")
        print(f"Best fitness = {best_fitness:.6f}")
        print(f"Elapsed time: {elapsed_time:.4f} sec")

        filename = f"{excel_filename_prefix}_run_{run}.xlsx"
        summary_record = export_results_to_excel(
            best_solution=best_solution,
            best_fitness=best_fitness,
            elapsed_time=elapsed_time,
            best_fitness_history=history,
            initial_info=initial_info,
            seed=run_seed,
            run=run,
            filename=filename,
            pop_size=pop_size,
            max_iter=max_iter,
        )

        all_summary_records.append(summary_record)
        all_seed_records.append({
            "Algorithm": "COCSOS",
            "Problem": "Relay_TDS_PS_AB_Optimization_15bus",
            "Run": run,
            "Seed": int(run_seed),
            "Seed Source": "Generated by COCSOS 15-bus AB-variable code",
            "Pop Size": pop_size,
            "Max Iter": max_iter,
            "Dimension": total_dim,
            "Initial Random Best OF": initial_info["Initial Best OF"],
            "CO Initial Best OF": initial_info["CO Initial Best OF"],
        })

    # 3) Xuất file tổng hợp toàn bộ run và bảng seed để SOS đọc lại.
    all_summary_df = pd.DataFrame(all_summary_records)
    all_seed_df = pd.DataFrame(all_seed_records)

    summary_filename = f"{excel_filename_prefix}_ALL_SUMMARY.xlsx"
    with pd.ExcelWriter(summary_filename) as writer:
        all_summary_df.to_excel(writer, sheet_name="All_Summary", index=False)
        seed_table.to_excel(writer, sheet_name="Run_Seeds", index=False)
        all_seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

    print(f"\nSummary, seed protocol, and Run_Seeds exported to {summary_filename}")
