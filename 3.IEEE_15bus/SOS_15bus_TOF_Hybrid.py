import os
import time
import numpy as np
import random
import pandas as pd

# ==============================================================
# SOS - 15 bus - số biến tìm kiếm 3D
# Vector nghiệm x = [TDS_1..TDS_D, PS_1..PS_D, mode_1..mode_D]
# mode: 0 = NI, 1 = VI, 2 = EI
# ============================================================== 

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
mode_names = {0: "NI", 1: "VI", 2: "EI"}

TDS_LOWER_BOUND = 0.1
TDS_UPPER_BOUND = 1.1
PS_LOWER_BOUND = 0.5
PS_UPPER_BOUND = 2.5
MODE_LOWER_BOUND = 0
MODE_UPPER_BOUND = 2
PS_ROUND_DIGITS = 5


# ------------------ Hàm tính toán bài toán ------------------
def time_operation(TDS, Ipickup, I, mode):
    """Tính thời gian hoạt động theo đặc tính NI/VI/EI."""
    ratio = I / Ipickup
    mode = int(np.clip(np.rint(mode), 0, 2))
    if mode == 0:      # NI
        A, B = 0.14, 0.02
    elif mode == 1:    # VI
        A, B = 13.5, 1.0
    else:              # EI
        A, B = 80.0, 2.0

    denominator = ratio ** B - 1.0
    if denominator <= 0 or not np.isfinite(denominator):
        return float("inf")
    return TDS * (A / denominator)


def get_backup_current(primary_idx, count):
    backup_data = I_data_backup[primary_idx]
    if isinstance(backup_data, list):
        return backup_data[count % len(backup_data)] if backup_data else None
    return backup_data


def discretize_ps(ps):
    ps = np.asarray(ps, dtype=float)
    return np.clip(np.round(ps * 100000) / 100000, PS_LOWER_BOUND, PS_UPPER_BOUND)


def mode_to_int(mode):
    """Làm tròn mode theo cơ chế code cũ: int(np.clip(np.rint(mode), 0, 2))."""
    return int(np.clip(np.rint(mode), MODE_LOWER_BOUND, MODE_UPPER_BOUND))


def split_solution(x):
    """Tách nghiệm theo cơ chế code cũ: TDS liên tục, PS rời rạc, mode làm tròn khi dùng."""
    x = np.asarray(x, dtype=float)
    TDS_values = x[:D]
    PS_values = discretize_ps(x[D:2 * D])
    mode_values = x[2 * D:3 * D]
    return TDS_values, PS_values, mode_values


def check_constraints(x) -> float:
    alpha_backup = 500
    alpha_primary_time = 56000

    TDS_values, PS_values, mode_values = split_solution(x)

    primary_times = []
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        primary_times.append(time_operation(TDS_values[i], I_pickup, I_data[i], mode_values[i]))

    penalty = 0.0
    for t in primary_times:
        if not np.isfinite(t):
            penalty += 1e12
        else:
            penalty += alpha_primary_time * (max(0.0, 0.015 - t) ** 2)

    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        if backup_current is None:
            continue

        T_primary = primary_times[primary_idx]
        I_pickup_backup = CT[backup_idx] * PS_values[backup_idx]
        T_backup = time_operation(TDS_values[backup_idx], I_pickup_backup, backup_current, mode_values[backup_idx])

        if not np.isfinite(T_primary) or not np.isfinite(T_backup):
            penalty += 1e12
            continue

        violation = max(0.0, CTI - (T_backup - T_primary))
        penalty += alpha_backup * violation ** 2

    return penalty


def objective_function(x):
    TDS_values, PS_values, mode_values = split_solution(x)
    base_obj = 0.0
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        t = time_operation(TDS_values[i], I_pickup, I_data[i], mode_values[i])
        if not np.isfinite(t):
            base_obj += 1e12
        else:
            base_obj += t
    penalty = check_constraints(x)
    return float(base_obj + penalty)


