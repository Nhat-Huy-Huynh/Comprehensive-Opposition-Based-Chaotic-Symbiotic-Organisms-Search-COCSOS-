import time
import numpy as np
import random
import math
import pandas as pd  # Dùng để xuất kết quả ra Excel

# ------------------ Dữ liệu và hàm của bài toán TDS ------------------
D = 90
I_data = [19700, 20555, 8838, 30997, 23197, 47483, 23197, 47483, 47364, 10000,
          45680, 7526, 18292, 8554, 14974, 28338, 7122, 30050, 45220, 9119,
           48631, 4897, 6227, 5546, 13432, 10238, 11594, 35019, 4787, 6055,
            4478, 38724, 41151, 12416, 12482, 18614, 7971, 41151, 35801, 13598,
              37633, 6419, 8182, 33026, 9283, 26784, 36813, 10116, 4703, 24081,
              25694, 2378, 4602, 2597, 3966, 5187, 2246, 37068, 9982, 4157, 36041,
                18649, 35913, 18025, 34533, 7684, 28874, 3621, 5071, 10310, 2566,
                 21877, 22889, 10768, 22885, 10733, 18974, 6992, 16426, 213, 16313,
                   354, 10257, 8195, 16426, 213, 3725, 6605, 17262, 2788 ]  # near

I_data_far = [8838, 8850, 7716, 20555, 3588, 15499, 3588, 15499, 7122, 3677, 
              18292, 5380, 14410, 7526, 6063, 7995, 4310, 10000, 13432, 5840, 
              5615, 2452, 4787, 4303, 11594, 9119, 6179, 10238, 4487, 5546, 2484, 
              6055, 12482, 11359, 7971, 12415, 11359, 18614, 8182, 5379, 9283, 3539, 
              5533, 13598, 3994, 6419, 2291, 1767, 3241, 7715, 4602, 1577, 3966, 2378, 
              2246, 2597, 1511, 5187, 3725, 2413, 12128, 2512, 12752, 2642, 8195, 4036,
                5071, 1908, 2566, 3621, 2051, 10310, 8614, 1027, 8649, 1031, 9638, 5020, 
                9586, 212, 6309, 349, 7684, 6342, 9586, 212, 2788, 4157, 6605, 2146]#far
I_data_mid = [12264, 12388, 8239, 24727, 13259, 26382, 13259, 26382, 12590, 6144,
              26194, 6498, 16126, 8015, 9018, 12694, 5592, 15087, 20790, 7267, 10118,
              3574, 5410, 4850, 12448, 9647, 8198, 15913, 4627, 5789,
              3415, 10512, 20756, 6893, 10133, 15160, 4630, 26258, 13549, 8198,
              14989, 4922, 6772, 19325, 5914, 10479, 32605, 1812, 3867, 11727,
              7853, 1943, 4260, 2484, 2873, 3466, 1537, 32818, 5439, 3073, 34538,
              3157, 34414, 3289, 19208, 4836, 8808, 2711, 3472, 5407,
              2332, 14074, 14066, 5994, 14089, 5983, 12822, 5896, 12159, 212,
              9177, 352, 8800, 7162, 12159, 212, 3191, 5094, 9573, 2445]#mid

