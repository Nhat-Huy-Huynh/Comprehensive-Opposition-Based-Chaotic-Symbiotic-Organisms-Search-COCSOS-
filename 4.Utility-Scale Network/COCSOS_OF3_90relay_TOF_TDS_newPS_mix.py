import time
import numpy as np
import random
import math
import pandas as pd  # dùng để xuất kết quả ra Excel

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

mode_names = {0: "NI", 1: "VI", 2: "EI"}

def time_operation(TDS, Ipickup, I, mode):
    ratio = I / Ipickup
    if ratio >=20:
        ratio = 20
    if mode == 0:  # NI
        A = 0.14
        B = 0.02
    elif mode == 1:  # VI
        A = 13.5
        B = 1
    elif mode == 2:  # EI
        A = 80
        B = 2
    denominator = (ratio ** B - 1)
    if denominator <= 0:
        base_time = float('inf')
    else:
        base_time = TDS * (A / denominator)
    return base_time

def get_backup_current(primary_idx, count):
    backup_data = I_data_backup[primary_idx]
    if isinstance(backup_data, list):
        return backup_data[count % len(backup_data)] if backup_data else None
    return backup_data

# --- Hàm trợ giúp: chuyển đổi PS sang giá trị rời rạc ---
def discretize_ps(x,lb,ub):
    tds = x[:D]
    ps_cont = x[D:2*D]
    extra = x[2*D:]
    ps_lb = lb[D:2*D]
    ps_ub = ub[D:2*D]
    ps_quant = np.clip(np.round(ps_cont * 100000) / 100000,ps_lb, ps_ub)
    return np.concatenate((tds, ps_quant, extra))

def check_constraints(x) -> float:
    alpha_backup = 5000
    alpha_primary_time = 20000  # phạt thời gian tác động quá nhỏ
    alpha_ratio = 1000          # phạt nếu I / Ipickup < 1.2

    TDS_values = x[:D]
    PS_values = x[D:2*D]
    mode_values = x[2*D:3*D]

    # 1. t_primary
    primary_times = []
    for i in range(D):
        mode_i = int(np.clip(np.rint(mode_values[i]), 0, 2))
        I_pickup = CT[i] * PS_values[i]
        primary_times.append(time_operation(TDS_values[i], I_pickup, I_data[i], mode_i))
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
        mode_backup = int(np.clip(np.rint(mode_values[backup_idx]), 0, 2))
        I_pickup_backup = CT[backup_idx] * PS_values[backup_idx]
        T_backup= time_operation(TDS_values[backup_idx], I_pickup_backup, backup_current, mode_backup)

        violation  = max(0.0, CTI - (T_backup - T_primary))
        penalty   += alpha_backup * violation ** 2

    for i in range(D):
        Ipickup = CT[i] * PS_values[i]
        penalty += alpha_ratio *(max(0,1.2-I_data_far[i] / Ipickup)**2)
    return penalty

def objective_function(x, iteration_count=0):
    TDS_values  = x[:D]
    PS_values   = x[D:2*D]
    mode_values = x[2*D:3*D]

    modes = np.clip(np.rint(mode_values), 0, 2).astype(int)  # shape: (D,)

    primary_times = [
        time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i],      modes[i])
        for i in range(D)
    ]
    primary_times_mid = [
        time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_mid[i],  modes[i])
        for i in range(D)
    ]
    primary_times_far = [
        time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_far[i],  modes[i])
        for i in range(D)
    ]

    # Tổng mục tiêu có trọng số p_jump
    primary_obj = 0.0
    for i in range(D):
        primary_obj += (
            0.15 * primary_times[i] +
            0.7 * primary_times_mid[i] +
            0.15 * primary_times_far[i]
        ) * p_jump[i]
    penalty = check_constraints(x)
    return primary_obj + penalty


