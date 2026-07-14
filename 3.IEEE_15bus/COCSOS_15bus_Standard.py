import time
import numpy as np
import random
import math
import pandas as pd  # dùng để xuất kết quả ra Excel

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

def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    return TDS * (80/ (ratio**2- 1))
# Thay đổi hệ số để chọn đặc tính NI/VI/EI

def get_backup_current(primary_idx, count):
    backup_data = I_data_backup[primary_idx]
    if isinstance(backup_data, list):
        return backup_data[count % len(backup_data)] if backup_data else None
    return backup_data

def check_constraints(x) -> float:
    alpha_backup = 500
    alpha_primary_time = 56000  

    TDS_values = x[:D]
    PS_values = x[D:2*D]

    # 1. t_primary
    primary_times = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i])
                     for i in range(D)]
    penalty = 0.0
    for t in primary_times:
        penalty += alpha_primary_time * (max(0.0, 0.015 - t) ** 2)

    # 2. CTI between primary–backup
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx,
                                            primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        if backup_current is None:
            continue

        T_primary = primary_times[primary_idx]
        T_backup  = time_operation(TDS_values[backup_idx], CT[backup_idx] * PS_values[backup_idx], backup_current)
        violation  = max(0.0, CTI - (T_backup - T_primary))
        penalty   += alpha_backup * violation ** 2

    return penalty

def objective_function(x):
    TDS_values = x[:D]
    PS_values = x[D:2*D]
    
    # Tính tổng thời gian hoạt động của relay primary
    primary_times = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i])
                     for i in range(D)]
    primary_obj = sum(primary_times)
    
    # Tính hình phạt nếu có vi phạm ràng buộc
    penalty = check_constraints(x)
    
    return primary_obj + penalty

def print_detailed_results(best_solution, best_fitness):
    print("\nBest solution found:")
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2*D]
    print("TDS values:")
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        print(f"Relay {i+1}: TDS = {TDS_values[i]:.4f} sec, I_pickup = {I_pickup:.2f} A")
    print("\nPS values:")
    for i in range(D):
        print(f"Relay {i+1}: PS = {PS_values[i]:.4f} A")
        
    print(f"\nBest fitness (total operation time): {best_fitness:.4f} sec")
    
    print("\nOperation times for each relay:")
    primary_times = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i])
                     for i in range(D)]
    for i, t in enumerate(primary_times):
        print(f"Relay {i+1}: {t:.4f} sec")
    
    print("\nDetailed Backup Coordination Times:")
    header = f"{'Primary Relay':<15} {'Backup Relay':<15} {'Primary Time (sec)':<20} {'Backup Time (sec)':<20} {'Coordination Time (sec)':<25}"
    print(header)
    print("-" * len(header))
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        primary_time = time_operation(TDS_values[primary_idx], CT[primary_idx] * PS_values[primary_idx], I_data[primary_idx])
        backup_time = time_operation(TDS_values[backup_idx], CT[backup_idx] * PS_values[backup_idx], backup_current)
        coordination_time = backup_time - primary_time
        print(f"{primary_idx+1:<15} {backup_idx+1:<15} {primary_time:<20.4f} {backup_time:<20.4f} {coordination_time:<25.4f}")
    
    print("\nBackup Pair Input Data:")
    for primary_idx, backup_idx in backup_pairs:
        print(f"Relay {primary_idx+1}: I_data = {I_data[primary_idx]}")
        print(f"Relay {backup_idx+1}: I_data_backup = {I_data_backup[primary_idx]}")
        print("-----------------------------------------------------")
    
    print("\nChecking coordination for backup pairs:")
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        primary_time = time_operation(TDS_values[primary_idx], CT[primary_idx] * PS_values[primary_idx], I_data[primary_idx])
        backup_time = time_operation(TDS_values[backup_idx], CT[backup_idx] * PS_values[backup_idx], backup_current)
        if backup_time - primary_time >= CTI:
            print(f"Backup relay {backup_idx+1} coordinated with primary relay {primary_idx+1}: Success")
        else:
            print(f"Backup relay {backup_idx+1} failed to coordinate with primary relay {primary_idx+1}: Failure")

# ------------------ Hàm hỗ trợ để rời rạc hóa PS ------------------
def quantize_solution(x):
    D_local = len(x) // 2
    tds = x[:D_local]
    ps_cont = x[D_local:2*D_local]
    ps_quant = np.clip(np.round(ps_cont * 100000) / 100000, 0.5, 2.5)
    return np.concatenate((tds, ps_quant))

# ------------------ Các hàm hỗ trợ trong thuật toán COSOS ------------------
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