I_data_backup = [None,[20555.0],[8838.0],[15499.0,15499.0],[7716.0,15499.0],[3588.0,3677.0,5380.0,5840.0,2452.0],[7716.0,15499.0],
                 [3588.0,3677.0,5380.0,5840.0,2452.0],[3588.0,3588.0,5380.0,5840.0,2452.0],[10000],[3588.0,3588.0,3677.0,5840.0,2452.0],
                 [7526.0],[18292.0],[7995.0],[14410.0],[4310.0],[7122.0],[6063.0],[3588.0,3588.0,3677.0,5380.0,2452.0],[9119.0],
                 [3588.0,3588.0,3677.0,5380.0,5840.0],[4303.0],[5615.0],[5546.0],[13432.0],[10238.0],[11594.0],[2484.0,5379.0,3539.0],
                 [4787.0],[6055.0],[4478.0],[6179.0,5379.0,3539.0],[6179.0,2484.0,5379.0,3539.0],[12416.0],[12482.0],[18614.0],[7971.0],
                 [6179.0,2484.0,5379.0,3539.0],[6179.0,2484.0,3539.0],[13598.0],[6179.0,2484.0,5379.0],[6419.0],[8182.0],[1767.0,1511.0,2512.0,2642.0,4036],
                 [9283.0],[12128.0,12752.0,1908.0],[5533.0,1511.0,2512.0,2642.0,4036],[7715.0,2413.0],[2291.0,2413.0],[1577.0],[3241.0],[2378.0],
                 [4602.0],[2597.0],[3966.0],[5187.0],[2246.0],[5533.0,1767.0,2512.0,2642.0,4036],[2291.0,7715.0],[4157.0],[5533.0,1767.0,1511.0,2642.0,4036],
                 [3994.0,12752.0,1908.0],[5533.0,1767.0,1511.0,2512.0,4036],[3994.0,12128.0,1908.0],[5533.0,1767.0,1511.0,2512.0,2642.0],[7684.0],[3994.0,12128.0,12752.0],
                 [3621.0],[5071.0],[10310.0],[2566.0],[1027.0,1031.0,5020.0],[2051.0,1031.0,5020.0],[8649.0,2146.0],[2051.0,1027.0,5020.0],[8614.0,2146.0],[2051.0,1027.0,1031.0],
                 [212.0,349.0,6342.0,212.0],[9638.0,349.0,6342.0,212.0],None,[9638.0,212.0,6342.0,212.0],None,[9638.0,212.0,349.0,212.0],[8195.0],[9638.0,212.0,349.0,6342.0],None,[3725.0],
                 [6605.0],[8614.0,8649.0],[2788.0]]


backup_pairs = [(1,3),(2,0),(3,5),(3,7),(4,2),(4,7),(5,6),(5,9),(5,11),(5,19),(5,21),(6,2),
                (6,5),(7,4),(7,9),(7,11),(7,19),(7,21),(8,4),(8,6),(8,11),(8,19),(8,21),(9,17),
                (10,4),(10,6),(10,9),(10,19),(10,21),(11,13),(12,10),(13,15),(14,12),(15,16),
                (16,8),(17,14),(18,4),(18,6),(18,9),(18,11),(18,21),(19,25),(20,4),(20,6),(20,9),
                (20,11),(20,19),(21,23),(22,20),(23,29),(24,18),(25,27),(26,24),(27,30),(27,39),
                (27,41),(28,22),(29,31),(30,28),(31,26),(31,39),(31,41),(32,26),(32,30),(32,39),
                (32,41),(33,35),(34,32),(35,37),(36,34),(37,26),(37,30),(37,39),(37,41),(38,26),
                (38,30),(38,41),(39,43),(40,26),(40,30),(40,39),(41,45),(42,38),(43,47),(43,56),
                (43,61),(43,63),(43,65),(44,40),(45,60),(45,62),(45,67),(46,42),(46,56),(46,61),
                (46,63),(46,65),(47,49),(47,59),(48,46),(48,59),(49,51),(50,48),(51,53),(52,50),
                (53,55),(54,52),(55,57),(56,54),(57,42),(57,47),(57,61),(57,63),(57,65),(58,46),
                (58,49),(59,87),(60,42),(60,47),(60,56),(60,63),(60,65),(61,44),(61,62),(61,67),
                (62,42),(62,47),(62,56),(62,61),(62,65),(63,44),(63,60),(63,67),(64,42),(64,47),
                (64,56),(64,61),(64,63),(65,82),(66,44),(66,60),(66,62),(67,69),(68,66),(69,71),
                (70,68),(71,73),(71,75),(71,77),(72,70),(72,75),(72,77),(73,74),(73,89),(74,70),
                (74,73),(74,77),(75,72),(75,89),(76,70),(76,73),(76,75),(77,79),(77,81),(77,83),
                (77,85),(78,76),(78,81),(78,83),(78,85),(80,76),(80,79),(80,83),(80,85),(82,76),
                (82,79),(82,81),(82,85),(83,64),(84,76),(84,79),(84,81),(84,83),(86,58),(87,88),
                (88,72),(88,74),(89,86)]

p_jump = [0.0156,0.0156,0.0313,0.0313,0.047,0.047,0.0313,0.0313,0.0313,0.0313,
          0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0313,0.0313,
          0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0313,0.0313,0.0156,0.0156,
          0.0313,0.0313,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0313,0.0313,
          0.0156,0.0156,0.0781,0.0781,0.047,0.047,0.0156,0.0156,0.0156,0.0156,0.0156,
          0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.047,0.047,0.0156,0.0156,
          0.0156,0.0156,0.0313,0.0313,0.0313,0.0313,0.0156,0.0156,0.0156,0.0156,0.0156,
          0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156
          ,0.0156,0.0156,0.0156,0.0156,0.0156,0.0156]