def print_detailed_results(best_solution, best_fitness):
    print("\nBest solution found:")
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2*D]
    mode_values = best_solution[2*D:3*D]
    print("Relay details:")
    for i in range(D):
        mode_i = int(np.clip(np.rint(mode_values[i]), 0, 2))
        I_pickup = CT[i] * PS_values[i]
        print(f"Relay {i+1}: TDS = {TDS_values[i]:.4f} sec, PS = {PS_values[i]:.4f} A, Mode = {mode_names[mode_i]}")
        
    print(f"\nBest fitness (total operation time): {best_fitness:.4f} sec")
    
    print("\nOperation times for each relay:")
    for i in range(D):
        mode_i = int(np.clip(np.rint(mode_values[i]), 0, 2))
        I_pickup = CT[i] * PS_values[i]
        t = time_operation(TDS_values[i], I_pickup, I_data[i], mode_i)
        print(f"Relay {i+1}: {t:.4f} sec")
    
    print("\nDetailed Backup Coordination Times:")
    header = f"{'Primary Relay':<15} {'Backup Relay':<15} {'Primary Time (sec)':<20} {'Backup Time (sec)':<20} {'Coordination Time (sec)':<25}"
    print(header)
    print("-" * len(header))
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        
        mode_primary = int(np.clip(np.rint(mode_values[primary_idx]), 0, 2))
        mode_backup = int(np.clip(np.rint(mode_values[backup_idx]), 0, 2))
        primary_time = time_operation(TDS_values[primary_idx], CT[primary_idx] * PS_values[primary_idx], I_data[primary_idx], mode_primary)
        backup_time = time_operation(TDS_values[backup_idx], CT[backup_idx] * PS_values[backup_idx], backup_current, mode_backup)
        coordination_time = backup_time - primary_time
        
        print(f"{primary_idx+1:<15} {backup_idx+1:<15} {primary_time:<20.4f} {backup_time:<20.4f} {coordination_time:<25.4f}")

# ------------------ Hàm lấy DataFrame chi tiết Backup Coordination ------------------
def get_backup_coordination_df(best_solution):
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2*D]
    mode_values = best_solution[2*D:3*D]
    backup_rows = []
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        mode_primary = int(np.clip(np.rint(mode_values[primary_idx]), 0, 2))
        mode_backup = int(np.clip(np.rint(mode_values[backup_idx]), 0, 2))
        primary_time = time_operation(TDS_values[primary_idx], CT[primary_idx] * PS_values[primary_idx], I_data[primary_idx], mode_primary)
        backup_time = time_operation(TDS_values[backup_idx], CT[backup_idx] * PS_values[backup_idx], backup_current, mode_backup)
        coordination_time = backup_time - primary_time
        backup_rows.append({
            "Primary Relay": primary_idx + 1,
            "Backup Relay": backup_idx + 1,
            "Primary Time (sec)": primary_time,
            "Backup Time (sec)": backup_time,
            "Coordination Time (sec)": coordination_time
        })
    return pd.DataFrame(backup_rows)

# ------------------ Các hàm hỗ trợ trong thuật toán SOS_AFDB ------------------
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
        P_qo  = 1.41 - 1.92 * ratio
    
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
        new_sol = discretize_ps(new_sol,lb,ub)  # rời rạc hóa PS
        new_sol = np.clip(new_sol, lb_vec, ub_vec)
        new_fit = obj_func(new_sol)
        if new_fit < candidate_fit:
            candidate, candidate_fit = new_sol.copy(), new_fit

    return candidate, candidate_fit


# ------------------ Các hàm hỗ trợ seed và xuất Excel cho so sánh công bằng ------------------
FUNCTION_NAME = "Relay_TDS_3D"
MAX_UINT32_SEED = int(np.iinfo(np.uint32).max)

def validate_seed(seed, run=None, function_name=None):
    """Đảm bảo seed là số nguyên hợp lệ cho np.random.seed và random.seed."""
    try:
        seed = int(seed)
    except Exception as exc:
        raise ValueError(
            f"Seed không chuyển được sang int: {seed!r} | Run={run}, Function={function_name}"
        ) from exc

    if seed < 0 or seed > MAX_UINT32_SEED:
        raise ValueError(
            f"Seed không hợp lệ: {seed} | Run={run}, Function={function_name}. "
            f"Seed phải nằm trong khoảng 0 đến {MAX_UINT32_SEED}."
        )
    return seed

