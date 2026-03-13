import re
import numpy as np

# 1. 센서 로그 파일 읽기
with open("sensor_logs.txt", "r", encoding="utf-8") as f:
    raw_logs = f.read()

# 2. 정규표현식 패턴 설계 (6개 센서 캡처 그룹)
pattern = re.compile(
    r"\[LOG\]\[.+?\] "
    r"Temp: (\d+\.?\d*|nan)C, Press: (\d+\.?\d*|nan)Pa, Humid: (\d+\.?\d*|nan)%, "
    r"Volt: (\d+\.?\d*|nan)V, Flow: (\d+\.?\d*|nan) L/min, CO2: (\d+|nan) ppm"
)

# 3. 데이터 추출 (패턴에 맞지 않는 노이즈 라인은 자동 제거)
matches = pattern.findall(raw_logs)

# 4. NumPy 배열로 변환
COLS = ["Temp", "Press", "Humid", "Volt", "Flow", "CO2"]
data_array = np.array(matches, dtype=np.float32)

print(f"총 추출된 로그 수: {len(data_array)}행")
print(f"배열의 차원(Shape): {data_array.shape}")
print(f"상위 5개 데이터:\n{data_array[:5]}")

# 1. 정상 범위 정의 (각 센서별 [최솟값, 최댓값])
NORMAL_RANGES = {
    "Temp":  (5.0,  50.0),
    "Press": (90.0, 115.0),
    "Humid": (10.0, 95.0),
    "Volt":  (8.0,  17.0),
    "Flow":  (1.0,  22.0),
    "CO2":   (200,  1200),
}

# 2. 이상치 마스크 생성
outlier_mask = np.zeros(len(data_array), dtype=bool)
# 2-1. NaN이 하나라도 있는 행 (연결 끊김)
outlier_mask |= np.any(np.isnan(data_array), axis=1)
# 2-2. 정상 범위를 벗어난 행
for i, col in enumerate(COLS):
    lo, hi = NORMAL_RANGES[col]
    outlier_mask |= (data_array[:, i] < lo) | (data_array[:, i] > hi)

normal_data  = data_array[~outlier_mask]
outlier_data = data_array[outlier_mask]

print(f"\n정상 데이터: {len(normal_data)}행")
print(f"이상치 데이터: {len(outlier_data)}행")

# 3. 정상 데이터 통계 분석
means = np.mean(normal_data, axis=0)
stds  = np.std(normal_data, axis=0)

print(f"\n📊 정상 데이터 분석 결과 ({len(normal_data)}건)")
for col, mean, std in zip(COLS, means, stds):
    print(f"  {col:5s} 평균: {mean:8.2f}  (표준편차: {std:.2f})")

# 4. Min-Max 정규화
# 정상 데이터에서만 min/max를 계산해 이상치의 영향을 배제
d_min = np.min(normal_data, axis=0)  # 각 열의 최솟값, shape: (6,)
d_max = np.max(normal_data, axis=0)  # 각 열의 최댓값, shape: (6,)

# (현재값 - 최솟값) / (최댓값 - 최솟값) → 모든 값이 [0.0, 1.0] 범위로 변환
normalized_data = (normal_data - d_min) / (d_max - d_min)

print(f"\n정규화 완료 (Min-Max Scaled) --- shape: {normalized_data.shape}")
print(f"각 열의 최솟값(정규화 후): {normalized_data.min(axis=0)}")
print(f"각 열의 최댓값(정규화 후): {normalized_data.max(axis=0)}")
print(f"상위 5개 정규화 데이터:\n{normalized_data[:5]}")

# 5. 결과 파일 저장
# 5-1. NumPy 전용 바이너리 저장 (.npy)
# 데이터 타입(float32), 모양(N×6) 정보를 그대로 유지하며 저장됩니다.
np.save('refined_sensor_data.npy', normalized_data)

# 5-2. 텍스트 형식 저장 (.csv)
# 외부 협력사나 엑셀에서 열어볼 수 있도록 쉼표로 구분하여 저장합니다.
np.savetxt('final_report.csv', normalized_data, fmt='%.4f', delimiter=',',
           header=','.join(COLS), comments='')

print("\n[저장 완료]")
print("- 바이너리 파일: refined_sensor_data.npy")
print("- 보고서 파일:   final_report.csv")
