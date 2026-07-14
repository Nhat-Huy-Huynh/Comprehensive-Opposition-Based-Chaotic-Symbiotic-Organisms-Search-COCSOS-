import numpy as np
import pandas as pd
import time
import sys
import random
import matplotlib.pyplot as plt
from scipy.stats import qmc
import math
_rng = np.random.default_rng()
# ----- Hàm random_select -----
def random_select(pop, i):
    candidates = [k for k in range(len(pop)) if k != i]
    return np.random.choice(candidates)

# ----- Comprehensive Opposition (CO) Population -----
def co_population(pop, lb, ub, iteration, max_iter):
    pop_size, dim = pop.shape
    lb = np.array(lb)
    ub = np.array(ub)
    c = (lb + ub) / 2  # trung tâm của miền tìm kiếm
    new_pop = np.zeros_like(pop)
    
    # Tính tỉ lệ tiến triển
    ratio = iteration / max_iter

    if 0 <= ratio <= 0.224:  # Giai đoạn ban đầu: ưu tiên khám phá (QO cao)
        P_reo = 0.01
        P_qr  = 0.01
        P_qo  = 0.54 + 1.92 * ratio
    elif ratio > 0.723:      # Giai đoạn cuối: ưu tiên khai thác (QR cao)
        P_reo = 0.01
        P_qr  = 0.97
        P_qo  = 0.01
    else:                    
        P_reo = 0.01
        P_qr  = -0.42 + 1.92 * ratio
        P_qo  = 1.4 - 1.92 * ratio
    P_eo = 1 - (P_reo + P_qr + P_qo)

    # Duyệt qua từng cá thể trong quần thể
    for i in range(pop_size):
        x = pop[i]
        x_op = lb + ub - x  # Basic Opposite

        chosen = np.zeros(dim)
        # Sinh ngẫu nhiên và chọn chiến lược cho từng dimension
        for j in range(dim):
            r = random.random()
            if r < P_reo:
                # REO (Reflected Extended Opposition)
                if x[j] < c[j]:
                    x_eo = random.uniform(x_op[j], ub[j])
                else:
                    x_eo = random.uniform(lb[j], x_op[j])
                chosen[j] = lb[j] + ub[j] - x_eo

            elif r < P_reo + P_qr:
                # QR (Quasi-Reflection)
                if x[j] < c[j]:
                    chosen[j] = random.uniform(x[j], c[j])
                else:
                    chosen[j] = random.uniform(c[j], x[j])

            elif r < P_reo + P_qr + P_qo:
                # QO (Quasi-Opposition)
                if x[j] < c[j]:
                    chosen[j] = random.uniform(c[j], x_op[j])
                else:
                    chosen[j] = random.uniform(x_op[j], c[j])

            else:
                # EO (Extended Opposition)
                if x[j] < c[j]:
                    chosen[j] = random.uniform(x_op[j], ub[j])
                else:
                    chosen[j] = random.uniform(lb[j], x_op[j])

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
        x = r * x * (1 - x)
        chaotic_factor = x - 0.5
        i, j = np.random.choice(pop_size, size=2, replace=False)
        xi = pop[i]
        xj = pop[j]
        perturb = chaotic_factor * (xi - xj)
        new_sol = candidate + perturb
        new_sol = np.clip(new_sol, lb_vec, ub_vec)

        new_fit = obj_func(new_sol)
        if new_fit < candidate_fit:
            candidate, candidate_fit = new_sol.copy(), new_fit

    return candidate, candidate_fit

# ------ Các hàm hỗ trợ seed và xuất Excel ------
def validate_seed(seed, run=None, function_name=None):
    """Kiểm tra seed hợp lệ trong khoảng uint32 để tránh lỗi khi reset random."""
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
    """Reset đồng thời numpy random và random chuẩn của Python."""
    seed = validate_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    return seed