CT = [1200] * D
CTI = 0.2

# ------------------ Hàm tính thời gian hoạt động của relay ------------------
def time_operation(TDS, Ipickup, I, A, B):
    ratio = I / Ipickup
    if ratio >=20:
        ratio = 20
    return TDS * (A / (ratio**B - 1))

def get_backup_current(primary_idx, count):
    backup_data = I_data_backup[primary_idx]
    if isinstance(backup_data, list):
        return backup_data[count % len(backup_data)] if backup_data else None
    return backup_data

def check_constraints(x) -> float:
    alpha_backup = 5000
    alpha_primary_time = 20000
    alpha_ratio = 1000    
    TDS_values = x[:D]
    PS_values = x[D:2*D]
    A = x[2*D]
    B = x[2*D+1]

    # 1. t_primary
    primary_times = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B) for i in range(D)]
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
        T_backup= time_operation(TDS_values[backup_idx],
                                             CT[backup_idx] * PS_values[backup_idx],
                                             backup_current, A, B)

        violation  = max(0.0, CTI - (T_backup - T_primary))
        penalty   += alpha_backup * violation ** 2
    for i in range(D):
        Ipickup = CT[i] * PS_values[i]
        penalty += alpha_ratio *(max(0,1.2-I_data_far[i] / Ipickup)**2)

    return penalty
def objective_function(x,iteration_count=0):
    TDS_values = x[:D]
    PS_values = x[D:2*D]
    A = x[2*D]
    B = x[2*D+1]
    
    # Tính tổng thời gian hoạt động của relay primary
    primary_times = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B)
                     for i in range(D)]
    primary_times_mid = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_mid[i], A, B)
                     for i in range(D)]
    primary_times_far = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_far[i], A, B)
                     for i in range(D)]
    primary_obj = 0.0
    for i in range(D):
        primary_obj += (
            0.15 * primary_times[i] +
            0.7  * primary_times_mid[i] +
            0.15  * primary_times_far[i]
        ) *p_jump[i]
    
    # Tính hình phạt nếu có vi phạm ràng buộc
    penalty = check_constraints(x)
    
    return primary_obj + penalty

def print_detailed_results(best_solution, best_fitness):
    print("\nBest solution found:")
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2*D]
    A = best_solution[2*D]
    B = best_solution[2*D+1]
    
    print("TDS values:")
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        print(f"Relay {i+1}: TDS = {TDS_values[i]:.4f} sec, I_pickup = {I_pickup:.2f} A")
    print("\nPS values:")
    for i in range(D):
        print(f"Relay {i+1}: PS = {PS_values[i]:.4f} A")
    print(f"\nA = {A:.4f}, B = {B:.4f}")
    print(f"\nBest fitness (total operation time): {best_fitness:.4f} sec")
    
    print("\nOperation times for each relay:")
    primary_times = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B) for i in range(D)]
    for i, t in enumerate(primary_times):
        print(f"Relay {i+1}: {t:.4f} sec")
    
    print("\nCoordination times for backup pairs:")
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        primary_time = primary_times[primary_idx]
        backup_time = time_operation(TDS_values[backup_idx],
                                     CT[backup_idx] * PS_values[backup_idx],
                                     backup_current, A, B)
        coordination_time = backup_time - primary_time
        print(f"Pair (Relay {primary_idx+1}, Relay {backup_idx+1}): Coordination time = {coordination_time:.4f} sec")
    
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
        primary_time = primary_times[primary_idx]
        backup_time = time_operation(TDS_values[backup_idx],
                                     CT[backup_idx] * PS_values[backup_idx],
                                     backup_current, A, B)
        if backup_time - primary_time >= CTI:
            print(f"Backup relay {backup_idx+1} coordinated with primary relay {primary_idx+1}: Success")
        else:
            print(f"Backup relay {backup_idx+1} failed to coordinate with primary relay {primary_idx+1}: Failure")

# ------------------ Hàm hỗ trợ rời rạc hóa PS ------------------
def quantize_solution(x,lb, ub):
    tds = x[:D]
    ps_cont = x[D:2*D]
    A_cont, B_cont = x[2*D], x[2*D+1]
    ps_lb = lb[D:2*D]
    ps_ub = ub[D:2*D]

    # PS: bước 0.5 A
    ps_quant = np.clip(np.round(ps_cont * 100000) / 100000, ps_lb, ps_ub)

    # A: bước 0.01
    step_A = 0.01
    A_quant = np.clip(
        np.round((A_cont - 0.14) / step_A) * step_A + 0.14,
        0.14, 80
    )

    # B: bước 0.01
    step_B = 0.01
    B_quant = np.clip(
        np.round((B_cont - 0.02) / step_B) * step_B + 0.02,
        0.02, 2
    )

    return np.concatenate([tds, ps_quant, [A_quant, B_quant]])
