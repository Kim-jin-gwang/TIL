import numpy as np


def center_rows(matrix):
    """행 평균을 제거한 2차원 배열을 반환한다."""

    if matrix.ndim != 2:
        raise ValueError("Input must be a 2D array")
    
    if matrix.size == 0:
        return matrix.copy()
    
    row_means = matrix.mean(axis = 1)

    # [[20],[6]] -> [[20,20,20],[6,6,6]]
    centered = matrix - row_means[:,None]  # shape(2, ) 

    return centered


def main():
    sample = np.array([
        [10.0, 20.0, 30.0],
        [3.0, 6.0, 9.0],
    ])
    result = center_rows(sample)
    print(result)
    print('shape:', result.shape)
    print('row means:', result.mean(axis=1))


if __name__ == '__main__':
    main()
