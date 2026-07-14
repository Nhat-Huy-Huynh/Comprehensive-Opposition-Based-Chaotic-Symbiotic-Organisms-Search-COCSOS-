import time
import numpy as np

# Đo thời gian T0 theo tiêu chuẩn CEC2017
def compute_T0():
    start_time = time.time()  # Bắt đầu đo thời gian
    x = 0.55
    
    for i in range(1, 1000001):  # Lặp 1 triệu lần
        x = x + x
        x = x / 2
        x = x * x
        x = np.sqrt(x)
        x = np.log(x)
        x = np.exp(x)
        x = x / (x + 2)
    
    end_time = time.time()  # Kết thúc đo thời gian
    T0 = end_time - start_time
    return T0

# Chạy tính toán và in kết quả
T0 = compute_T0()
print(f"T0 (benchmark reference time) = {T0:.6f} seconds")