def chaotic_local_search(best_solution, best_fitness, pop, obj_func, lb, ub, local_search_limit=20):
    x = np.random.rand()    
    r = 4.0
    candidate = best_solution.copy()
    candidate_fit = best_fitness

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
        new_sol = quantize_solution(new_sol)
        new_sol = np.clip(new_sol, lb_vec, ub_vec)
        new_fit = obj_func(new_sol)
        if new_fit < candidate_fit:
            candidate, candidate_fit = new_sol.copy(), new_fit

    return candidate, candidate_fit


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
    Reset cả 2 bộ sinh số ngẫu nhiên đang dùng trong code:
    - numpy.random
    - random của Python
    """
    seed = validate_seed(seed, run=run)
    np.random.seed(seed)
    random.seed(seed)
    return seed


def make_run_seed_table(num_runs=50, master_seed=None):
    """
    Sinh bảng seed cho bài toán relay:
    - Mỗi Run có đúng 1 seed riêng.
    - Seed được sinh bằng Python int/np.int64, KHÔNG dùng np.uint32 để tránh lỗi
      bị hiểu nhầm thành số âm khi ép kiểu int32 trên một số môi trường.
    - Seed sinh ra nằm trong [0, 2**31 - 1]. Khoảng này vẫn hoàn toàn hợp lệ
      cho np.random.seed và random.seed, đồng thời an toàn khi ghi/đọc Excel.
    - Nếu master_seed=None: bảng seed được sinh ngẫu nhiên.
    - Nếu muốn sinh lại cùng bảng seed ở lần chạy khác, đặt master_seed cố định, ví dụ 2026.
    """
    if master_seed is None:
        rng = np.random.default_rng()
        seed_source = "Generated by COCSOS relay code"
    else:
        master_seed = validate_seed(master_seed)
        rng = np.random.default_rng(master_seed)
        seed_source = f"Generated by COCSOS relay code with master_seed={master_seed}"

    # Dùng 2**31 - 1 để tránh mọi trường hợp seed bị wrap sang số âm khi lưu/đọc Excel
    # hoặc khi môi trường tự ép kiểu signed int32.
    safe_max_seed = 2**31 - 1

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
        "Problem": ["Relay_TDS_PS_Optimization"] * int(num_runs),
        "Run": list(range(1, int(num_runs) + 1)),
        "Seed": [int(s) for s in seeds],
        "Seed Source": [seed_source] * int(num_runs)
    })


def check_seed_table(seed_table, num_runs):
    """Kiểm tra bảng seed đủ số dòng, không trùng run và seed hợp lệ."""
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

    return seed_table


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
        max_line_width=10_000
    )


def make_initial_population_df(initial_info, run, seed, dim):
    """
    Tạo bảng quần thể khởi tạo ngẫu nhiên ban đầu trước bước CO.
    Lưu cả nghiệm raw và OF tương ứng để SOS có thể kiểm tra/tái lập.
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