def make_function_seed_table(num_runs=50, function_names=None):
    """
    Sinh bảng seed cho CEC2017 theo từng cặp Run + Function.

    - Mỗi Run + Function có đúng 1 seed riêng.
    - Seed nằm trong [0, 2**32 - 1].
    - Bảng này được lưu ra Excel để SOS/thuật toán khác đọc lại.
    """
    if function_names is None:
        raise ValueError("function_names không được để trống khi sinh seed cho CEC2017.")

    rng = np.random.default_rng()
    total = int(num_runs) * len(function_names)
    seeds = []
    used = set()

    # Dùng safe_max_seed giống file chuẩn để tránh seed âm/lỗi khi chuyển kiểu ở Excel.
    safe_max_seed = 2**31 - 1
    while len(seeds) < total:
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
    """Kiểm tra bảng seed đủ cặp Run + Function và seed hợp lệ."""
    required_cols = {"Run", "Function", "Seed"}
    missing = required_cols - set(seed_table.columns)
    if missing:
        raise ValueError(f"seed_table thiếu các cột: {missing}")

    seed_table = seed_table.copy()
    seed_table["Run"] = seed_table["Run"].astype(int)
    seed_table["Function"] = seed_table["Function"].astype(str)
    seed_table["Seed"] = seed_table.apply(
        lambda row: validate_seed(row["Seed"], row["Run"], row["Function"]), axis=1
    ).astype(int)

    expected_rows = int(num_runs) * len(function_names)
    if len(seed_table) != expected_rows:
        raise ValueError(
            f"seed_table phải có {expected_rows} dòng = num_runs * số_function, "
            f"nhưng hiện có {len(seed_table)} dòng."
        )

    expected_pairs = {
        (run, str(fn))
        for run in range(1, int(num_runs) + 1)
        for fn in function_names
    }
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
    """Lấy seed đúng với Run + Function."""
    row = seed_table[
        (seed_table["Run"].astype(int) == int(run)) &
        (seed_table["Function"].astype(str) == str(function_name))
    ]
    if row.empty:
        raise ValueError(f"Không tìm thấy seed cho Run={run}, Function={function_name}")
    return validate_seed(row.iloc[0]["Seed"], run, function_name)


def array_to_excel_string(arr, precision=12):
    """Chuyển vector nghiệm sang chuỗi gọn để ghi vào Excel."""
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


def build_experiment_info_df(num_runs, pop_size, max_iter):
    """Thông tin mô tả seed protocol để lưu kèm Excel."""
    return pd.DataFrame({
        "Item": [
            "Algorithm",
            "Benchmark set",
            "Number of independent runs",
            "Population size",
            "Maximum iterations",
            "Seed source",
            "Seed protocol",
            "Random libraries reset",
            "Initial population record",
            "Reproducibility condition"
        ],
        "Value": [
            "COCSOS",
            "CEC2017",
            int(num_runs),
            int(pop_size),
            int(max_iter),
            "Generated once by COCSOS-CEC2017 and saved to sheet Function_Seeds",
            "Each Run + Function pair uses one recorded seed.",
            "np.random.seed(seed) and random.seed(seed)",
            "Initial random population and Initial Random OF are saved before applying co_population().",
            "Other algorithms must read the same Function_Seeds sheet and use the same Function + Run seed, bounds, dimension, population size, and initial random generation formula."
        ]
    })


# --------------------------- 3) Thuật toán SOS_AFDB ---------------------------
def COCSOS(obj_func, bounds, dim, pop_size=50, max_iter=1000, seed=None):
    """
    COCSOS gốc được giữ nguyên cơ chế thuật toán.

    Phần bổ sung duy nhất:
    - Nhận thêm seed để reset np.random và random.
    - Lưu quần thể ngẫu nhiên ban đầu và OF ban đầu trước khi áp dụng CO.
    """
    if seed is not None:
        set_random_seed(seed)

    start_time = time.time()
    lb = np.array([bounds[0]] * dim)
    ub = np.array([bounds[1]] * dim)
    best_fitness_history = []

    # ==============================================================
    # 1) Khởi tạo dân số ngẫu nhiên ban đầu và lưu lại để tái lập
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
    # 2) Thuật toán gốc tiếp tục dùng quần thể ban đầu này để tạo CO population
    # ==============================================================
    pop = co_population(pop_random_initial.copy(), lb, ub, iteration=0, max_iter=max_iter)
    fitness = np.array([obj_func(ind) for ind in pop])

    best_idx = np.argmin(fitness)
    best_sol = pop[best_idx].copy()
    best_fit = fitness[best_idx]

    # Lưu giá trị tốt nhất ngay sau khởi tạo ngẫu nhiên ban đầu.
    best_fitness_history = [initial_best_fit]
    
    for iteration in range(1, max_iter+1):
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
            host_idx = random_select(pop, i)
            parasite_vec = pop[i].copy()
            n_changes = int(np.ceil(np.random.rand()*dim))
            pick_dims = np.random.choice(dim, size=n_changes, replace=False)
            for d in pick_dims:
                    parasite_vec[d] = np.random.uniform(lb[d], ub[d])
            parasite_vec = np.clip(parasite_vec,lb,ub)
            parasite_fit = obj_func(parasite_vec)
            if parasite_fit < fitness[host_idx]:
                pop[host_idx] = parasite_vec
                fitness[host_idx] = parasite_fit

        # ===== Opposition Phase using Comprehensive Opposition (CO) =====
        if np.random.rand() < 0.4:
            co_pop2 = co_population(pop, lb, ub,iteration,max_iter)
            combined = np.vstack((pop, co_pop2))
            fitness_combined = np.array([obj_func(ind) for ind in combined])
            best_indices = np.argsort(fitness_combined)[:pop_size]
            pop = combined[best_indices]
            fitness = fitness_combined[best_indices]

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
    print(f"Algorithm finished in {elapsed_time:.4f} seconds.")
    return best_sol, best_fit, elapsed_time, best_fitness_history, initial_info