def set_random_seed(seed):
    """
    Reset đồng thời 2 bộ sinh số ngẫu nhiên đang dùng trong code:
    - np.random
    - random
    """
    seed = validate_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    return seed

def make_run_seed_table(num_runs=30, function_name=FUNCTION_NAME):
    """
    COCSOS là thuật toán chạy trước nên tự sinh bảng seed.
    Mỗi Run của bài toán relay 3D có đúng 1 seed riêng.
    SOS sẽ đọc lại bảng này để dùng cùng seed và tạo cùng quần thể khởi tạo.
    """
    rng = np.random.default_rng()
    safe_max_seed = 2**31 - 1
    used = set()
    records = []

    for run in range(1, int(num_runs) + 1):
        while True:
            seed = int(rng.integers(0, safe_max_seed + 1))
            if seed not in used:
                used.add(seed)
                break

        records.append({
            "Run": run,
            "Function": str(function_name),
            "Seed": validate_seed(seed, run, function_name),
            "Seed Source": "Generated by COCSOS",
        })

    return pd.DataFrame(records)

def check_seed_table(seed_table, num_runs, function_name=FUNCTION_NAME):
    """Kiểm tra bảng seed đủ cột, đủ run và seed hợp lệ."""
    required_cols = {"Run", "Function", "Seed"}
    missing = required_cols - set(seed_table.columns)
    if missing:
        raise ValueError(f"seed_table thiếu các cột: {missing}")

    seed_table = seed_table.copy()
    seed_table["Run"] = seed_table["Run"].astype(int)
    seed_table["Function"] = seed_table["Function"].astype(str)
    seed_table["Seed"] = seed_table["Seed"].apply(validate_seed).astype(int)

    expected_runs = set(range(1, int(num_runs) + 1))
    actual_runs = set(seed_table["Run"])
    missing_runs = expected_runs - actual_runs
    if missing_runs:
        raise ValueError(f"seed_table thiếu Run: {sorted(missing_runs)}")

    if len(seed_table) != int(num_runs):
        raise ValueError(
            f"seed_table phải có {num_runs} dòng cho {num_runs} run, "
            f"nhưng hiện có {len(seed_table)} dòng."
        )

    if seed_table.duplicated(subset=["Run", "Function"]).any():
        raise ValueError("seed_table bị trùng cặp Run + Function.")

    return seed_table

def get_run_seed(seed_table, run, function_name=FUNCTION_NAME):
    """Lấy đúng seed theo Run + Function."""
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
        separator=", ",
        max_line_width=100000
    )

def population_to_dataframe(pop, fitness, run, function_name, seed, prefix_of="Initial OF"):
    """Tạo bảng quần thể + giá trị hàm mục tiêu để xuất Excel."""
    pop = np.asarray(pop)
    fitness = np.asarray(fitness, dtype=float)

    df = pd.DataFrame(pop, columns=[f"x{j+1}" for j in range(pop.shape[1])])
    df.insert(0, prefix_of, fitness)
    df.insert(0, "Individual", np.arange(1, pop.shape[0] + 1))
    df.insert(0, "Seed", int(seed) if seed is not None else None)
    df.insert(0, "Function", function_name)
    df.insert(0, "Run", int(run) if run is not None else None)
    return df

def make_experiment_info_df(num_runs, pop_size, max_iter, dim, seed_file_name):
    return pd.DataFrame({
        "Item": [
            "Algorithm",
            "Problem",
            "Number of relays",
            "Number of search variables",
            "Search variable structure",
            "Number of independent runs",
            "Population size",
            "Maximum iterations",
            "Seed source",
            "Seed protocol",
            "Random libraries reset",
            "Initial population for fair comparison",
            "Reproducibility condition",
            "COCSOS seed output file",
        ],
        "Value": [
            "COCSOS",
            "90-relay TDS coordination with mixed NI/VI/EI mode",
            int(D),
            int(dim),
            "3D = TDS(D) + PS(D) + mode(D)",
            int(num_runs),
            int(pop_size),
            int(max_iter),
            "Generated once by COCSOS and saved to sheet Function_Seeds",
            "Each Run uses one recorded seed for Function=Relay_TDS_3D.",
            "np.random.seed(seed) and random.seed(seed)",
            "Initial_Random_Pop_OF sheet records np.random.uniform(lb, ub, (pop_size, dim)) before CO population.",
            "SOS must read Function_Seeds, use the same Run seed, and must not call random before creating its initial population.",
            seed_file_name,
        ]
    })