# ------------------ In và tạo bảng kết quả chi tiết ------------------
def print_detailed_results(best_solution, best_fitness):
    print("\nBest solution found:")
    TDS_values, PS_values, mode_values = split_solution(best_solution)

    print("Relay details:")
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        print(
            f"Relay {i + 1}: TDS = {TDS_values[i]:.4f} sec, "
            f"PS = {PS_values[i]:.5f}, I_pickup = {I_pickup:.2f} A, "
            f"Mode = {mode_names[mode_to_int(mode_values[i])]}"
        )

    print(f"\nBest fitness: {best_fitness:.6f}")

    print("\nDetailed Backup Coordination Times:")
    header = f"{'Primary Relay':<15} {'Backup Relay':<15} {'Primary Time':<16} {'Backup Time':<16} {'Coordination Time':<20}"
    print(header)
    print("-" * len(header))
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        primary_time = time_operation(
            TDS_values[primary_idx], CT[primary_idx] * PS_values[primary_idx], I_data[primary_idx], mode_values[primary_idx]
        )
        backup_time = time_operation(
            TDS_values[backup_idx], CT[backup_idx] * PS_values[backup_idx], backup_current, mode_values[backup_idx]
        )
        coordination_time = backup_time - primary_time
        print(f"{primary_idx + 1:<15} {backup_idx + 1:<15} {primary_time:<16.6f} {backup_time:<16.6f} {coordination_time:<20.6f}")


def get_relay_details_df(best_solution):
    TDS_values, PS_values, mode_values = split_solution(best_solution)
    rows = []
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        op_time = time_operation(TDS_values[i], I_pickup, I_data[i], mode_values[i])
        rows.append({
            "Relay": i + 1,
            "TDS": TDS_values[i],
            "PS": PS_values[i],
            "Mode_Value": mode_to_int(mode_values[i]),
            "Mode_Name": mode_names[mode_to_int(mode_values[i])],
            "CT": CT[i],
            "I_pickup": I_pickup,
            "I_primary": I_data[i],
            "Operation Time": op_time,
        })
    return pd.DataFrame(rows)


def get_backup_coordination_df(best_solution):
    TDS_values, PS_values, mode_values = split_solution(best_solution)
    rows = []
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        primary_time = time_operation(
            TDS_values[primary_idx], CT[primary_idx] * PS_values[primary_idx], I_data[primary_idx], mode_values[primary_idx]
        )
        backup_time = time_operation(
            TDS_values[backup_idx], CT[backup_idx] * PS_values[backup_idx], backup_current, mode_values[backup_idx]
        )
        coordination_time = backup_time - primary_time
        rows.append({
            "Primary Relay": primary_idx + 1,
            "Backup Relay": backup_idx + 1,
            "Primary Mode Value": mode_to_int(mode_values[primary_idx]),
            "Primary Mode Name": mode_names[mode_to_int(mode_values[primary_idx])],
            "Backup Mode Value": mode_to_int(mode_values[backup_idx]),
            "Backup Mode Name": mode_names[mode_to_int(mode_values[backup_idx])],
            "Primary Current": I_data[primary_idx],
            "Backup Current": backup_current,
            "Primary Time (sec)": primary_time,
            "Backup Time (sec)": backup_time,
            "Coordination Time (sec)": coordination_time,
            "CTI": CTI,
            "Status": "Success" if coordination_time >= CTI else "Failure",
        })
    return pd.DataFrame(rows)


# ------------------ Seed protocol: đọc seed từ COCSOS ------------------
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
    seed = validate_seed(seed, run=run)
    np.random.seed(seed)
    random.seed(seed)
    return seed


