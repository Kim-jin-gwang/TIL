import numpy as np


def summarize_class_scores(scores):
    """반 점수를 간단 요약해 반환한다."""
    # TODO: 과제 요구 사항을 만족하도록 구현

    if scores.size == 0:
        return{
            'row_mean': np.array([], dtype=float), 
            'class_mean': float(0.0), 
            'pass_flag': np.array([],dtype=int)
        }

    row_mean = scores.mean(axis=1)
    class_mean = scores.mean()

    pass_flag = (row_mean > class_mean).astype(int)

    return{
            'row_mean': row_mean, 
            'class_mean': float(class_mean), 
            'pass_flag': pass_flag
        }


def main():
    scores = np.array([
        [80, 90, 100],
        [70, 75, 65],
        [95, 88, 92],
    ], dtype=float)
    result = summarize_class_scores(scores)
    print(result)


if __name__ == '__main__':
    main()
