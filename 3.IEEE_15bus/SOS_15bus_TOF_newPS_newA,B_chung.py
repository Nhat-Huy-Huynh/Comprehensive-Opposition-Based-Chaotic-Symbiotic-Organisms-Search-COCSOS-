import os
import time
import numpy as np
import random
import math
import pandas as pd

# ================================================================
# SOS 15-bus | bien tim kiem 2D+2: [TDS_1..TDS_D, PS_1..PS_D, A, B]
# =====
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



# ------------------ Thiet lap bien tim kiem: phai khop voi COCSOS ------------------
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
    """Tao vector lb/ub cho nghiem [TDS_1..TDS_D, PS_1..PS_D, A, B]."""
    expected_dim = 2 * D + 2
    if int(dim) != expected_dim:
        raise ValueError(f"dim phai bang 2*D+2 = {expected_dim}, nhung hien la {dim}")

    lb_TDS = np.array([bounds[0]] * D)
    ub_TDS = np.array([bounds[1]] * D)
    lb_PS = np.array([PS_LOWER_BOUND] * D)
    ub_PS = np.array([PS_UPPER_BOUND] * D)
    lb_extra = np.array([A_LOWER_BOUND, B_LOWER_BOUND])
    ub_extra = np.array([A_UPPER_BOUND, B_UPPER_BOUND])
    lb = np.concatenate((lb_TDS, lb_PS, lb_extra))
    ub = np.concatenate((ub_TDS, ub_PS, ub_extra))
    return lb, ub


# ------------------ Ham tinh thoi gian va ham muc tieu ------------------
def time_operation(TDS, Ipickup, I, A, B):
    ratio = I / Ipickup
    return TDS * (A / (ratio ** B - 1))


def get_backup_current(primary_idx, count):
    backup_data = I_data_backup[primary_idx]
    if isinstance(backup_data, list):
        return backup_data[count % len(backup_data)] if backup_data else None
    return backup_data


def check_constraints(x) -> float:
    # Dong bo voi ban COCSOS 2D+2 da tao seed protocol truoc do.
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


# ------------------ Roi rac hoa nghiem: phai khop voi COCSOS ------------------
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


# ------------------ Seed protocol ------------------
def validate_seed(seed, run=None):
    """Dam bao seed hop le cho np.random.seed va random.seed."""
    try:
        seed = int(seed)
    except Exception as exc:
        raise ValueError(f"Seed khong chuyen duoc sang int: {seed!r} | Run={run}") from exc

    max_seed = int(np.iinfo(np.uint32).max)
    if seed < 0 or seed > max_seed:
        raise ValueError(
            f"Seed khong hop le: {seed} | Run={run}. Seed phai nam trong khoang 0 den {max_seed}."
        )
    return seed


def set_random_seed(seed, run=None):
    seed = validate_seed(seed, run=run)
    np.random.seed(seed)
    random.seed(seed)
    return seed