def read_cocsos_seed_table(cocsos_seed_excel, num_runs=None):
    """
    Đọc seed do COCSOS 3D đã xuất ra Excel.
    Ưu tiên sheet Run_Seeds trong file:
        COCSOS_15bus_TOF_newPS_mix_3D_seed_protocol_ALL_SUMMARY.xlsx
    """
    if not os.path.exists(cocsos_seed_excel):
        raise FileNotFoundError(
            f"Không tìm thấy file seed Excel của COCSOS: {cocsos_seed_excel}\n"
            "Hãy đặt file này cùng thư mục với code SOS hoặc sửa biến COCSOS_SEED_EXCEL."
        )

    try:
        seed_table = pd.read_excel(cocsos_seed_excel, sheet_name="Run_Seeds")
        seed_sheet = "Run_Seeds"
    except Exception:
        seed_table = pd.read_excel(cocsos_seed_excel, sheet_name="Seed_Protocol")
        seed_sheet = "Seed_Protocol"

    required_cols = {"Run", "Seed"}
    missing = required_cols - set(seed_table.columns)
    if missing:
        raise ValueError(f"File seed COCSOS thiếu các cột: {missing}. Sheet đọc được: {seed_sheet}")

    seed_table = seed_table.copy()
    seed_table["Run"] = seed_table["Run"].astype(int)
    seed_table["Seed"] = seed_table.apply(lambda row: validate_seed(row["Seed"], run=row["Run"]), axis=1).astype(int)
    seed_table = seed_table.sort_values("Run").reset_index(drop=True)

    if seed_table.duplicated(subset=["Run"]).any():
        raise ValueError("Bảng seed COCSOS bị trùng Run.")

    if num_runs is not None:
        expected_runs = set(range(1, int(num_runs) + 1))
        actual_runs = set(seed_table["Run"])
        missing_runs = expected_runs - actual_runs
        if missing_runs:
            raise ValueError(f"Bảng seed COCSOS thiếu Run: {sorted(missing_runs)}")
        seed_table = seed_table[seed_table["Run"].isin(expected_runs)].copy()

    return seed_table


def get_run_seed(seed_table, run):
    row = seed_table[seed_table["Run"].astype(int) == int(run)]
    if row.empty:
        raise ValueError(f"Không tìm thấy seed cho Run={run}")
    return validate_seed(row.iloc[0]["Seed"], run=run)


def array_to_excel_string(arr, precision=12):
    return np.array2string(np.asarray(arr), precision=precision, separator=", ", max_line_width=10_000)


def make_initial_population_df(initial_info, run, seed, dim):
    """Lưu quần thể random ban đầu dạng liên tục và OF tương ứng.

    OF được tính bởi objective_function, trong đó PS/mode mới được rời rạc hóa.
    """
    init_pop = np.asarray(initial_info["Initial Random Population"])
    init_of = np.asarray(initial_info["Initial Random OF"])

    coord_cols = [f"x{j + 1}" for j in range(dim)]
    df_init = pd.DataFrame(init_pop, columns=coord_cols)
    df_init.insert(0, "Initial Random OF", init_of)
    df_init.insert(0, "Individual", np.arange(1, len(init_pop) + 1))
    df_init.insert(0, "Seed", int(seed))
    df_init.insert(0, "Run", int(run))
    return df_init


def load_cocsos_initial_population_for_comparison(cocsos_run_excel, dim):
    """
    Đọc Initial_Random_Pop của COCSOS run tương ứng để kiểm tra SOS có tạo cùng đầu vào không.
    Nếu file không tồn tại, trả về None để code vẫn chạy bình thường.
    """
    if not cocsos_run_excel or not os.path.exists(cocsos_run_excel):
        return None

    df = pd.read_excel(cocsos_run_excel, sheet_name="Initial_Random_Pop")
    x_cols = [f"x{i + 1}" for i in range(dim)]
    required_cols = ["Initial Random OF"] + x_cols
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"File COCSOS Initial_Random_Pop thiếu cột: {missing}")

    return {
        "file": cocsos_run_excel,
        "population": df[x_cols].to_numpy(dtype=float),
        "of": df["Initial Random OF"].to_numpy(dtype=float),
    }


