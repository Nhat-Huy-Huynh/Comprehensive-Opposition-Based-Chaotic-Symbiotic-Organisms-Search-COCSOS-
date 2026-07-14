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

def time_operation(TDS, Ipickup, I):
    ratio = I / Ipickup
    if ratio >=20:
        ratio = 20
    return TDS * (13.5/ (ratio**1 - 1))

def get_backup_current(primary_idx, count):
    backup_data = I_data_backup[primary_idx]
    if isinstance(backup_data, list):
        return backup_data[count % len(backup_data)] if backup_data else None
    return backup_data


def check_constraints(x, iteration_count=0):
    alpha_backup = 5000
    alpha_primary_time = 20000
    alpha_ratio = 1000
    penalty = 0.0

    TDS_values = x[:D]
    PS_values  = x[D:2*D]
    
    # 1) compute primary operation times
    primary_times = [
        time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i])
        for i in range(D)
    ]
    
    # 2) count any primary times that are too small
    for t in primary_times:
        penalty += alpha_primary_time *(max(0,0.015 - t) ** 2)
    
    # 3) enforce I/Ipickup >= 1.2  for each relay
    for i in range(D):
        Ipickup = CT[i] * PS_values[i]
        penalty += alpha_ratio *(max(0,1.2-I_data_far[i] / Ipickup)**2)

    # 4) check backup coordination as before
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        if backup_current is not None:
            T_backup = time_operation(TDS_values[backup_idx],CT[backup_idx] * PS_values[backup_idx],backup_current)
            T_primary = primary_times[primary_idx]
            dt= T_backup - T_primary
            violation = max(0, CTI - dt)
            penalty += alpha_backup * violation ** 2
        primary_idx_count[primary_idx] += 1

    return penalty

def objective_function(x, iteration_count=0):
    # Tách vector giải pháp thành TDS và PS
    TDS_values = x[:D]
    PS_values = x[D:2*D]
    
    # Tính tổng thời gian hoạt động của relay primary
    primary_times = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i])
                     for i in range(D)]
    primary_times_mid = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_mid[i])
                     for i in range(D)]
    primary_times_far = [time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_far[i])
                     for i in range(D)]
    primary_obj = 0.0
    for i in range(D):
        primary_obj += (
            0.15 * primary_times[i] +
            0.7 * primary_times_mid[i] +
            0.15  * primary_times_far[i]
        ) *p_jump[i]
    
    # Tính hình phạt nếu có vi phạm ràng buộc
    penalty = check_constraints(x,iteration_count)
    
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
def quantize_solution(x,lb,ub):
    D_local = len(x) // 2
    tds = x[:D_local]
    ps_cont = x[D_local:2*D_local]
    ps_lb = lb[D_local:]
    ps_ub = ub[D_local:]
    ps_quant = np.clip(np.round(ps_cont * 100000) / 100000,ps_lb, ps_ub)
    return np.concatenate((tds, ps_quant))
# ------------------ Các hàm hỗ trợ trong thuật toán COSOS ------------------
def random_select(pop, i):
    candidates = [k for k in range(len(pop)) if k != i]
    return np.random.choice(candidates)