def read_cocsos_seed_table(cocsos_seed_excel, num_runs=None):
    """
    Doc bang seed tu file ALL_SUMMARY cua COCSOS.
    Uu tien sheet Run_Seeds, neu khong co thi doc Seed_Protocol.
    """
    if not os.path.exists(cocsos_seed_excel):
        raise FileNotFoundError(
            f"Khong tim thay file seed Excel cua COCSOS: {cocsos_seed_excel}\n"
            "Hay dat file nay cung thu muc voi code SOS hoac sua bien COCSOS_SEED_EXCEL."
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
        raise ValueError(f"File seed COCSOS thieu cac cot: {missing}. Sheet doc duoc: {seed_sheet}")

    seed_table = seed_table.copy()
    seed_table["Run"] = seed_table["Run"].astype(int)
    seed_table["Seed"] = seed_table.apply(
        lambda row: validate_seed(row["Seed"], run=row["Run"]), axis=1
    ).astype(int)
    seed_table = seed_table.sort_values("Run").reset_index(drop=True)

    if seed_table.duplicated(subset=["Run"]).any():
        raise ValueError("Bang seed COCSOS bi trung Run.")

    if num_runs is not None:
        expected_runs = set(range(1, int(num_runs) + 1))
        actual_runs = set(seed_table["Run"])
        missing_runs = expected_runs - actual_runs
        if missing_runs:
            raise ValueError(f"Bang seed COCSOS thieu Run: {sorted(missing_runs)}")
        seed_table = seed_table[seed_table["Run"].isin(expected_runs)].copy()

    return seed_table


def get_run_seed(seed_table, run):
    row = seed_table[seed_table["Run"].astype(int) == int(run)]
    if row.empty:
        raise ValueError(f"Khong tim thay seed cho Run={run}")
    return validate_seed(row.iloc[0]["Seed"], run=run)


def array_to_excel_string(arr, precision=12):
    return np.array2string(
        np.asarray(arr),
        precision=precision,
        separator=", ",
        max_line_width=10_000,
    )


def make_initial_population_df(initial_info, run, seed, dim):
    init_pop = initial_info["Initial Random Population"]
    init_of = initial_info["Initial Random OF"]
    coord_cols = [f"x{j + 1}" for j in range(dim)]
    df_init = pd.DataFrame(init_pop, columns=coord_cols)
    df_init.insert(0, "Initial Random OF", init_of)
    df_init.insert(0, "Individual", np.arange(1, len(init_pop) + 1))
    df_init.insert(0, "Seed", int(seed))
    df_init.insert(0, "Run", int(run))
    return df_init


def compare_with_cocsos_initial(df_sos_initial, run, cocsos_run_file, tol=1e-5):
    """
    Neu co file run cua COCSOS, doc sheet Initial_Random_Pop de kiem tra:
    - Quần thể khởi tạo SOS và COCSOS có giống nhau không.
    - Initial Random OF của SOS và COCSOS có giống nhau không.
    """
    if not cocsos_run_file or not os.path.exists(cocsos_run_file):
        return pd.DataFrame({
            "Run": [int(run)],
            "COCSOS Run File": [cocsos_run_file],
            "Comparison Status": ["COCSOS run file not found - skipped"],
            "Same Initial Population": [None],
            "Max Abs Diff Population": [None],
            "Same Initial OF": [None],
            "Max Abs Diff Initial OF": [None],
        })

    try:
        df_coc = pd.read_excel(cocsos_run_file, sheet_name="Initial_Random_Pop")
    except Exception as exc:
        return pd.DataFrame({
            "Run": [int(run)],
            "COCSOS Run File": [cocsos_run_file],
            "Comparison Status": [f"Cannot read Initial_Random_Pop: {exc}"],
            "Same Initial Population": [None],
            "Max Abs Diff Population": [None],
            "Same Initial OF": [None],
            "Max Abs Diff Initial OF": [None],
        })

    x_cols = [c for c in df_sos_initial.columns if str(c).startswith("x")]
    common_x_cols = [c for c in x_cols if c in df_coc.columns]

    if len(common_x_cols) != len(x_cols) or len(df_coc) != len(df_sos_initial):
        return pd.DataFrame({
            "Run": [int(run)],
            "COCSOS Run File": [cocsos_run_file],
            "Comparison Status": ["Different row count or variable columns"],
            "Same Initial Population": [False],
            "Max Abs Diff Population": [None],
            "Same Initial OF": [False],
            "Max Abs Diff Initial OF": [None],
        })

    sos_pop = df_sos_initial[common_x_cols].to_numpy(dtype=float)
    coc_pop = df_coc[common_x_cols].to_numpy(dtype=float)
    pop_diff = float(np.nanmax(np.abs(sos_pop - coc_pop)))

    sos_of = df_sos_initial["Initial Random OF"].to_numpy(dtype=float)
    coc_of = df_coc["Initial Random OF"].to_numpy(dtype=float)
    of_diff = float(np.nanmax(np.abs(sos_of - coc_of)))

    return pd.DataFrame({
        "Run": [int(run)],
        "COCSOS Run File": [cocsos_run_file],
        "Comparison Status": ["Compared"],
        "Same Initial Population": [bool(pop_diff <= tol)],
        "Max Abs Diff Population": [pop_diff],
        "Same Initial OF": [bool(of_diff <= tol)],
        "Max Abs Diff Initial OF": [of_diff],
        "Tolerance": [tol],
    })


# ------------------ SOS algorithm co seed protocol ------------------
def random_select(pop, i):
    candidates = [k for k in range(len(pop)) if k != i]
    return np.random.choice(candidates)


def SOS(obj_func, bounds, dim, pop_size=50, max_iter=5000, seed=None, run=None):
    """
    SOS doc seed tu COCSOS:
    - Reset np.random va random truoc khi tao quan the.
    - Tao pop_random_initial bang dung lb/ub, dim, pop_size, quantize_solution nhu COCSOS.
    - Luu Initial Random Population va Initial Random OF.
    - best_fitness_history[0] la Initial Random Best OF sau khi tao quan the.
    """
    if seed is not None:
        seed = set_random_seed(seed, run=run)

    start_time = time.time()
    lb, ub = build_bounds_vector(bounds, dim)

    # ==============================================================
    # 1) Khởi tạo quần thể ngẫu nhiên ban đầu 
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

    # SOS goc bat dau truc tiep tu quan the random ban dau, khong co buoc CO.
    pop = pop_random_initial.copy()
    fitness = fitness_random_initial.copy()

    best_idx = int(np.argmin(fitness))
    best_sol = pop[best_idx].copy()
    best_fit = float(fitness[best_idx])

    # Iteration 0 = Best OF sau khi tao quan the ngau nhien ban dau.
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

        best_idx_now = int(np.argmin(fitness))
        best_sol = pop[best_idx_now].copy()
        best_fit = float(fitness[best_idx_now])
        best_fitness_history.append(best_fit)
        history_stage.append("SOS iteration best")

        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fit}")

    elapsed_time = time.time() - start_time
    print_detailed_results(best_sol, best_fit)
    print(f"Algorithm finished in {elapsed_time:.4f} seconds.")
    return best_sol, best_fit, elapsed_time, best_fitness_history, history_stage, initial_info