def make_initial_comparison_df(initial_info, cocsos_initial):
    """Tạo bảng so sánh Initial_Random_Pop và Initial Random OF giữa SOS và COCSOS."""
    sos_pop = np.asarray(initial_info["Initial Random Population"], dtype=float)
    sos_of = np.asarray(initial_info["Initial Random OF"], dtype=float)

    if cocsos_initial is None:
        return pd.DataFrame({
            "Metric": [
                "COCSOS initial file found",
                "Same Initial Population",
                "Same Initial OF",
                "Note",
            ],
            "Value": [
                False,
                "Not checked",
                "Not checked",
                "Không tìm thấy file COCSOS run tương ứng; SOS vẫn lưu Initial_Random_Pop để so sánh thủ công.",
            ],
        })

    coc_pop = np.asarray(cocsos_initial["population"], dtype=float)
    coc_of = np.asarray(cocsos_initial["of"], dtype=float)

    if coc_pop.shape != sos_pop.shape:
        same_pop = False
        max_pop_diff = f"Shape mismatch: SOS {sos_pop.shape}, COCSOS {coc_pop.shape}"
    else:
        max_pop_diff_val = float(np.max(np.abs(sos_pop - coc_pop))) if sos_pop.size else 0.0
        same_pop = bool(np.allclose(sos_pop, coc_pop, rtol=1e-12, atol=1e-12))
        max_pop_diff = max_pop_diff_val

    if coc_of.shape != sos_of.shape:
        same_of = False
        max_of_diff = f"Shape mismatch: SOS {sos_of.shape}, COCSOS {coc_of.shape}"
    else:
        max_of_diff_val = float(np.max(np.abs(sos_of - coc_of))) if sos_of.size else 0.0
        same_of = bool(np.allclose(sos_of, coc_of, rtol=1e-9, atol=1e-6))
        max_of_diff = max_of_diff_val

    return pd.DataFrame({
        "Metric": [
            "COCSOS initial file found",
            "COCSOS initial file",
            "Same Initial Population",
            "Max Abs Diff Initial Population",
            "Same Initial OF",
            "Max Abs Diff Initial OF",
            "SOS Initial Best OF",
            "COCSOS Initial Best OF",
            "Important note",
        ],
        "Value": [
            True,
            cocsos_initial["file"],
            same_pop,
            max_pop_diff,
            same_of,
            max_of_diff,
            float(np.min(sos_of)),
            float(np.min(coc_of)),
            "Nếu Same Initial Population và Same Initial OF đều TRUE, SOS và COCSOS có cùng đầu vào khởi tạo ngẫu nhiên.",
        ],
    })


# ------------------ Các hàm hỗ trợ SOS ------------------
def random_select(pop, i):
    candidates = [k for k in range(len(pop)) if k != i]
    return np.random.choice(candidates)


def build_bounds(bounds, dim):
    if dim != 3 * D:
        raise ValueError(f"dim phải bằng 3*D = {3 * D}, nhưng hiện là {dim}")
    D_local = dim // 3
    lb = np.concatenate((
        np.array([bounds[0]] * D_local),
        np.array([PS_LOWER_BOUND] * D_local),
        np.array([MODE_LOWER_BOUND] * D_local),
    ))
    ub = np.concatenate((
        np.array([bounds[1]] * D_local),
        np.array([PS_UPPER_BOUND] * D_local),
        np.array([MODE_UPPER_BOUND] * D_local),
    ))
    return lb, ub