def COCSOS(obj_func, bounds, dim, pop_size=100, max_iter=3000, seed=None, run=None):
    """
    COCSOS cho bài toán relay có bổ sung seed protocol.

    Điểm quan trọng:
    - Nếu seed != None, reset np.random và random trước khi khởi tạo.
    - Lưu lại quần thể khởi tạo ngẫu nhiên ban đầu trước bước CO.
    - Lưu OF của từng cá thể trong quần thể khởi tạo ban đầu.
    """
    if seed is not None:
        seed = set_random_seed(seed, run=run)

    start_time = time.time()
    D_local = dim // 2
    lb = np.concatenate((np.array([bounds[0]] * D_local), np.array([0.5] * D_local)))
    ub = np.concatenate((np.array([bounds[1]] * D_local), np.array([2.5] * D_local)))

    # ==============================================================
    # 1) Khởi tạo quần thể ngẫu nhiên ban đầu bằng seed của Run hiện tại
    #    Đây là quần thể cần lưu để SOS dùng cùng seed/tái lập công bằng.
    # ==============================================================
    pop_random_initial = np.random.uniform(lb, ub, (pop_size, dim))
    pop_random_initial = np.array([quantize_solution(ind) for ind in pop_random_initial])
    fitness_random_initial = np.array([obj_func(ind) for ind in pop_random_initial])

    initial_best_idx = int(np.argmin(fitness_random_initial))
    initial_best_sol = pop_random_initial[initial_best_idx].copy()
    initial_best_fit = float(fitness_random_initial[initial_best_idx])

    initial_info = {
        "Run": int(run) if run is not None else None,
        "Seed": int(seed) if seed is not None else None,
        "Initial Random Population": pop_random_initial.copy(),
        "Initial Random OF": fitness_random_initial.copy(),
        "Initial Best Index": initial_best_idx,
        "Initial Best Individual": initial_best_sol.copy(),
        "Initial Best OF": initial_best_fit,
    }

    # ==============================================================
    # 2) COCSOS tiếp tục từ quần thể khởi tạo ban đầu để tạo CO population
    # ==============================================================
    pop = co_population(pop_random_initial.copy(), lb, ub, iteration=0, max_iter=max_iter)
    pop = np.array([quantize_solution(ind) for ind in pop])
    fitness = np.array([obj_func(ind) for ind in pop])

    best_idx = int(np.argmin(fitness))
    best_sol = pop[best_idx].copy()
    best_fit = float(fitness[best_idx])

    # Iteration 0 được dùng để ghi nhận best OF của quần thể khởi tạo ngẫu nhiên ban đầu.
    best_fitness_history = [initial_best_fit]

    for iteration in range(1, max_iter+1):
        # Mutualism Phase
        for i in range(pop_size):
            best_idx = np.argmin(fitness)
            best_sol = pop[best_idx].copy()
            j = random_select(pop, i)
            mutual = (pop[i] + pop[j]) / 2.0
            bf1, bf2 = np.random.randint(1, 3, size=2)  
            r1_val = np.random.rand(dim)
            new_ind1 = pop[i] + r1_val * (best_sol - bf1 * mutual)
            new_ind1 = np.clip(new_ind1, lb, ub)
            new_ind1 = quantize_solution(new_ind1)
            new_fit1 = obj_func(new_ind1)
            if new_fit1 < fitness[i]:
                pop[i] = new_ind1
                fitness[i] = new_fit1
            r2_val = np.random.rand(dim)
            new_ind2 = pop[j] + r2_val * (best_sol - bf2 * mutual)
            new_ind2 = np.clip(new_ind2, lb, ub)
            new_ind2 = quantize_solution(new_ind2)
            new_fit2 = obj_func(new_ind2)
            if new_fit2 < fitness[j]:
                pop[j] = new_ind2
                fitness[j] = new_fit2

        # Commensalism Phase
            j = random_select(pop, i)
            r = np.random.uniform(-1, 1, dim)
            new_ind = pop[i] + r * (best_sol - pop[j])
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
            co_pop2 = co_population(pop, lb, ub,iteration,max_iter)
            combined = np.vstack((pop, co_pop2))
            combined = np.array([quantize_solution(ind) for ind in combined])
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
        improved_sol, improved_fit = chaotic_local_search(best_sol, best_fit, pop, obj_func, lb, ub, local_search_limit=20)
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

        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fit}")

    elapsed_time = time.time() - start_time
    print_detailed_results(best_sol, best_fit)
    print(f"Algorithm finished in {elapsed_time:.4f} seconds.")
    return best_sol, best_fit, elapsed_time, best_fitness_history, initial_info


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
    # Tách vector giải pháp thành TDS và PS
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2*D]

    # Fitness History Sheet
    # Iteration 0 = best OF của quần thể khởi tạo ngẫu nhiên ban đầu.
    df_fitness = pd.DataFrame({
        "Iteration": list(range(0, len(best_fitness_history))),
        "Best Fitness": best_fitness_history,
        "elapsed_time": elapsed_time
    })

    # Relay Details Sheet
    relay_details = []
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        op_time = time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i])
        relay_details.append({
            "Relay": i+1,
            "TDS": TDS_values[i],
            "PS": PS_values[i],
            "I_pickup": I_pickup,
            "Operation Time": op_time
        })
    df_relays = pd.DataFrame(relay_details)

    # Backup Coordination Sheet
    backup_records = []
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        primary_time = time_operation(TDS_values[primary_idx], CT[primary_idx] * PS_values[primary_idx], I_data[primary_idx])
        backup_time = time_operation(TDS_values[backup_idx], CT[backup_idx] * PS_values[backup_idx],
                                     backup_current)
        coordination_time = backup_time - primary_time
        status = "Success" if coordination_time >= CTI else "Failure"
        backup_records.append({
            "Primary Relay": primary_idx+1,
            "Backup Relay": backup_idx+1,
            "Primary Time": primary_time,
            "Backup Time": backup_time,
            "Coordination Time": coordination_time,
            "CTI": CTI,
            "Status": status
        })
    df_backup = pd.DataFrame(backup_records)

    df_summary = pd.DataFrame({
        "Algorithm": ["COCSOS"],
        "Problem": ["Relay_TDS_PS_Optimization"],
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Dimension": [len(best_solution)],
        "D_Relay": [D],
        "Pop Size": [pop_size],
        "Max Iter": [max_iter],
        "Initial Best Index": [initial_info["Initial Best Index"] + 1],
        "Initial Best OF": [initial_info["Initial Best OF"]],
        "Initial Best Individual": [array_to_excel_string(initial_info["Initial Best Individual"])],
        "Elapsed Time (sec)": [elapsed_time],
        "Best Fitness": [best_fitness],
        "Best Solution": [array_to_excel_string(best_solution)]
    })

    df_seed = pd.DataFrame({
        "Algorithm": ["COCSOS"],
        "Problem": ["Relay_TDS_PS_Optimization"],
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Seed Source": ["Generated by COCSOS relay code"],
        "Random libraries reset": ["np.random.seed(seed) and random.seed(seed)"],
        "Reproducibility condition": [
            "Use the same Run seed, bounds, dim, pop_size, max_iter, quantize_solution, objective_function, and data."
        ]
    })

    df_initial_pop = make_initial_population_df(
        initial_info=initial_info,
        run=run,
        seed=seed,
        dim=len(best_solution)
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
            "Relay count D",
            "Total dimension",
            "Seed protocol",
            "Initial population sheet",
            "Initial OF definition",
            "Random libraries reset"
        ],
        "Value": [
            "COCSOS",
            "Relay_TDS_PS_Optimization",
            int(run),
            int(seed),
            pop_size,
            max_iter,
            str((0.1, 1.1)),
            str((0.5, 2.5)),
            D,
            len(best_solution),
            "Each independent run uses one recorded seed.",
            "Initial_Random_Pop",
            "Objective function value of each individual in the initial random population before CO.",
            "np.random.seed(seed) and random.seed(seed)"
        ]
    })

    with pd.ExcelWriter(filename) as writer:
        df_summary.to_excel(writer, sheet_name="Summary", index=False)
        df_seed.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        df_experiment.to_excel(writer, sheet_name="Experiment_Info", index=False)
        df_initial_pop.to_excel(writer, sheet_name="Initial_Random_Pop", index=False)
        df_fitness.to_excel(writer, sheet_name="Fitness History", index=False)
        df_relays.to_excel(writer, sheet_name="Relay Details", index=False)
        df_backup.to_excel(writer, sheet_name="Backup Coordination", index=False)

    print(f"Results exported to {filename}")

    return df_summary.iloc[0].to_dict()


