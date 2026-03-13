import numpy as np


def clean_sensor_data(sensor_matrix, valid_ranges):
    """결측/이상치를 제거한 센서 데이터와 요약을 반환한다."""
    # TODO: 요구 사항을 만족하도록 구현

    rows, cols = sensor_matrix.shape 

    remove_mask = np.zeros(rows, dtype=bool)

    remove_mask |= np.isnan(sensor_matrix).any(axis=1)

    for col, (min_v, max_v) in enumerate(valid_ranges):
        out_of_range = (sensor_matrix[:,col] < min_v) | (sensor_matrix[:,col] > max_v)
        remove_mask |= out_of_range

    remove_idx = np.where(remove_mask)[0]

    cleaned = sensor_matrix[~remove_mask]

    if cleaned.shape[0] == 0:
        column_mean = np.array([])
    else:
        column_mean = cleaned.mean(axis=0)
    
    return {
        "cleaned": cleaned,
        "removed_idx": remove_idx,
        "column_mean": column_mean
    }

def main():
    sensor = np.array([
        [20.0, 110.0, 45.0],
        [np.nan, 108.0, 50.0],
        [55.0, 109.0, 47.0],
        [23.0, 111.0, 44.0],
    ])
    ranges = [(5.0, 50.0), (90.0, 115.0), (10.0, 95.0)]
    result = clean_sensor_data(sensor, ranges)
    for k, v in result.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()