def SOS(obj_func, bounds, dim, pop_size=100, max_iter=3000, seed=None, run=None):
    if seed is not None:
        seed = set_random_seed(seed, run=run)

    start_time = time.time()
    lb, ub = build_bounds(bounds, dim)

    # ==============================================================
    # 1) Quần thể random ban đầu - phải giống COCSOS nếu cùng seed.
    # ==============================================================
    pop_random_initial = np.random.uniform(lb, ub, (pop_size, dim))
    fitness_random_initial = np.array([obj_func(ind) for ind in pop_random_initial], dtype=float)

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

    pop = pop_random_initial.copy()
    fitness = fitness_random_initial.copy()

    best_idx = int(np.argmin(fitness))
    best_sol = pop[best_idx].copy()
    best_fit = float(fitness[best_idx])


    best_fitness_history = [initial_best_fit]
    history_stage = ["Initial Random Best OF before SOS update"]

    for iteration in range(1, max_iter + 1):
        for i in range(pop_size):
            best_idx = int(np.argmin(fitness))
            best_sol_current = pop[best_idx].copy()
            # Mutualism Phase
            j = random_select(pop, i)
            mutual = (pop[i] + pop[j]) / 2.0
            bf1, bf2 = np.random.randint(1, 3, size=2)

            r1_val = np.random.rand()
            new_ind1 = pop[i] + r1_val * (best_sol_current - bf1 * mutual)
            new_ind1 = np.clip(new_ind1, lb, ub)
   
            new_fit1 = obj_func(new_ind1)
            if new_fit1 < fitness[i]:
                pop[i] = new_ind1
                fitness[i] = new_fit1

            r2_val = np.random.rand()
            new_ind2 = pop[j] + r2_val * (best_sol_current - bf2 * mutual)
            new_ind2 = np.clip(new_ind2, lb, ub)

            new_fit2 = obj_func(new_ind2)
            if new_fit2 < fitness[j]:
                pop[j] = new_ind2
                fitness[j] = new_fit2

            # Commensalism Phase
            j = random_select(pop, i)
            r_vec = np.random.uniform(-1, 1, dim)
            new_ind = pop[i] + r_vec * (best_sol_current - pop[j])
            new_ind = np.clip(new_ind, lb, ub)

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

            parasite_fit = obj_func(parasite_vec)
            if parasite_fit < fitness[host_idx]:
                pop[host_idx] = parasite_vec
                fitness[host_idx] = parasite_fit

        best_idx_now = int(np.argmin(fitness))
        best_sol = pop[best_idx_now].copy()
        best_fit = float(fitness[best_idx_now])
        best_fitness_history.append(best_fit)
        history_stage.append("SOS iteration")

        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fit}")

    elapsed_time = time.time() - start_time
    print_detailed_results(best_sol, best_fit)
    print(f"Algorithm finished in {elapsed_time:.4f} seconds.")
    return best_sol, float(best_fit), elapsed_time, best_fitness_history, history_stage, initial_info