# --------------------------- 4) Chạy thuật toán trên tất cả các hàm benchmark ---------------------------
def run_qocsos_for_all(
    functions,
    run_index,
    seed_table,
    pop_size=50,
    max_iter=1000,
    excel_filename_prefix="COCSOS_CEC2017_F1-F30_30dim",
    experiment_info_df=None,
):
    results = []
    history_dict = {}
    initial_infos = {}
    seed_records_this_run = []

    for name, (func, bound, global_min, dim) in functions.items():
        function_seed = get_function_seed(seed_table, run_index, name)
        print(f"Running Function: {name} (Run {run_index}) | Seed = {function_seed}")

        best_sol, best_val, elapsed_time, best_history, initial_info = COCSOS(
            obj_func=func,
            bounds=bound,
            dim=dim,
            pop_size=pop_size,
            max_iter=max_iter,
            seed=function_seed,
        )

        results.append({
            "Algorithm": "COCSOS",
            "Run": run_index,
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
            "Running Time (s)": elapsed_time
        })

        seed_records_this_run.append({
            "Algorithm": "COCSOS",
            "Run": run_index,
            "Function": name,
            "Seed": function_seed,
            "Seed Source": "Generated by COCSOS-CEC2017",
            "Dimension": dim,
            "Bounds": str(bound),
            "Pop Size": pop_size,
            "Max Iter": max_iter,
        })

        history_dict[name] = best_history
        initial_infos[name] = initial_info

    summary_df = pd.DataFrame(results)
    if not summary_df.empty:
        summary_df["Initial Best Individual"] = summary_df["Initial Best Individual"].apply(array_to_excel_string)
        summary_df["Best Solution"] = summary_df["Best Solution"].apply(array_to_excel_string)

    seed_df = pd.DataFrame(seed_records_this_run)
    excel_filename = f"{excel_filename_prefix}_{run_index}.xlsx"

    with pd.ExcelWriter(excel_filename) as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        if experiment_info_df is not None:
            experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

        # Lưu quần thể khởi tạo ngẫu nhiên và OF ban đầu của từng function.
        for func_name, initial_info in initial_infos.items():
            init_pop = initial_info["Initial Random Population"]
            init_of = initial_info["Initial Random OF"]

            coord_cols = [f"x{j + 1}" for j in range(init_pop.shape[1])]
            df_init = pd.DataFrame(init_pop, columns=coord_cols)
            df_init.insert(0, "Initial Random OF", init_of)
            df_init.insert(0, "Individual", np.arange(1, len(init_pop) + 1))
            df_init.insert(0, "Function", func_name)
            df_init.insert(0, "Seed", initial_info["Seed"])
            df_init.insert(0, "Run", run_index)

            sheet_name = safe_sheet_name(func_name, suffix="_InitOF")
            df_init.to_excel(writer, sheet_name=sheet_name, index=False)

        # Lưu lịch sử hội tụ. Iteration 0 là trạng thái sau khởi tạo ngẫu nhiên ban đầu.
        for func_name, best_fitness_history in history_dict.items():
            pd.DataFrame({
                "Iteration": np.arange(0, len(best_fitness_history)),
                "Best Fitness": best_fitness_history
            }).to_excel(writer, sheet_name=safe_sheet_name(func_name), index=False)

    print(f"Results of run {run_index} have been exported to {excel_filename}")
    return summary_df, seed_df