def COCSOS(obj_func, bounds, dim, pop_size=100, max_iter=3000, seed=None, run=None, function_name=FUNCTION_NAME):
    if seed is not None:
        set_random_seed(seed)

    start_time = time.time()

    D_local = dim // 3  
    lb = np.concatenate((
        np.full(D_local, bounds[0]),  # TDS thấp nhất
        np.array([0.340, 0.340, 0.533, 0.533, 0.800, 0.800,
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
                            0.340, 0.130, 0.407, 0.407, 0.407, 0.407]),                        # PS thấp nhất theo từng relay
        np.zeros(D_local)             # mode in [0, 2]
    ))
    ub = np.concatenate((
        np.full(D_local, bounds[1]),  # TDS cao nhất
        np.array([0.850, 0.850, 1.333, 1.333, 2.000, 2.000,
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
                0.850, 0.147, 1.017, 1.017, 1.017, 1.017]),                 # PS cao nhất theo từng relay
        np.full(D_local, 2.0)         # mode in [0, 2]
    ))
    
    # ==============================================================
    # 1) Khởi tạo quần thể ngẫu nhiên ban đầu bằng seed đã ghi nhận
    # ==============================================================
    pop_random_initial = np.random.uniform(lb, ub, (pop_size, dim))
    fitness_random_initial = np.array([obj_func(ind) for ind in pop_random_initial])

    initial_best_idx = int(np.argmin(fitness_random_initial))
    initial_best_sol = pop_random_initial[initial_best_idx].copy()
    initial_best_fit = float(fitness_random_initial[initial_best_idx])

    initial_info = {
        "Run": int(run) if run is not None else None,
        "Function": str(function_name),
        "Seed": int(seed) if seed is not None else None,
        "Initial Random Population": pop_random_initial.copy(),
        "Initial Random OF": fitness_random_initial.copy(),
        "Initial Best Index": initial_best_idx,
        "Initial Best Individual": initial_best_sol.copy(),
        "Initial Best OF": initial_best_fit,
        "Lower Bounds": lb.copy(),
        "Upper Bounds": ub.copy(),
    }

    # ==============================================================
    # 2) COCSOS tiếp tục dùng quần thể random ban đầu này để tạo CO population
    # ==============================================================
    pop = co_population(pop_random_initial.copy(), lb, ub, iteration=0, max_iter=max_iter)
    fitness = np.array([obj_func(ind) for ind in pop])
    best_idx = np.argmin(fitness)
    best_sol = pop[best_idx].copy()
    best_fit = fitness[best_idx]

    # Lưu Iteration = 0 là Best OF của quần thể random ban đầu để so sánh với SOS.
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
            new_ind1 = discretize_ps(new_ind1,lb,ub)
            new_fit1 = obj_func(new_ind1)
            if new_fit1 < fitness[i]:
                pop[i] = new_ind1
                fitness[i] = new_fit1
            r2_val = np.random.rand(dim)
            new_ind2 = pop[j] + r2_val * (best_sol - bf2 * mutual)
            new_ind2 = np.clip(new_ind2, lb, ub)
            new_ind2 = discretize_ps(new_ind2,lb,ub)
            new_fit2 = obj_func(new_ind2)
            if new_fit2 < fitness[j]:
                pop[j] = new_ind2
                fitness[j] = new_fit2
        
        # Commensalism Phase
            j = random_select(pop, i)
            r = np.random.uniform(-1, 1, dim)
            new_ind = pop[i] + r * (best_sol - pop[j])
            new_ind = np.clip(new_ind, lb, ub)
            new_ind = discretize_ps(new_ind,lb,ub)
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
            parasite_vec = discretize_ps(parasite_vec,lb,ub)
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
            pop = np.array([discretize_ps(ind,lb,ub) for ind in pop])
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