# ------------------ Xuất Excel ------------------
def export_results_to_excel(
    best_solution,
    best_fitness,
    elapsed_time,
    best_fitness_history,
    history_stage,
    initial_info,
    seed,
    run,
    filename="optimization_results.xlsx",
    pop_size=None,
    max_iter=None,
    seed_excel_source=None,
    cocsos_run_excel=None,
):
    dim = len(best_solution)

    df_fitness = pd.DataFrame({
        "Run": [int(run)] * len(best_fitness_history),
        "Seed": [int(seed)] * len(best_fitness_history),
        "Iteration": list(range(0, len(best_fitness_history))),
        "Stage": history_stage,
        "Best Fitness": best_fitness_history,
        "Elapsed Time (sec)": [elapsed_time] * len(best_fitness_history),
    })

    df_summary = pd.DataFrame({
        "Algorithm": ["SOS"],
        "Problem": ["Relay_TDS_PS_Mode_Optimization_3D"],
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Seed Excel Source": [seed_excel_source],
        "COCSOS Run Excel Compared": [cocsos_run_excel],
        "Dimension": [dim],
        "D_Relay": [D],
        "Pop Size": [pop_size],
        "Max Iter": [max_iter],
        "Initial Best Index": [initial_info["Initial Best Index"] + 1],
        "Initial Random Best OF": [initial_info["Initial Best OF"]],
        "Initial Best Individual": [array_to_excel_string(initial_info["Initial Best Individual"])],
        "Elapsed Time (sec)": [elapsed_time],
        "Best Fitness": [best_fitness],
        "Best Solution": [array_to_excel_string(best_solution)],
    })

    df_seed = pd.DataFrame({
        "Algorithm": ["SOS"],
        "Problem": ["Relay_TDS_PS_Mode_Optimization_3D"],
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Seed Source": ["Read from COCSOS Run_Seeds / Seed_Protocol Excel"],
        "Seed Excel Source": [seed_excel_source],
        "Random libraries reset": ["np.random.seed(seed) and random.seed(seed)"],
        "Reproducibility condition": [
            "Use the same Run seed, dim=3D, pop_size, bounds, objective_function, and relay data as COCSOS. PS/mode are discretized only inside objective_function/check_constraints."
        ],
    })

    df_initial_pop = make_initial_population_df(initial_info=initial_info, run=run, seed=seed, dim=dim)

    cocsos_initial = load_cocsos_initial_population_for_comparison(cocsos_run_excel, dim=dim)
    df_initial_comparison = make_initial_comparison_df(initial_info=initial_info, cocsos_initial=cocsos_initial)

    df_experiment = pd.DataFrame({
        "Item": [
            "Algorithm",
            "Problem",
            "Run",
            "Seed",
            "Seed Excel Source",
            "COCSOS run Excel for comparison",
            "Population size",
            "Maximum iterations",
            "TDS bounds",
            "PS bounds",
            "Mode bounds",
            "Mode mapping",
            "Relay count D",
            "Total dimension",
            "Seed protocol",
            "Initial population sheet",
            "Initial OF definition",
            "Fitness History iteration 0",
            "Random libraries reset",
            "Important fairness note",
        ],
        "Value": [
            "SOS",
            "Relay_TDS_PS_Mode_Optimization_3D",
            int(run),
            int(seed),
            seed_excel_source,
            cocsos_run_excel,
            pop_size,
            max_iter,
            str((TDS_LOWER_BOUND, TDS_UPPER_BOUND)),
            str((PS_LOWER_BOUND, PS_UPPER_BOUND)),
            str((MODE_LOWER_BOUND, MODE_UPPER_BOUND)),
            "0=NI, 1=VI, 2=EI",
            D,
            dim,
            "Each SOS Run reads and uses the same recorded seed as the corresponding COCSOS Run.",
            "Initial_Random_Pop",
            "Objective function value of each continuous initial random individual before SOS updates; PS/mode are discretized only during OF evaluation.",
            "Iteration 0 is Initial Random Best OF before any SOS update.",
            "np.random.seed(seed) and random.seed(seed)",
            "Initial_Random_Pop and Initial Random OF must match COCSOS if seed, bounds, dim, pop_size, objective_function, and data are identical. PS/mode are discretized only during OF evaluation.",
        ],
    })

    df_relays = get_relay_details_df(best_solution)
    df_backup = get_backup_coordination_df(best_solution)

    with pd.ExcelWriter(filename) as writer:
        df_summary.to_excel(writer, sheet_name="Summary", index=False)
        df_seed.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        df_experiment.to_excel(writer, sheet_name="Experiment_Info", index=False)
        df_initial_comparison.to_excel(writer, sheet_name="Initial_Comparison", index=False)
        df_initial_pop.to_excel(writer, sheet_name="Initial_Random_Pop", index=False)
        df_fitness.to_excel(writer, sheet_name="Fitness History", index=False)
        df_relays.to_excel(writer, sheet_name="Relay Details", index=False)
        df_backup.to_excel(writer, sheet_name="Backup Coordination", index=False)

    print(f"Results exported to {filename}")
    return df_summary.iloc[0].to_dict()