# ------------------ In chi tiet ket qua ------------------
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
    print(f"\nA = {A:.6f}, B = {B:.6f}")
    print(f"\nBest fitness: {best_fitness:.10f}")

    print("\nOperation times for each relay:")
    primary_times = [
        time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B)
        for i in range(D)
    ]
    for i, t in enumerate(primary_times):
        print(f"Relay {i + 1}: {t:.6f} sec")

    print("\nChecking coordination for backup pairs:")
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
        if coordination_time >= CTI:
            print(f"Backup relay {backup_idx + 1} coordinated with primary relay {primary_idx + 1}: Success")
        else:
            print(f"Backup relay {backup_idx + 1} failed with primary relay {primary_idx + 1}: Failure")


# ------------------ Xuat Excel ------------------
def build_relay_details_df(best_solution):
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2 * D]
    A = best_solution[2 * D]
    B = best_solution[2 * D + 1]
    relay_data = []
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        op_time = time_operation(TDS_values[i], I_pickup, I_data[i], A, B)
        relay_data.append({
            "Relay": i + 1,
            "TDS": TDS_values[i],
            "PS": PS_values[i],
            "A": A,
            "B": B,
            "I_pickup": I_pickup,
            "Operation Time": op_time,
        })
    return pd.DataFrame(relay_data)