# ------------------ Các hàm hỗ trợ trong thuật toán SOS ------------------
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
        new_sol = quantize_solution(new_sol,lb, ub)  # rời rạc hóa PS
        new_sol = np.clip(new_sol, lb_vec, ub_vec)
        new_fit = obj_func(new_sol)
        if new_fit < candidate_fit:
            candidate, candidate_fit = new_sol.copy(), new_fit

    return candidate, candidate_fit


# ------------------ Các hàm hỗ trợ seed và xuất dữ liệu khởi tạo ------------------
def validate_seed(seed, run=None, function_name=None):
    """Kiểm tra seed hợp lệ cho np.random.seed/random.seed."""
    try:
        seed = int(seed)
    except Exception as exc:
        raise ValueError(
            f"Seed không chuyển được sang int: {seed!r} | Run={run}, Function={function_name}"
        ) from exc

    max_seed = int(np.iinfo(np.uint32).max)
    if seed < 0 or seed > max_seed:
        raise ValueError(
            f"Seed không hợp lệ: {seed} | Run={run}, Function={function_name}. "
            f"Seed phải nằm trong khoảng 0 đến {max_seed}."
        )
    return seed


def set_random_seed(seed):
    """
    Reset đồng thời 2 bộ sinh số ngẫu nhiên đang dùng trong code:
    - numpy.random
    - random của Python
    """
    seed = validate_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    return seed


def make_run_seed_table(num_runs=30, function_name="Relay_TDS_2D_plus_2"):
    """
    Cơ chế seed giống benchmark:
    - Mỗi Run của bài toán relay được cấp đúng 1 seed riêng.
    - Seed được sinh ngẫu nhiên hợp lệ và lưu ra Excel.
    - SOS đọc lại đúng seed theo Run + Function để khởi tạo cùng quần thể ban đầu.
    """
    rng = np.random.default_rng()
    safe_max_seed = 2**31 - 1
    used = set()
    seeds = []

    while len(seeds) < int(num_runs):
        s = int(rng.integers(0, safe_max_seed + 1))
        if s not in used:
            used.add(s)
            seeds.append(s)

    records = []
    for run, seed in enumerate(seeds, start=1):
        records.append({
            "Run": int(run),
            "Function": str(function_name),
            "Seed": validate_seed(seed, run, function_name),
        })

    return pd.DataFrame(records)


def check_seed_table(seed_table, num_runs, function_name="Relay_TDS_2D_plus_2"):
    """Kiểm tra bảng seed đủ số run, đúng cột và seed hợp lệ."""
    required_cols = {"Run", "Function", "Seed"}
    missing = required_cols - set(seed_table.columns)
    if missing:
        raise ValueError(f"seed_table thiếu các cột: {missing}")

    seed_table = seed_table.copy()
    seed_table["Run"] = seed_table["Run"].astype(int)
    seed_table["Function"] = seed_table["Function"].astype(str)
    seed_table["Seed"] = seed_table["Seed"].apply(validate_seed).astype(int)

    expected_rows = int(num_runs)
    if len(seed_table) != expected_rows:
        raise ValueError(
            f"seed_table phải có {expected_rows} dòng = số lần chạy, "
            f"nhưng hiện có {len(seed_table)} dòng."
        )

    expected_pairs = {(run, str(function_name)) for run in range(1, int(num_runs) + 1)}
    actual_pairs = set(zip(seed_table["Run"], seed_table["Function"]))
    missing_pairs = expected_pairs - actual_pairs
    if missing_pairs:
        raise ValueError(f"seed_table thiếu cặp Run + Function: {sorted(missing_pairs)[:10]}")

    if seed_table.duplicated(subset=["Run", "Function"]).any():
        raise ValueError("seed_table bị trùng cặp Run + Function.")

    if seed_table["Seed"].duplicated().any():
        raise ValueError("Có seed bị trùng giữa các lần chạy.")

    return seed_table


def get_run_seed(seed_table, run, function_name="Relay_TDS_2D_plus_2"):
    """Lấy seed ứng với đúng Run + Function từ seed_table."""
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