# ------------------ Chạy thuật toán COCSOS nhiều lần và xuất Excel ------------------
if __name__ == "__main__":
    bounds = (0.1, 1.1)  # Biên cho TDS
    pop_size = 50
    max_iter = 5000       # Giá trị phù hợp với bài toán TDS
    total_dim = 2 * D     # 2*D (D cho TDS, D cho PS)
    num_runs = 30         # Chạy chính thức 50 lần; nếu test nhanh có thể đổi nhỏ hơn

    excel_filename_prefix = "COCSOS_15bus_TOF_TDS_newPS_EI_seed_protocol"

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
            "Relay count D",
            "Total dimension",
            "Seed source",
            "Seed generation range",
            "Seed protocol",
            "Random libraries reset",
            "Initial population saved",
            "Initial OF saved",
            "Reproducibility condition"
        ],
        "Value": [
            "COCSOS",
            "Relay_TDS_PS_Optimization",
            int(num_runs),
            int(pop_size),
            int(max_iter),
            str(bounds),
            str((0.1, 5)),
            D,
            total_dim,
            "Generated once by COCSOS and saved to sheet Run_Seeds",
            "0 to 2**31 - 1, valid for np.random.seed and safe for Excel/signed int32",
            "Each Run uses one recorded seed.",
            "np.random.seed(seed) and random.seed(seed)",
            "Yes, sheet Initial_Random_Pop in each run file",
            "Yes, column Initial Random OF in sheet Initial_Random_Pop",
            "SOS must read the same Run_Seeds sheet and use the same Run seed before initialization."
        ]
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
            run=run
        )

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
            max_iter=max_iter
        )

        all_summary_records.append(summary_record)
        all_seed_records.append({
            "Algorithm": "COCSOS",
            "Problem": "Relay_TDS_PS_Optimization",
            "Run": run,
            "Seed": int(run_seed),
            "Seed Source": "Generated by COCSOS relay code",
            "Pop Size": pop_size,
            "Max Iter": max_iter,
            "Dimension": total_dim
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