def build_backup_coordination_df(best_solution):
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2 * D]
    A = best_solution[2 * D]
    B = best_solution[2 * D + 1]
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
        backup_records.append({
            "Primary Relay": primary_idx + 1,
            "Backup Relay": backup_idx + 1,
            "Backup Current Used": backup_current,
            "Primary Operation Time": primary_time,
            "Backup Operation Time": backup_time,
            "Coordination Time": coordination_time,
            "CTI": CTI,
            "Status": "Success" if coordination_time >= CTI else "Failure",
        })
    return pd.DataFrame(backup_records)


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
    cocsos_run_file=None,
):
    dim = len(best_solution)
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2 * D]
    A = best_solution[2 * D]
    B = best_solution[2 * D + 1]

    df_fitness = pd.DataFrame({
        "Iteration": list(range(0, len(best_fitness_history))),
        "Stage": history_stage,
        "Best Fitness": best_fitness_history,
        "Elapsed Time Run (sec)": elapsed_time,
        "Run": int(run),
        "Seed": int(seed),
    })

    df_initial_pop = make_initial_population_df(initial_info, run, seed, dim)
    df_initial_compare = compare_with_cocsos_initial(df_initial_pop, run, cocsos_run_file)

    df_init_summary = pd.DataFrame({
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Initial Random Best Index": [initial_info["Initial Best Index"] + 1],
        "Initial Random Best OF": [initial_info["Initial Best OF"]],
        "Initial Random Best Individual": [array_to_excel_string(initial_info["Initial Best Individual"])],
    })

    df_summary = pd.DataFrame({
        "Algorithm": ["SOS"],
        "Problem": ["Relay_TDS_PS_AB_Optimization_15bus"],
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Seed Excel Source": [seed_excel_source],
        "Dimension": [dim],
        "D_Relay": [D],
        "Pop Size": [pop_size],
        "Max Iter": [max_iter],
        "Initial Random Best Index": [initial_info["Initial Best Index"] + 1],
        "Initial Random Best OF": [initial_info["Initial Best OF"]],
        "Initial Random Best Individual": [array_to_excel_string(initial_info["Initial Best Individual"])],
        "Elapsed Time (sec)": [elapsed_time],
        "Best Fitness": [best_fitness],
        "Best Solution": [array_to_excel_string(best_solution)],
        "Best A": [A],
        "Best B": [B],
    })

    df_seed = pd.DataFrame({
        "Algorithm": ["SOS"],
        "Problem": ["Relay_TDS_PS_AB_Optimization_15bus"],
        "Run": [int(run)],
        "Seed": [int(seed)],
        "Seed Source": ["Read from COCSOS Run_Seeds / Seed_Protocol Excel"],
        "Seed Excel Source": [seed_excel_source],
        "Random libraries reset": ["np.random.seed(seed) and random.seed(seed)"],
        "Reproducibility condition": [
            "Use same Run seed, TDS/PS/A/B bounds, dim=2D+2, pop_size, quantize_solution, objective_function, and relay data as COCSOS."
        ],
    })

    df_experiment = pd.DataFrame({
        "Item": [
            "Algorithm",
            "Problem",
            "Run",
            "Seed",
            "Seed Excel Source",
            "COCSOS Run File For Initial Check",
            "Population size",
            "Maximum iterations",
            "TDS bounds",
            "PS bounds",
            "A bounds",
            "B bounds",
            "PS rounding digits",
            "Relay count D",
            "Total dimension",
            "Variable order",
            "Seed protocol",
            "Initial population saved",
            "Initial OF saved",
            "Fitness History iteration 0",
            "Random libraries reset",
            "Important fairness note",
        ],
        "Value": [
            "SOS",
            "Relay_TDS_PS_AB_Optimization_15bus",
            int(run),
            int(seed),
            seed_excel_source,
            cocsos_run_file,
            pop_size,
            max_iter,
            str((TDS_LOWER_BOUND, TDS_UPPER_BOUND)),
            str((PS_LOWER_BOUND, PS_UPPER_BOUND)),
            str((A_LOWER_BOUND, A_UPPER_BOUND)),
            str((B_LOWER_BOUND, B_UPPER_BOUND)),
            PS_ROUND_DIGITS,
            D,
            dim,
            "[TDS_1..TDS_D, PS_1..PS_D, A, B]",
            "Each SOS Run reads and uses the same seed recorded for the corresponding COCSOS Run.",
            "Yes, sheet Initial_Random_Pop",
            "Yes, column Initial Random OF in sheet Initial_Random_Pop",
            "Iteration 0 = Initial Random Best OF before SOS updates",
            "np.random.seed(seed) and random.seed(seed)",
            "Initial Random Population and Initial Random OF match COCSOS only if bounds, quantize_solution and objective_function are identical.",
        ],
    })

    df_relays = build_relay_details_df(best_solution)
    df_backup = build_backup_coordination_df(best_solution)

    with pd.ExcelWriter(filename) as writer:
        df_summary.to_excel(writer, sheet_name="Summary", index=False)
        df_seed.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        df_experiment.to_excel(writer, sheet_name="Experiment_Info", index=False)
        df_init_summary.to_excel(writer, sheet_name="Initialization_Summary", index=False)
        df_initial_pop.to_excel(writer, sheet_name="Initial_Random_Pop", index=False)
        df_initial_compare.to_excel(writer, sheet_name="Initial_Comparison", index=False)
        df_fitness.to_excel(writer, sheet_name="Fitness History", index=False)
        df_relays.to_excel(writer, sheet_name="Relay Details", index=False)
        df_backup.to_excel(writer, sheet_name="Backup Coordination", index=False)

    print(f"Results exported to {filename}")
    return df_summary.iloc[0].to_dict(), df_seed.iloc[0].to_dict(), df_initial_compare.iloc[0].to_dict()