def build_initial_population_dataframe(
    initial_info,
    run,
    function_name="Relay_TDS_2D_plus_2",
    population_key="Initial Quantized Population",
    of_key="Initial Quantized OF"
):
    """
    Tạo DataFrame quần thể khởi tạo để xuất Excel.
    - Initial Random Population: quần thể vừa sinh bởi np.random.uniform.
    - Initial Quantized Population: quần thể sau khi rời rạc hóa PS, A, B.
    - Initial Quantized OF: giá trị hàm mục tiêu dùng để so sánh công bằng với SOS.
    """
    init_pop = np.asarray(initial_info[population_key])
    coord_cols = [f"x{j + 1}" for j in range(init_pop.shape[1])]

    df_init = pd.DataFrame(init_pop, columns=coord_cols)
    df_init.insert(0, "Initial OF", initial_info[of_key])
    df_init.insert(0, "Individual", np.arange(1, len(init_pop) + 1))
    df_init.insert(0, "Seed", initial_info["Seed"])
    df_init.insert(0, "Function", function_name)
    df_init.insert(0, "Run", run)

    return df_init


def COCSOS(obj_func, bounds, dim, pop_size=100, max_iter=3000, seed=None):
    if seed is not None:
        set_random_seed(seed)

    start_time = time.time()

    lb_TDS = np.array([bounds[0]] * D)
    ub_TDS = np.array([bounds[1]] * D)
    lb_PS = np.array([0.340, 0.340, 0.533, 0.533, 0.800, 0.800,
                            0.407, 0.407, 0.800, 0.800, 0.800, 0.800,
                            0.800, 0.800, 0.800, 0.800, 0.800, 0.800,
                            0.800, 0.800, 0.407, 0.407, 0.407, 0.407,
                            0.800, 0.800, 0.800, 0.800, 0.800, 0.800,
                            0.800, 0.800, 0.800, 0.100, 0.800, 0.800,
                            0.100, 0.800, 0.800, 0.800, 0.800, 0.800,
                            0.800, 0.800, 0.800, 0.800, 0.340, 0.340,
                            0.533, 0.533, 0.340, 0.340, 0.533, 0.533,
                            0.340, 0.340, 0.340, 0.340, 0.340, 0.340,
                            0.340, 0.340, 0.340, 0.340, 0.533, 0.533,
                            0.340, 0.340, 0.407, 0.407, 0.533, 0.533,
                            0.533, 0.600, 0.533, 0.600, 0.533, 0.533,
                            0.340, 0.130, 0.340, 0.210, 0.533, 0.533,
                            0.340, 0.130, 0.407, 0.407, 0.407, 0.407])
    ub_PS = np.array([0.850, 0.850, 1.333, 1.333, 2.000, 2.000,
                1.017, 1.017, 2.000, 2.000, 2.000, 2.000,
                2.000, 2.000, 2.000, 2.000, 2.000, 2.000,
                2.000, 2.000, 1.017, 1.017, 1.017, 1.017,
                2.000, 2.000, 2.000, 2.000, 2.000, 2.000,
                1.400, 2.000, 2.000, 0.500, 2.000, 2.000,
                0.500, 2.000, 2.000, 2.000, 2.000, 2.000,
                2.000, 2.000, 2.000, 2.000, 0.850, 0.850,
                1.333, 1.333, 0.850, 0.850, 1.333, 1.333,
                0.850, 0.850, 0.850, 0.850, 0.850, 0.850,
                0.850, 0.850, 0.850, 0.850, 1.333, 1.333,
                0.850, 0.850, 1.017, 1.017, 1.333, 1.333,
                1.333, 0.700, 1.333, 0.700, 1.333, 1.333,
                0.850, 0.147, 0.850, 0.241, 1.333, 1.333,
                0.850, 0.147, 1.017, 1.017, 1.017, 1.017])
    lb_extra = np.array([0.14, 0.02])
    ub_extra = np.array([80, 2])
    lb = np.concatenate((lb_TDS, lb_PS, lb_extra))
    ub = np.concatenate((ub_TDS, ub_PS, ub_extra))
    
    # ==============================================================
    # 1) Khởi tạo quần thể ngẫu nhiên ban đầu bằng seed đã ghi nhận
    # ==============================================================
    pop_random_initial = np.random.uniform(lb, ub, (pop_size, dim))
    pop_random_initial_quantized = np.array([quantize_solution(ind,lb, ub) for ind in pop_random_initial])

    # Lưu cả OF raw và OF sau quantize. Best history dùng OF sau quantize vì đây là nghiệm hợp lệ.
    fitness_random_raw_initial = np.array([obj_func(ind) for ind in pop_random_initial])
    fitness_random_initial = np.array([obj_func(ind) for ind in pop_random_initial_quantized])

    initial_best_idx = int(np.argmin(fitness_random_initial))
    initial_best_sol = pop_random_initial_quantized[initial_best_idx].copy()
    initial_best_fit = float(fitness_random_initial[initial_best_idx])

    initial_info = {
        "Seed": int(seed) if seed is not None else None,
        "Initial Random Population": pop_random_initial.copy(),
        "Initial Quantized Population": pop_random_initial_quantized.copy(),
        "Initial Raw OF": fitness_random_raw_initial.copy(),
        "Initial Quantized OF": fitness_random_initial.copy(),
        "Initial Best Index": initial_best_idx,
        "Initial Best Individual": initial_best_sol.copy(),
        "Initial Best OF": initial_best_fit,
    }

    # ==============================================================
    # 2) COCSOS
    # ==============================================================
    pop = co_population(pop_random_initial.copy(), lb, ub, iteration=0, max_iter=max_iter)
    pop = np.array([quantize_solution(ind,lb, ub) for ind in pop])
    fitness = np.array([obj_func(ind) for ind in pop])
    best_idx = np.argmin(fitness)
    best_sol = pop[best_idx].copy()
    best_fit = fitness[best_idx]

    # Iteration = 0 lưu giá trị hàm mục tiêu tốt nhất sau khởi tạo quần thể random ban đầu.
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
            new_ind1 = quantize_solution(new_ind1,lb, ub)
            new_fit1 = obj_func(new_ind1)
            if new_fit1 < fitness[i]:
                pop[i] = new_ind1
                fitness[i] = new_fit1
            r2_val = np.random.rand(dim)
            new_ind2 = pop[j] + r2_val * (best_sol - bf2 * mutual)
            new_ind2 = np.clip(new_ind2, lb, ub)
            new_ind2 = quantize_solution(new_ind2,lb, ub)
            new_fit2 = obj_func(new_ind2)
            if new_fit2 < fitness[j]:
                pop[j] = new_ind2
                fitness[j] = new_fit2
        
        # Commensalism Phase
            j = random_select(pop, i)
            r = np.random.uniform(-1, 1, dim)
            new_ind = pop[i] + r * (best_sol - pop[j])
            new_ind = np.clip(new_ind, lb, ub)
            new_ind = quantize_solution(new_ind,lb, ub)
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
            parasite_vec = quantize_solution(parasite_vec,lb, ub)
            parasite_fit = obj_func(parasite_vec)
            if parasite_fit < fitness[host_idx]:
                pop[host_idx] = parasite_vec
                fitness[host_idx] = parasite_fit
        
        # Opposition Phase using Comprehensive Opposition
        if np.random.rand() < 0.4:
            co_pop2 = co_population(pop, lb, ub,iteration,max_iter)
            combined = np.vstack((pop, co_pop2))
            fitness_combined = np.array([obj_func(ind) for ind in combined])
            best_indices = np.argsort(fitness_combined)[:pop_size]
            pop = combined[best_indices]
            pop = np.array([quantize_solution(ind,lb, ub) for ind in pop])
            fitness = fitness_combined[best_indices]

        best_idx = np.argmin(fitness)
        if fitness[best_idx] < best_fit:
            best_sol = pop[best_idx].copy()
            best_fit = fitness[best_idx]

        # ============= Chaotic Local Search =============
        improved_sol, improved_fit = chaotic_local_search(best_sol, best_fit, pop, obj_func, lb, ub, local_search_limit=20)
        if improved_fit < best_fit:
            best_sol = improved_sol
            best_fit = improved_fit

        worst_idx = np.argmax(fitness)
        if fitness[worst_idx] > best_fit:
            pop[worst_idx] = best_sol.copy()
            fitness[worst_idx] = best_fit
            
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
    filename="optimization_results.xlsx",
    run=None,
    seed=None,
    initial_info=None,
    pop_size=None,
    max_iter=None,
    bounds=None,
    dim=None,
    function_name="Relay_TDS_2D_plus_2"
):
    # Fitness History Sheet
    # Iteration = 0 lưu Best Fitness sau khi khởi tạo quần thể random ban đầu.
    df_fitness = pd.DataFrame({
        "Iteration": list(range(0, len(best_fitness_history))),
        "Best Fitness": best_fitness_history,
        "Elapsed Time (sec)": elapsed_time
    })
    
    # Relay Details Sheet
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2*D]
    A = best_solution[2*D]
    B = best_solution[2*D+1]
    relay_data = []
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        op_time = time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B)
        primary_times_mid = time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_mid[i], A, B)
        primary_times_far = time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_far[i], A, B)
        relay_data.append({
            "Relay": i+1,
            "TDS": TDS_values[i],
            "PS": PS_values[i],
            "A": A,
            "B": B,
            "I_pickup": I_pickup,
            "Primary Time Near": op_time,
            "Primary Time Mid": primary_times_mid,
            "Primary Time Far": primary_times_far
        })
    df_relays = pd.DataFrame(relay_data)
    
    # Backup Coordination Sheet
    primary_times = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i], A, B) for i in range(D)]
    backup_records = []
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        primary_time = primary_times[primary_idx]
        backup_val = I_data_backup[primary_idx] if not isinstance(I_data_backup[primary_idx], list) \
                     else get_backup_current(primary_idx, primary_idx_count[primary_idx]-1)
        backup_time = time_operation(TDS_values[backup_idx], CT[backup_idx] * PS_values[backup_idx],
                                     backup_val, A, B)
        coordination_time = backup_time - primary_time
        status = "Success" if coordination_time >= CTI else "Failure"
        backup_records.append({
            "Primary Relay": primary_idx+1,
            "Backup Relay": backup_idx+1,
            "Primary Operation Time": primary_time,
            "Backup Operation Time": backup_time,
            "Coordination Time": coordination_time,
            "CTI": CTI,
            "Status": status
        })
    df_backup = pd.DataFrame(backup_records)
    initial_best_of = None
    initial_best_index = None
    initial_best_individual = None
    if initial_info is not None:
        initial_best_of = initial_info.get("Initial Best OF")
        initial_best_index = int(initial_info.get("Initial Best Index")) + 1
        initial_best_individual = array_to_excel_string(initial_info.get("Initial Best Individual"))

    df_summary = pd.DataFrame({
        "Algorithm": ["COCSOS"],
        "Run": [run],
        "Function": [function_name],
        "Seed": [seed],
        "Dimension": [dim],
        "Pop Size": [pop_size],
        "Max Iter": [max_iter],
        "Bounds": [str(bounds)],
        "Initial Best Index": [initial_best_index],
        "Initial Best OF": [initial_best_of],
        "Initial Best Individual": [initial_best_individual],
        "Elapsed Time (sec)": [elapsed_time],
        "Best Fitness": [best_fitness]
    })
    seed_protocol_df = pd.DataFrame({
        "Algorithm": ["COCSOS"],
        "Run": [run],
        "Function": [function_name],
        "Seed": [seed],
        "Seed Source": ["Generated by COCSOS"],
        "Dimension": [dim],
        "Pop Size": [pop_size],
        "Max Iter": [max_iter],
        "Bounds": [str(bounds)],
        "Initial OF saved at iteration": [0],
        "Initial OF definition": ["Best objective value after random initialization and quantize_solution"]
    })

    with pd.ExcelWriter(filename) as writer:
        df_summary.to_excel(writer, sheet_name="Summary", index=False)
        df_fitness.to_excel(writer, sheet_name="Fitness History", index=False)
        df_relays.to_excel(writer, sheet_name="Relay Details", index=False)
        df_backup.to_excel(writer, sheet_name="Backup Coordination", index=False)
        seed_protocol_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)

        if initial_info is not None:
            df_init_random = build_initial_population_dataframe(
                initial_info,
                run,
                function_name=function_name,
                population_key="Initial Random Population",
                of_key="Initial Raw OF"
            )
            df_init_quantized = build_initial_population_dataframe(
                initial_info,
                run,
                function_name=function_name,
                population_key="Initial Quantized Population",
                of_key="Initial Quantized OF"
            )
            df_init_random.to_excel(writer, sheet_name="Initial_Random_Pop_OF", index=False)
            df_init_quantized.to_excel(writer, sheet_name="Initial_Quantized_Pop_OF", index=False)
    
    print(f"Results exported to {filename}")