def run_multiple_times(
    functions,
    n_runs=50,
    pop_size=50,
    max_iter=1000,
    excel_filename_prefix="COCSOS_CEC2017_F21-F30_100dim",
):
    function_names = list(functions.keys())

    # COCSOS chạy trước nên tự sinh seed và lưu lại cho các thuật toán khác dùng.
    seed_table = make_function_seed_table(num_runs=n_runs, function_names=function_names)
    seed_table = check_seed_table(seed_table, num_runs=n_runs, function_names=function_names)
    experiment_info_df = build_experiment_info_df(n_runs, pop_size, max_iter)

    all_summary_records = []
    all_seed_records = []

    for run_i in range(1, n_runs + 1):
        print(f"\n--- Starting run {run_i} ---")
        summary_df, seed_df = run_qocsos_for_all(
            functions,
            run_i,
            seed_table=seed_table,
            pop_size=pop_size,
            max_iter=max_iter,
            excel_filename_prefix=excel_filename_prefix,
            experiment_info_df=experiment_info_df,
        )
        all_summary_records.extend(summary_df.to_dict("records"))
        all_seed_records.extend(seed_df.to_dict("records"))

    all_summary_df = pd.DataFrame(all_summary_records)
    all_seed_df = pd.DataFrame(all_seed_records)
    function_seed_df = seed_table.copy()
    function_seed_df["Seed Source"] = "Generated by COCSOS-CEC2017"

    all_file_name = f"{excel_filename_prefix}_ALL_SUMMARY.xlsx"
    with pd.ExcelWriter(all_file_name) as writer:
        all_summary_df.to_excel(writer, sheet_name="All_Summary", index=False)
        all_seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        function_seed_df.to_excel(writer, sheet_name="Function_Seeds", index=False)
        function_seed_df.to_excel(writer, sheet_name="Run_Function_Seeds", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

    print(f"All {n_runs} runs completed.")
    print(f"All COCSOS CEC2017 runs summary exported to {all_file_name}")
    return function_seed_df

if __name__ == "__main__":
    max_iter = 1000
    # Thêm đường dẫn chứa package cec2017 vào sys.path
    sys.path.append(r"C:\Tai lieu BK\NCKH\TỔNG HỢP CODE\CODE_SOS\COCSOS_Original\Bài toán CEC2017")
    
    # Dictionary chứa tất cả các hàm benchmark
    functions = {}
    common_bound = (-100, 100)
    dim = 100

    # # # # # ----- Lấy hàm từ file simple.py -----
    # from cec2017.simple import all_functions as simple_functions
    # global_mins_simple = [0] * len(simple_functions)  # Giả sử global min = 0 cho tất cả
    # for i, f in enumerate(simple_functions):
    #     func_name = f"simple_f{i+1}"
    #     # Bọc lại để đảm bảo trả về số scalar (lấy phần tử đầu tiên)
    #     wrapped_func = lambda x, f=f: f(x.reshape(1, -1))[0]
    #     functions[func_name] = (wrapped_func, common_bound, global_mins_simple[i], dim)
    
    # # ----- Lấy hàm từ file hybrid.py -----
    # from cec2017.hybrid import all_functions as hybrid_functions
    # global_mins_hybrid = [0] * len(hybrid_functions)
    # for i, f in enumerate(hybrid_functions):
    #     func_name = f"hybrid_f{i+1}"
    #     wrapped_func = lambda x, f=f: f(x.reshape(1, -1))[0]
    #     functions[func_name] = (wrapped_func, common_bound, global_mins_hybrid[i], dim)
    
    # # # # ----- Lấy hàm từ file composition.py -----
    from cec2017.composition import all_functions as composition_functions
    global_mins_composition = [0] * len(composition_functions)
    for i, f in enumerate(composition_functions):
        func_name = f"composition_f{i+1}"
        wrapped_func = lambda x, f=f: f(x.reshape(1, -1))[0]
        functions[func_name] = (wrapped_func, common_bound, global_mins_composition[i], dim)
    
    # In ra danh sách các hàm đã load để kiểm tra
    print("Danh sách các hàm benchmark đã load:")
    for key in functions.keys():
        print(key)
    
    # Chạy thuật toán với tất cả các hàm benchmark đã gộp
    run_multiple_times(functions, n_runs=30, pop_size=50, max_iter=max_iter)