# --- Hàm xuất kết quả ra file Excel ---
def export_results_to_excel(
    best_solution,
    best_fitness,
    best_fitness_history,
    run_index,
    elapsed_time,
    seed,
    initial_info,
    filename,
    function_name=FUNCTION_NAME,
):
    # DataFrame cho lịch sử vòng lặp
    # Iteration = 0 là giá trị Best OF sau khởi tạo random ban đầu.
    df_iterations = pd.DataFrame({
        "Iteration": list(range(0, len(best_fitness_history))),
        "Best Fitness": best_fitness_history
    })

    # DataFrame cho chi tiết giải pháp tốt nhất
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2*D]
    mode_values = best_solution[2*D:3*D]
    data_solution = []
    for i in range(D):
        mode_i = int(np.clip(np.rint(mode_values[i]), 0, 2))
        I_pickup = CT[i] * PS_values[i]
        op_time = time_operation(TDS_values[i], I_pickup, I_data[i], mode_i)
        primary_times_mid = time_operation(TDS_values[i], I_pickup, I_data_mid[i], mode_i)
        primary_times_far = time_operation(TDS_values[i], I_pickup, I_data_far[i], mode_i)
        data_solution.append({
            "Relay": i+1,
            "TDS": TDS_values[i],
            "PS": PS_values[i],
            "Mode_Value": mode_values[i],
            "Mode": mode_names[mode_i],
            "I_pickup": I_pickup,
            "Primary Time Near": op_time,
            "Primary Time Mid": primary_times_mid,
            "Primary Time Far": primary_times_far
        })
    df_solution = pd.DataFrame(data_solution)

    # DataFrame cho Backup Coordination Times
    df_backup = get_backup_coordination_df(best_solution)

    # DataFrame cho Summary
    df_summary = pd.DataFrame({
        "Algorithm": ["COCSOS"],
        "Run": [int(run_index)],
        "Function": [function_name],
        "Seed": [int(seed)],
        "Dimension": [len(best_solution)],
        "Search Variable Structure": ["3D = TDS(D) + PS(D) + mode(D)"],
        "Initial Best Index": [initial_info["Initial Best Index"] + 1],
        "Initial Best OF": [initial_info["Initial Best OF"]],
        "Initial Best Individual": [array_to_excel_string(initial_info["Initial Best Individual"])],
        "Best Fitness": [best_fitness],
        "Best Solution": [array_to_excel_string(best_solution)],
        "Elapsed Time (sec)": [elapsed_time],
    })

    df_seed = pd.DataFrame([{
        "Algorithm": "COCSOS",
        "Run": int(run_index),
        "Function": function_name,
        "Seed": int(seed),
        "Seed Source": "Generated by COCSOS",
        "Dimension": len(best_solution),
        "Pop Size": len(initial_info["Initial Random Population"]),
        "Initial Best OF": initial_info["Initial Best OF"],
    }])

    # Bảng quan trọng để SOS kiểm tra đầu vào giống nhau
    df_initial_random = population_to_dataframe(
        initial_info["Initial Random Population"],
        initial_info["Initial Random OF"],
        run=run_index,
        function_name=function_name,
        seed=seed,
        prefix_of="Initial Random OF"
    )

    with pd.ExcelWriter(filename) as writer:
        df_summary.to_excel(writer, sheet_name="Summary", index=False)
        df_seed.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        df_iterations.to_excel(writer, sheet_name="Iteration History", index=False)
        df_initial_random.to_excel(writer, sheet_name="Initial_Random_Pop_OF", index=False)
        df_solution.to_excel(writer, sheet_name="Best Solution", index=False)
        df_backup.to_excel(writer, sheet_name="Backup Coordination", index=False)

    print(f"Results exported to '{filename}'")