# ------------------ Các hàm hỗ trợ seed, bounds và xuất dữ liệu khởi tạo ------------------
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
    Reset đồng thời 2 bộ sinh số ngẫu nhiên để đồng bộ với COCSOS:
    - numpy.random
    - random của Python
    """
    seed = validate_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    return seed


def get_bounds_vectors(bounds, dim):
    """
    Trả về lb/ub giống đúng code COCSOS cho bài toán 90 relay.
    Lưu ý: SOS phải dùng cùng lb/ub với COCSOS thì cùng seed mới sinh ra cùng quần thể.
    """
    D_local = dim // 2
    if D_local != D:
        raise ValueError(f"D_local={D_local} không khớp D={D}. Kiểm tra dim = 2*D.")

    ps_lb = np.array([
                            0.340, 0.340, 0.533, 0.533, 0.800, 0.800,
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
                            0.340, 0.130, 0.407, 0.407, 0.407, 0.407
    ], dtype=float)

    ps_ub = np.array([
                0.850, 0.850, 1.333, 1.333, 2.000, 2.000,
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
                0.850, 0.147, 1.017, 1.017, 1.017, 1.017
    ], dtype=float)

    if len(ps_lb) != D or len(ps_ub) != D:
        raise ValueError("Số phần tử ps_lb/ps_ub phải bằng D=90.")

    lb = np.concatenate((np.array([bounds[0]] * D_local, dtype=float), ps_lb))
    ub = np.concatenate((np.array([bounds[1]] * D_local, dtype=float), ps_ub))
    return lb, ub


def load_seed_table_from_cocsos(seed_excel_path, function_name="COCSOS_NI_110kV", sheet_candidates=None):
    """
    Đọc seed do COCSOS xuất ra từ file ALL_SUMMARY.
    Ưu tiên sheet Function_Seeds; nếu không có thì thử Run_Function_Seeds.
    """
    if sheet_candidates is None:
        sheet_candidates = ["Function_Seeds", "Run_Function_Seeds", "Seed_Protocol"]

    last_error = None
    seed_table = None
    used_sheet = None

    for sheet in sheet_candidates:
        try:
            df = pd.read_excel(seed_excel_path, sheet_name=sheet)
            if {"Run", "Function", "Seed"}.issubset(df.columns):
                seed_table = df.copy()
                used_sheet = sheet
                break
        except Exception as exc:
            last_error = exc

    if seed_table is None:
        raise ValueError(
            f"Không đọc được bảng seed từ file {seed_excel_path}. "
            f"Cần có sheet chứa các cột Run, Function, Seed. Lỗi cuối: {last_error}"
        )

    seed_table["Run"] = seed_table["Run"].astype(int)
    seed_table["Function"] = seed_table["Function"].astype(str)
    seed_table["Seed"] = seed_table["Seed"].apply(validate_seed).astype(int)

    filtered = seed_table[seed_table["Function"] == str(function_name)].copy()
    if filtered.empty:
        available = sorted(seed_table["Function"].astype(str).unique().tolist())
        raise ValueError(
            f"Không tìm thấy Function='{function_name}' trong sheet {used_sheet}. "
            f"Các Function hiện có: {available}"
        )

    if filtered.duplicated(subset=["Run", "Function"]).any():
        raise ValueError("Bảng seed bị trùng cặp Run + Function.")

    filtered = filtered.sort_values("Run").reset_index(drop=True)
    filtered.attrs["Used Seed Sheet"] = used_sheet
    return filtered


def get_run_seed(seed_table, run, function_name="COCSOS_NI_110kV"):
    """Lấy đúng seed theo cặp Run + Function."""
    row = seed_table[
        (seed_table["Run"].astype(int) == int(run)) &
        (seed_table["Function"].astype(str) == str(function_name))
    ]
    if row.empty:
        raise ValueError(f"Không tìm thấy seed cho Run={run}, Function={function_name}")
    return validate_seed(row.iloc[0]["Seed"], run, function_name)


def load_cocsos_initial_summary(seed_excel_path, function_name="COCSOS_NI_110kV"):
    """Đọc Initial Best OF của COCSOS trong sheet All_Summary để đối chiếu với SOS."""
    try:
        df = pd.read_excel(seed_excel_path, sheet_name="All_Summary")
    except Exception:
        return pd.DataFrame()

    required = {"Run", "Function", "Initial Best OF"}
    if not required.issubset(df.columns):
        return pd.DataFrame()

    df = df[df["Function"].astype(str) == str(function_name)].copy()
    if df.empty:
        return pd.DataFrame()

    df["Run"] = df["Run"].astype(int)
    return df[["Run", "Function", "Initial Best OF"]].rename(
        columns={"Initial Best OF": "COCSOS Initial Best OF"}
    )


def array_to_excel_string(arr, precision=12):
    """Chuyển vector nghiệm sang chuỗi để ghi gọn vào Excel."""
    return np.array2string(
        np.asarray(arr),
        precision=precision,
        separator=', ',
        max_line_width=10_000
    )


def build_initial_population_dataframe(initial_info, run, function_name="COCSOS_NI_110kV", population_key="Initial Random Population"):
    """
    Tạo DataFrame quần thể khởi tạo để xuất Excel.
    population_key có thể là:
    - Initial Random Population
    - Initial Quantized Population
    """
    init_pop = np.asarray(initial_info[population_key])
    coord_cols = [f"x{j + 1}" for j in range(init_pop.shape[1])]

    df_init = pd.DataFrame(init_pop, columns=coord_cols)
    df_init.insert(0, "Initial OF", initial_info["Initial Random OF"])
    df_init.insert(0, "Individual", np.arange(1, len(init_pop) + 1))
    df_init.insert(0, "Seed", initial_info["Seed"])
    df_init.insert(0, "Function", function_name)
    df_init.insert(0, "Run", run)
    return df_init


def compare_initial_best_with_cocsos(initial_best_of, cocsos_initial_best_of, atol=1e-9, rtol=1e-9):
    """Trả về True nếu Initial Best OF của SOS khớp COCSOS trong dung sai."""
    if pd.isna(cocsos_initial_best_of):
        return None
    return bool(np.isclose(float(initial_best_of), float(cocsos_initial_best_of), atol=atol, rtol=rtol))


def SOS(obj_func, bounds, dim, pop_size=100, max_iter=3000, seed=None):
    """
    SOS gốc đã bổ sung seed protocol:
    - Đọc seed từ COCSOS bên ngoài và truyền vào tham số seed.
    - Reset np.random và random trước khi khởi tạo.
    - Khởi tạo pop_random_initial giống COCSOS bằng np.random.uniform(lb, ub, (pop_size, dim)).
    - Lưu Initial Random Population, Initial Quantized Population và Initial OF.
    """
    if seed is not None:
        set_random_seed(seed)

    start_time = time.time()
    lb, ub = get_bounds_vectors(bounds, dim)

    # ==============================================================
    # 1) Khởi tạo quần thể ban đầu giống COCSOS bằng cùng seed
    # ==============================================================
    pop_random_initial = np.random.uniform(lb, ub, (pop_size, dim))
    pop_random_initial_quantized = np.array([quantize_solution(ind, lb, ub) for ind in pop_random_initial])
    fitness_random_initial = np.array([obj_func(ind) for ind in pop_random_initial_quantized])

    initial_best_idx = int(np.argmin(fitness_random_initial))
    initial_best_sol = pop_random_initial_quantized[initial_best_idx].copy()
    initial_best_fit = float(fitness_random_initial[initial_best_idx])

    initial_info = {
        "Seed": int(seed) if seed is not None else None,
        "Initial Random Population": pop_random_initial.copy(),
        "Initial Quantized Population": pop_random_initial_quantized.copy(),
        "Initial Random OF": fitness_random_initial.copy(),
        "Initial Best Index": initial_best_idx,
        "Initial Best Individual": initial_best_sol.copy(),
        "Initial Best OF": initial_best_fit,
    }

    # SOS bắt đầu trực tiếp từ quần thể sau lượng tử hóa.
    # Đây là điểm khác COCSOS: COCSOS còn áp dụng thêm CO population như một cải tiến của thuật toán.
    pop = pop_random_initial_quantized.copy()
    fitness = fitness_random_initial.copy()
    best_idx = int(np.argmin(fitness))
    best_sol = pop[best_idx].copy()
    best_fit = float(fitness[best_idx])

    # Iteration = 0 lưu giá trị tốt nhất sau khởi tạo random ban đầu.
    best_fitness_history = [initial_best_fit]

    for iteration in range(1, max_iter + 1):
        for i in range(pop_size):
            # Mutualism Phase
            best_idx = int(np.argmin(fitness))
            best_sol = pop[best_idx].copy()
            j = random_select(pop, i)
            mutual = (pop[i] + pop[j]) / 2.0
            bf1, bf2 = np.random.randint(1, 3, size=2)  

            r1_val = np.random.rand(dim)
            new_ind1 = pop[i] + r1_val * (best_sol - bf1 * mutual)
            new_ind1 = np.clip(new_ind1, lb, ub)
            new_ind1 = quantize_solution(new_ind1, lb, ub)
            new_fit1 = obj_func(new_ind1, iteration)
            if new_fit1 < fitness[i]:
                pop[i] = new_ind1
                fitness[i] = new_fit1

            r2_val = np.random.rand(dim)
            new_ind2 = pop[j] + r2_val * (best_sol - bf2 * mutual)
            new_ind2 = np.clip(new_ind2, lb, ub)
            new_ind2 = quantize_solution(new_ind2, lb, ub)
            new_fit2 = obj_func(new_ind2, iteration)
            if new_fit2 < fitness[j]:
                pop[j] = new_ind2
                fitness[j] = new_fit2

            # Commensalism Phase
            j = random_select(pop, i)
            r = np.random.uniform(-1, 1, dim)
            new_ind = pop[i] + r * (best_sol - pop[j])
            new_ind = np.clip(new_ind, lb, ub)
            new_ind = quantize_solution(new_ind, lb, ub)
            new_fit = obj_func(new_ind, iteration)
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
            parasite_vec = quantize_solution(parasite_vec, lb, ub)
            parasite_fit = obj_func(parasite_vec, iteration)
            if parasite_fit < fitness[host_idx]:
                pop[host_idx] = parasite_vec
                fitness[host_idx] = parasite_fit

        best_idx_now = int(np.argmin(fitness))
        best_sol = pop[best_idx_now].copy()
        best_fit = float(fitness[best_idx_now])
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
    function_name="COCSOS_NI_110kV",
    seed_excel_path=None,
    cocsos_initial_best_of=None
):
    TDS_values = best_solution[:D]
    PS_values = best_solution[D:2*D]

    df_fitness = pd.DataFrame({
        "Iteration": list(range(0, len(best_fitness_history))),
        "Best Fitness": best_fitness_history,
        "elapsed_time": elapsed_time
    })

    relay_details = []
    for i in range(D):
        I_pickup = CT[i] * PS_values[i]
        op_time = time_operation(TDS_values[i], CT[i] * PS_values[i], I_data[i])
        primary_times_mid = time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_mid[i])
        primary_times_far = time_operation(TDS_values[i], CT[i] * PS_values[i], I_data_far[i])
        relay_details.append({
            "Relay": i + 1,
            "TDS": TDS_values[i],
            "PS": PS_values[i],
            "I_pickup": I_pickup,
            "Primary Time Near": op_time,
            "Primary Time Mid": primary_times_mid,
            "Primary Time Far": primary_times_far
        })
    df_relays = pd.DataFrame(relay_details)

    backup_records = []
    primary_idx_count = {i: 0 for i in range(D)}
    for primary_idx, backup_idx in backup_pairs:
        backup_current = get_backup_current(primary_idx, primary_idx_count[primary_idx])
        primary_idx_count[primary_idx] += 1
        if backup_current is None:
            backup_records.append({
                "Primary Relay": primary_idx + 1,
                "Backup Relay": backup_idx + 1,
                "Backup Current": None,
                "Primary Time": None,
                "Backup Time": None,
                "Coordination Time": None,
                "CTI": CTI,
                "Status": "No backup current"
            })
            continue

        primary_time = time_operation(
            TDS_values[primary_idx],
            CT[primary_idx] * PS_values[primary_idx],
            I_data[primary_idx]
        )
        backup_time = time_operation(
            TDS_values[backup_idx],
            CT[backup_idx] * PS_values[backup_idx],
            backup_current
        )
        coordination_time = backup_time - primary_time
        status = "Success" if coordination_time >= CTI else "Failure"
        backup_records.append({
            "Primary Relay": primary_idx + 1,
            "Backup Relay": backup_idx + 1,
            "Backup Current": backup_current,
            "Primary Time": primary_time,
            "Backup Time": backup_time,
            "Coordination Time": coordination_time,
            "CTI": CTI,
            "Status": status
        })
    df_backup = pd.DataFrame(backup_records)

    initial_best_index = None
    initial_best_of = None
    initial_best_individual = None
    initial_match = None
    if initial_info is not None:
        initial_best_index = initial_info["Initial Best Index"] + 1
        initial_best_of = initial_info["Initial Best OF"]
        initial_best_individual = array_to_excel_string(initial_info["Initial Best Individual"])
        if cocsos_initial_best_of is not None:
            initial_match = compare_initial_best_with_cocsos(initial_best_of, cocsos_initial_best_of)

    df_summary = pd.DataFrame({
        "Algorithm": ["SOS"],
        "Run": [run],
        "Function": [function_name],
        "Seed": [seed],
        "Seed Source File": [seed_excel_path],
        "Dimension": [dim],
        "Bounds": [str(bounds)],
        "Pop Size": [pop_size],
        "Max Iter": [max_iter],
        "Initial Best Index": [initial_best_index],
        "Initial Best OF": [initial_best_of],
        "COCSOS Initial Best OF": [cocsos_initial_best_of],
        "Initial Best OF Match COCSOS": [initial_match],
        "Initial Best Individual": [initial_best_individual],
        "Elapsed Time (sec)": [elapsed_time],
        "Best Fitness": [best_fitness],
        "Best Solution": [array_to_excel_string(best_solution)]
    })

    seed_protocol_df = pd.DataFrame({
        "Algorithm": ["SOS"],
        "Run": [run],
        "Function": [function_name],
        "Seed": [seed],
        "Seed Source": ["Read from COCSOS Function_Seeds"],
        "Seed Source File": [seed_excel_path],
        "Dimension": [dim],
        "Bounds": [str(bounds)],
        "Pop Size": [pop_size],
        "Max Iter": [max_iter],
        "Random libraries reset": ["np.random.seed(seed) and random.seed(seed)"],
        "Reproducibility condition": ["SOS reads the same Run + Function seed from COCSOS before np.random.uniform(lb, ub, (pop_size, dim))."],
        "Fairness check": ["Initial Best OF and Initial_Quantized_Pop_OF should match the COCSOS initial random population stage."]
    })

    experiment_info_df = pd.DataFrame({
        "Item": [
            "Algorithm",
            "Seed protocol",
            "Random libraries reset",
            "Same bounds as COCSOS",
            "Initial population saved",
            "Initial objective value saved",
            "Fitness history iteration 0",
            "Important fairness note"
        ],
        "Value": [
            "SOS",
            "Each Run + Function pair uses the seed generated and recorded by COCSOS.",
            "np.random.seed(seed) and random.seed(seed)",
            "get_bounds_vectors() uses the same lb/ub vectors as the COCSOS code.",
            "Initial Random Population and Initial Quantized Population are exported.",
            "Initial Random OF is computed after quantize_solution for the random initial population.",
            "Iteration = 0 stores Initial Best OF before SOS iteration 1.",
            "SOS must not call any random function before creating the initial population."
        ]
    })

    with pd.ExcelWriter(filename) as writer:
        df_summary.to_excel(writer, sheet_name="Summary", index=False)
        seed_protocol_df.to_excel(writer, sheet_name="Seed_Protocol", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)
        df_fitness.to_excel(writer, sheet_name="Fitness History", index=False)
        df_relays.to_excel(writer, sheet_name="Relay Details", index=False)
        df_backup.to_excel(writer, sheet_name="Backup Coordination", index=False)

        if initial_info is not None:
            df_initial_random = build_initial_population_dataframe(
                initial_info,
                run=run,
                function_name=function_name,
                population_key="Initial Random Population"
            )
            df_initial_random.to_excel(writer, sheet_name="Initial_Random_Pop_OF", index=False)

            df_initial_quantized = build_initial_population_dataframe(
                initial_info,
                run=run,
                function_name=function_name,
                population_key="Initial Quantized Population"
            )
            df_initial_quantized.to_excel(writer, sheet_name="Initial_Quantized_Pop_OF", index=False)

    print(f"Results exported to {filename}")

# ------------------ Chạy SOS theo seed do COCSOS xuất ra ------------------
if __name__ == "__main__":
    bounds = (0.05, 3)
    pop_size = 100
    max_iter = 5000
    total_dim = 2 * D

    # File ALL_SUMMARY do COCSOS xuất ra. Đặt file này cùng thư mục với code SOS trước khi chạy.
    seed_excel_path = "COCSOS_OF3_110kV_TDS_newPS_VI_ALL_SUMMARY.xlsx"

    # Function phải giống đúng tên Function trong sheet Function_Seeds của COCSOS.
    function_name = "COCSOS_VI_110kV"

    seed_table = load_seed_table_from_cocsos(
        seed_excel_path=seed_excel_path,
        function_name=function_name
    )
    cocsos_initial_df = load_cocsos_initial_summary(
        seed_excel_path=seed_excel_path,
        function_name=function_name
    )

    num_runs = len(seed_table)
    print(f"Loaded {num_runs} seed(s) from {seed_excel_path}")

    all_summary_records = []

    for _, seed_row in seed_table.iterrows():
        run = int(seed_row["Run"])
        function_seed = get_run_seed(seed_table, run, function_name=function_name)

        cocsos_initial_best_of = None
        if not cocsos_initial_df.empty:
            matched = cocsos_initial_df[cocsos_initial_df["Run"] == run]
            if not matched.empty:
                cocsos_initial_best_of = float(matched.iloc[0]["COCSOS Initial Best OF"])

        print(f"\n======== SOS RUN {run} / {num_runs} | Seed = {function_seed} ========")
        best_solution, best_fitness, elapsed_time, history, initial_info = SOS(
            objective_function,
            bounds,
            total_dim,
            pop_size,
            max_iter,
            seed=function_seed
        )

        initial_match = compare_initial_best_with_cocsos(
            initial_info["Initial Best OF"],
            cocsos_initial_best_of
        ) if cocsos_initial_best_of is not None else None

        print("\nBest solution found:")
        print("TDS values:")
        print(best_solution[:D])
        print("PS values:")
        print(best_solution[D:2 * D])
        print(f"Initial best OF after random initialization: {initial_info['Initial Best OF']:.8f}")
        if cocsos_initial_best_of is not None:
            print(f"COCSOS initial best OF from summary: {cocsos_initial_best_of:.8f}")
            print(f"Initial best OF match COCSOS: {initial_match}")
        print(f"Best fitness: {best_fitness:.8f}")
        print(f"Elapsed time: {elapsed_time:.4f} sec")

        all_summary_records.append({
            "Algorithm": "SOS",
            "Run": run,
            "Function": function_name,
            "Seed": function_seed,
            "Seed Source File": seed_excel_path,
            "Dimension": total_dim,
            "Bounds": str(bounds),
            "Pop Size": pop_size,
            "Max Iter": max_iter,
            "Initial Best Index": initial_info["Initial Best Index"] + 1,
            "Initial Best OF": initial_info["Initial Best OF"],
            "COCSOS Initial Best OF": cocsos_initial_best_of,
            "Initial Best OF Match COCSOS": initial_match,
            "Initial Best Individual": array_to_excel_string(initial_info["Initial Best Individual"]),
            "Best Fitness": best_fitness,
            "Best Solution": array_to_excel_string(best_solution),
            "Elapsed Time (sec)": elapsed_time
        })

        filename = f"SOS_OF3_110kV_TDS_newPS_VI_seeded_run_{run}.xlsx"
        export_results_to_excel(
            best_solution,
            best_fitness,
            elapsed_time,
            history,
            filename,
            run=run,
            seed=function_seed,
            initial_info=initial_info,
            pop_size=pop_size,
            max_iter=max_iter,
            bounds=bounds,
            dim=total_dim,
            function_name=function_name,
            seed_excel_path=seed_excel_path,
            cocsos_initial_best_of=cocsos_initial_best_of
        )

    all_summary_df = pd.DataFrame(all_summary_records)

    function_seed_df = seed_table.copy()
    function_seed_df["Seed Source"] = "Read from COCSOS"
    function_seed_df["Seed Source File"] = seed_excel_path

    experiment_info_df = pd.DataFrame({
        "Item": [
            "Algorithm",
            "Number of independent runs",
            "Population size",
            "Maximum iterations",
            "Seed source",
            "Seed protocol",
            "Random libraries reset",
            "Initial population saved in each run file",
            "Initial objective value saved in each run file",
            "Fitness history iteration 0",
            "Reproducibility condition"
        ],
        "Value": [
            "SOS",
            int(num_runs),
            int(pop_size),
            int(max_iter),
            "Read from COCSOS Function_Seeds sheet",
            "Each SOS Run + Function pair uses the corresponding seed generated by COCSOS.",
            "np.random.seed(seed) and random.seed(seed)",
            "Initial_Random_Pop_OF and Initial_Quantized_Pop_OF",
            "Initial Random OF and Initial Best OF",
            "Iteration = 0 stores Initial Best OF before SOS iteration 1.",
            "SOS must read the same Function_Seeds sheet and use the same Run + Function seed before creating the initial population."
        ]
    })

    all_file_name = "SOS_OF3_110kV_TDS_newPS_VI_ALL_SUMMARY_seeded.xlsx"
    with pd.ExcelWriter(all_file_name) as writer:
        all_summary_df.to_excel(writer, sheet_name="All_Summary", index=False)
        function_seed_df.to_excel(writer, sheet_name="Function_Seeds", index=False)
        function_seed_df.to_excel(writer, sheet_name="Run_Function_Seeds", index=False)
        experiment_info_df.to_excel(writer, sheet_name="Experiment_Info", index=False)

    print(f"All SOS runs summary exported to {all_file_name}")