# ------------------ Chạy SOS nhiều lần, đọc seed từ Excel COCSOS và xuất Excel ------------------
if __name__ == "__main__":
    bounds = (TDS_LOWER_BOUND, TDS_UPPER_BOUND)
    pop_size = 50
    max_iter = 5000          
    dim = 3 * D           # TDS(D) + PS(D) + mode(D)
    num_runs = 2      # Đổi thành 30 hoặc 50 khi chạy chính thức

    sos_excel_filename_prefix = "SOS_15bus_TOF_newPS_mix_seed_protocol"

    # File tổng hợp COCSOS 3D đã xuất ra từ code COCSOS seed protocol.
    COCSOS_SEED_EXCEL = "COCSOS_15bus_TOF_newPS_mix_seed_protocol_ALL_SUMMARY.xlsx"
    COCSOS_RUN_FILE_PREFIX = "COCSOS_15bus_TOF_newPS_mix_seed_protocol_run"

    # 1) Đọc bảng seed từ COCSOS.
    seed_table = read_cocsos_seed_table(COCSOS_SEED_EXCEL, num_runs=num_runs)

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
            "Mode bounds",
            "Mode mapping",
            "Relay count D",
            "Total dimension",
            "Seed source",
            "Seed protocol",
            "Random libraries reset",
            "Initial population saved",
            "Initial OF saved",
            "Initial comparison saved",
            "Reproducibility condition",
        ],
        "Value": [
            "SOS",
            "Relay_TDS_PS_Mode_Optimization_3D",
            int(num_runs),
            int(pop_size),
            int(max_iter),
            str(bounds),
            str((PS_LOWER_BOUND, PS_UPPER_BOUND)),
            str((MODE_LOWER_BOUND, MODE_UPPER_BOUND)),
            "0=NI, 1=VI, 2=EI",
            D,
            dim,
            f"Read from COCSOS Excel file: {COCSOS_SEED_EXCEL}",
            "Each SOS Run uses the same recorded seed as the corresponding COCSOS Run.",
            "np.random.seed(seed) and random.seed(seed)",
            "Yes, sheet Initial_Random_Pop in each run file",
            "Yes, column Initial Random OF in sheet Initial_Random_Pop",
            "Yes, sheet Initial_Comparison if COCSOS run Excel exists",
            "Use the same Run seed, dim=3D, pop_size, bounds, objective_function, and relay data as COCSOS. PS/mode are discretized only inside objective_function/check_constraints.",
        ],
    })

    # 2) Chạy nhiều lần. Mỗi run lấy đúng seed tương ứng từ COCSOS.
    for run in range(1, int(num_runs) + 1):
        run_seed = get_run_seed(seed_table, run)
        cocsos_run_excel = f"{COCSOS_RUN_FILE_PREFIX}_{run}.xlsx"

        print(f"\n======== SOS 3D RUN {run} / {num_runs} | Seed from COCSOS = {run_seed} ========")
        best_solution, best_fitness, elapsed_time, history, history_stage, initial_info = SOS(
            objective_function,
            bounds,
            dim,
            pop_size=pop_size,
            max_iter=max_iter,
            seed=run_seed,
            run=run,
        )

        filename = f"{sos_excel_filename_prefix}_run_{run}.xlsx"
        summary_record = export_results_to_excel(
            best_solution=best_solution,
            best_fitness=best_fitness,
            elapsed_time=elapsed_time,
            best_fitness_history=history,
            history_stage=history_stage,
            initial_info=initial_info,
            seed=run_seed,
            run=run,
            filename=filename,
            pop_size=pop_size,
            max_iter=max_iter,
            seed_excel_source=COCSOS_SEED_EXCEL,
            cocsos_run_excel=cocsos_run_excel,
        )

        all_summary_records.append(summary_record)
        all_seed_records.append({
            "Algorithm": "SOS",
            "Problem": "Relay_TDS_PS_Mode_Optimization_3D",
            "Run": run,
            "Seed": int(run_seed),
            "Seed Source": "Read from COCSOS Run_Seeds / Seed_Protocol Excel",
            "Seed Excel Source": COCSOS_SEED_EXCEL,
            "COCSOS Run Excel Compared": cocsos_run_excel,
            "Pop Size": pop_size,
            "Max Iter": max_iter,
            "Dimension": dim,
        })

    # 3) Xuất file tổng hợp toàn bộ run của SOS.
    all_summary_df = pd.DataFrame(all_summary_records)
    all_seed_df = pd.DataFrame(all_seed_records)

    summary_filename = f"{sos_excel_filename_prefix}_ALL_SUMMARY.xlsx"
    with pd.ExcelWriter(summary_filename) as writer:
        all_summary_df.to_excel(writer, sheet_name="All_Summary", index=False)
        seed_table.to_excel(writer, sheet_name="COCSOS_Run_Seeds", index=False)
        all_seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

    print(f"\nSOS summary and seed protocol exported to {summary_filename}")