# ------------------ Main: doc seed COCSOS va chay SOS ------------------
if __name__ == "__main__":
    bounds = (TDS_LOWER_BOUND, TDS_UPPER_BOUND)
    pop_size = 50
    max_iter = 5000       # doi thanh so vong lap chinh thuc khi chay that
    total_dim = 2 * D + 2
    num_runs = 15     

    sos_excel_filename_prefix = "SOS_15bus_TOF_newPS_AB_chung_seed_protocol"

    # File seed do COCSOS 2D+2 da xuat ra.
    COCSOS_SEED_EXCEL = "COCSOS_15bus_TOF_newPS_AB_chung_seed_protocol_ALL_SUMMARY.xlsx"
    COCSOS_RUN_FILE_PREFIX = "COCSOS_15bus_TOF_newPS_AB_chung_seed_protocol_run_"

    seed_table = read_cocsos_seed_table(COCSOS_SEED_EXCEL, num_runs=num_runs)

    all_summary_records = []
    all_seed_records = []
    all_compare_records = []

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
            "PS rounding digits",
            "Relay count D",
            "Total dimension",
            "Variable order",
            "Seed source",
            "Seed protocol",
            "Random libraries reset",
            "Initial population saved",
            "Initial OF saved",
            "Fitness History iteration 0",
            "Reproducibility condition",
        ],
        "Value": [
            "SOS",
            "Relay_TDS_PS_AB_Optimization_15bus",
            int(num_runs),
            int(pop_size),
            int(max_iter),
            str(bounds),
            str((PS_LOWER_BOUND, PS_UPPER_BOUND)),
            str((A_LOWER_BOUND, A_UPPER_BOUND)),
            str((B_LOWER_BOUND, B_UPPER_BOUND)),
            PS_ROUND_DIGITS,
            D,
            total_dim,
            "[TDS_1..TDS_D, PS_1..PS_D, A, B]",
            f"Read from COCSOS Excel file: {COCSOS_SEED_EXCEL}",
            "Each SOS Run uses the same recorded seed as the corresponding COCSOS Run.",
            "np.random.seed(seed) and random.seed(seed)",
            "Yes, sheet Initial_Random_Pop in each run file",
            "Yes, column Initial Random OF in sheet Initial_Random_Pop",
            "Iteration 0 = Initial Random Best OF before SOS updates",
            "Use same Run seed, bounds, dim=2D+2, pop_size, objective_function, and quantize_solution as COCSOS.",
        ],
    })

    for run in range(1, int(num_runs) + 1):
        run_seed = get_run_seed(seed_table, run)
        cocsos_run_file = f"{COCSOS_RUN_FILE_PREFIX}{run}.xlsx"

        print(f"\n======== SOS RUN {run} / {num_runs} | Seed from COCSOS = {run_seed} ========")
        best_solution, best_fitness, elapsed_time, history, history_stage, initial_info = SOS(
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
        print(f"A = {best_solution[2 * D]:.6f}, B = {best_solution[2 * D + 1]:.6f}")
        print(f"Initial Random Best OF: {initial_info['Initial Best OF']:.10f}")
        print(f"Best fitness: {best_fitness:.10f}")
        print(f"Elapsed time: {elapsed_time:.4f} sec")

        filename = f"{sos_excel_filename_prefix}_run_{run}.xlsx"
        summary_record, seed_record, compare_record = export_results_to_excel(
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
            cocsos_run_file=cocsos_run_file,
        )

        all_summary_records.append(summary_record)
        all_seed_records.append(seed_record)
        all_compare_records.append(compare_record)

    all_summary_df = pd.DataFrame(all_summary_records)
    all_seed_df = pd.DataFrame(all_seed_records)
    all_compare_df = pd.DataFrame(all_compare_records)

    summary_filename = f"{sos_excel_filename_prefix}_ALL_SUMMARY.xlsx"
    with pd.ExcelWriter(summary_filename) as writer:
        all_summary_df.to_excel(writer, sheet_name="All_Summary", index=False)
        seed_table.to_excel(writer, sheet_name="COCSOS_Run_Seeds", index=False)
        all_seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        all_compare_df.to_excel(writer, sheet_name="Initial_Comparison", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

    print(f"\nSOS summary and seed protocol exported to {summary_filename}")