# ------------------ Chạy thuật toán COCSOS nhiều lần và xuất Excel ------------------
if __name__ == "__main__":
    bounds = (0.05, 3)  # Miền cho TDS
    pop_size = 100
    max_iter = 5000
    total_dim = 2*D+2  # TDS (D), PS (D), A và B (2)
    num_runs = 20
    function_name = "Relay_TDS_2D_plus_2"
    excel_filename_prefix = "COCSOS_110kV_newPS_newAB_chung_seed_protocol"

    # COCSOS là thuật toán chạy trước, nên tự sinh seed và lưu lại cho SOS đọc.
    seed_table = make_run_seed_table(num_runs=num_runs, function_name=function_name)
    seed_table = check_seed_table(seed_table, num_runs=num_runs, function_name=function_name)

    experiment_info_df = pd.DataFrame({
        "Item": [
            "Algorithm",
            "Problem",
            "Number of independent runs",
            "Decision variables",
            "Population size",
            "Maximum iterations",
            "Seed source",
            "Seed protocol",
            "Random libraries reset",
            "Initial population generation",
            "Initial OF saved at iteration",
            "Reproducibility condition for SOS"
        ],
        "Value": [
            "COCSOS",
            function_name,
            int(num_runs),
            "2D + 2 = TDS(D) + PS(D) + A + B",
            int(pop_size),
            int(max_iter),
            "Generated once by COCSOS and saved to sheet Function_Seeds",
            "Each Run + Function pair uses one recorded seed.",
            "np.random.seed(seed) and random.seed(seed)",
            "pop_random_initial = np.random.uniform(lb, ub, (pop_size, total_dim)) immediately after reset seed",
            "Iteration = 0 stores Initial Best OF after quantize_solution",
            "SOS must read the same Function_Seeds sheet, use the same Run seed, same dim=2D+2, same bounds/lb/ub/pop_size, and must not call random before initial population."
        ]
    })

    all_summary_records = []
    all_seed_records = []

    for run in range(1, num_runs + 1):
        function_seed = get_run_seed(seed_table, run, function_name=function_name)
        print(f"\n======== COCSOS RUN {run} / {num_runs} | Seed = {function_seed} ========")

        best_solution, best_fitness, elapsed_time, history, initial_info = COCSOS(
            objective_function,
            bounds,
            total_dim,
            pop_size,
            max_iter,
            seed=function_seed
        )
        
        print("\nBest solution found:")
        print("TDS values:")
        print(best_solution[:D])
        print("PS values:")
        print(best_solution[D:2*D])
        A = best_solution[2*D]
        B = best_solution[2*D+1]
        print(f"A = {A:.4f}, B = {B:.4f}")
        print(f"Initial Best OF: {initial_info['Initial Best OF']:.12f}")
        print(f"Best fitness (total operation time): {best_fitness:.4f} sec")
        print(f"Elapsed time: {elapsed_time:.4f} sec")

        summary_row = {
            "Algorithm": "COCSOS",
            "Run": run,
            "Function": function_name,
            "Seed": function_seed,
            "Dimension": total_dim,
            "Pop Size": pop_size,
            "Max Iter": max_iter,
            "Bounds": str(bounds),
            "Initial Best Index": initial_info["Initial Best Index"] + 1,
            "Initial Best OF": initial_info["Initial Best OF"],
            "Initial Best Individual": array_to_excel_string(initial_info["Initial Best Individual"]),
            "Best Fitness": best_fitness,
            "Elapsed Time (sec)": elapsed_time,
        }
        all_summary_records.append(summary_row)

        seed_row = {
            "Algorithm": "COCSOS",
            "Run": run,
            "Function": function_name,
            "Seed": function_seed,
            "Seed Source": "Generated by COCSOS",
            "Dimension": total_dim,
            "Pop Size": pop_size,
            "Max Iter": max_iter,
            "Bounds": str(bounds),
        }
        all_seed_records.append(seed_row)

        filename = f"{excel_filename_prefix}_run_{run}.xlsx"
        export_results_to_excel(
            best_solution,
            best_fitness,
            elapsed_time,
            history,
            filename=filename,
            run=run,
            seed=function_seed,
            initial_info=initial_info,
            pop_size=pop_size,
            max_iter=max_iter,
            bounds=bounds,
            dim=total_dim,
            function_name=function_name
        )

    all_summary_df = pd.DataFrame(all_summary_records)
    all_seed_df = pd.DataFrame(all_seed_records)
    function_seed_df = seed_table.copy()
    function_seed_df["Seed Source"] = "Generated by COCSOS"

    all_file_name = f"{excel_filename_prefix}_ALL_SUMMARY.xlsx"
    with pd.ExcelWriter(all_file_name) as writer:
        all_summary_df.to_excel(writer, sheet_name="All_Summary", index=False)
        all_seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        function_seed_df.to_excel(writer, sheet_name="Function_Seeds", index=False)
        function_seed_df.to_excel(writer, sheet_name="Run_Function_Seeds", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

    print(f"\nAll COCSOS runs summary exported to {all_file_name}")
