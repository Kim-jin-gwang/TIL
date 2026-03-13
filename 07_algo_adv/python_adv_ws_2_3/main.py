import numpy as np


def summarize_scores(score_matrix):
    """성적 배열을 다중 요약해 딕셔너리로 반환한다."""
    if score_matrix.size == 0:
        raise ValueError
    
    student_mean = np.mean(score_matrix, axis = 1)
    subject_mean = np.mean(score_matrix, axis = 0)

    top_student_idx = np.argmax(student_mean)
    level_label = np.where(
        student_mean >= 85,
        'HIGH',
        np.where(student_mean >= 70, 'MID', 'LOW')
    )

    return {
        "student_mean" : student_mean,
        "subject_mean" : subject_mean,
        "top_student_idx" : top_student_idx,
        "level_label" : level_label,
    }

def main():
    scores = np.array([
        [80, 90, 100],    # 열 = 학생, 행 = 과목
        [72, 68, 74],
        [95, 88, 91],
    ], dtype=float)
    result = summarize_scores(scores)
    for k, v in result.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()