def run_all_cocsos_with_seed_protocol(
    excel_filename_prefix="COCSOS_110kV_TOF_newPS_mix_3D_seed_protocol",
    num_runs=15,
    pop_size=100,
    max_iter=5000,
):
    bounds = (0.05, 3)  # Giới hạn của TDS
    dim = 3 * D         # Tổng số biến: D cho TDS, D cho PS, D cho mode
    function_name = FUNCTION_NAME

    seed_table = make_run_seed_table(num_runs=num_runs, function_name=function_name)
    seed_table = check_seed_table(seed_table, num_runs=num_runs, function_name=function_name)

    all_summary_records = []
    all_seed_records = []

    all_summary_filename = f"{excel_filename_prefix}_ALL_SUMMARY.xlsx"
    experiment_info_df = make_experiment_info_df(
        num_runs=num_runs,
        pop_size=pop_size,
        max_iter=max_iter,
        dim=dim,
        seed_file_name=all_summary_filename,
    )

    for run in range(1, int(num_runs) + 1):
        function_seed = get_run_seed(seed_table, run, function_name=function_name)

        print(f"\n--- COCSOS Run {run}/{num_runs} | Function={function_name} | Seed={function_seed} ---")
        best_solution, best_fitness, elapsed_time, history, initial_info = COCSOS(
            objective_function,
            bounds,
            dim,
            pop_size,
            max_iter,
            seed=function_seed,
            run=run,
            function_name=function_name,
        )

        print(f"Run {run} completed in {elapsed_time:.4f} sec with best fitness = {best_fitness:.4f}")

        file_name = f"{excel_filename_prefix}_run_{run}.xlsx"
        export_results_to_excel(
            best_solution=best_solution,
            best_fitness=best_fitness,
            best_fitness_history=history,
            run_index=run,
            elapsed_time=elapsed_time,
            seed=function_seed,
            initial_info=initial_info,
            filename=file_name,
            function_name=function_name,
        )

        summary_row = {
            "Algorithm": "COCSOS",
            "Run": run,
            "Function": function_name,
            "Seed": function_seed,
            "Dimension": dim,
            "Search Variable Structure": "3D = TDS(D) + PS(D) + mode(D)",
            "Pop Size": pop_size,
            "Max Iter": max_iter,
            "Initial Best Index": initial_info["Initial Best Index"] + 1,
            "Initial Best OF": initial_info["Initial Best OF"],
            "Initial Best Individual": initial_info["Initial Best Individual"],
            "Best Fitness": best_fitness,
            "Best Solution": best_solution,
            "Elapsed Time (sec)": elapsed_time,
        }
        all_summary_records.append(summary_row)

        all_seed_records.append({
            "Algorithm": "COCSOS",
            "Run": run,
            "Function": function_name,
            "Seed": function_seed,
            "Seed Source": "Generated by COCSOS",
            "Dimension": dim,
            "Pop Size": pop_size,
            "Max Iter": max_iter,
            "Initial Best OF": initial_info["Initial Best OF"],
        })

    all_summary_df = pd.DataFrame(all_summary_records)
    if not all_summary_df.empty:
        all_summary_df["Initial Best Individual"] = all_summary_df["Initial Best Individual"].apply(array_to_excel_string)
        all_summary_df["Best Solution"] = all_summary_df["Best Solution"].apply(array_to_excel_string)

    all_seed_df = pd.DataFrame(all_seed_records)
    function_seed_df = seed_table.copy()

    with pd.ExcelWriter(all_summary_filename) as writer:
        all_summary_df.to_excel(writer, sheet_name="All_Summary", index=False)
        all_seed_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        function_seed_df.to_excel(writer, sheet_name="Function_Seeds", index=False)
        function_seed_df.to_excel(writer, sheet_name="Run_Function_Seeds", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

    print(f"\nAll COCSOS runs summary exported to {all_summary_filename}")
    return function_seed_df


# ------------------ Chạy thuật toán 30 lần và xuất kết quả ra Excel ------------------
if __name__ == "__main__":
    run_all_cocsos_with_seed_protocol(
        excel_filename_prefix="COCSOS_110kV_TOF_newPS_mix_3D_seed_protocol",
        num_runs=10,
        pop_size=100,
        max_iter=5000,
    )
