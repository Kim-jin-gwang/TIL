def hanoi(n, source, auxiliary, target):
    """
    n개의 원반을 source 기둥에서 target 기둥으로 옮깁니다.

    Args:
        n (int): 이동할 원반의 개수
        source (str): 시작 기둥 (예: 'A')
        auxiliary (str): 보조 기둥 (예: 'B')
        target (str): 목표 기둥 (예: 'C')
    """
    if n > 0:
        # === 1단계: 가장 큰 원반을 옮기기 위한 준비 ===
        # 목표: 맨 아래 있는 가장 큰 원반(n번)을 시작(source)에서 목표(target)로 옮기고 싶다.
        # 문제: 그런데 n-1개의 작은 원반들이 위에서 길을 막고 있다.
        # 해결책: 이 n-1개의 방해물들을 전부 보조(auxiliary) 기둥으로 잠시 치워두자.
        #
        # 이 '치우는' 작업 역시 '하노이의 탑' 문제와 똑같다! (단, 원반 개수만 n-1개)
        # 그래서 hanoi 함수를 다시 호출(재귀)해서 이 문제를 풀게 한다.
        #
        # hanoi(n-1, source, target, auxiliary)
        # -> "n-1개 원반을 source에서 auxiliary로 옮겨줘. target은 잠시 보조 기둥으로 사용해."
        hanoi(n - 1, source, target, auxiliary)

        # === 2단계: 원래 목표였던 가장 큰 원반 옮기기 ===
        # 이제 길을 막던 원반들이 모두 보조 기둥으로 치워졌다.
        # 드디어 원래 목표였던 n번 원반을 시작(source)에서 목표(target)로 옮길 수 있다.
        #
        # [중요!] 여기서 'n'은 현재 이 함수가 맡은 원반들 중 가장 큰 원반을 의미합니다.
        # 예를 들어, hanoi(1, ...)가 호출되면, 이때의 n은 1이므로 "원반 1"이 출력됩니다.
        # 즉, 재귀 호출이 깊어질수록 더 작은 '가장 큰 원반'을 옮기게 됩니다.
        print(f"원반 {n}을(를) {source}에서 {target}으로 이동")

        # === 3단계: 마무리 작업 ===
        # 가장 큰 원반을 성공적으로 옮겼다.
        # 이제 보조(auxiliary) 기둥에 쌓아뒀던 n-1개의 원반들을
        # 다시 목표(target) 기둥 위로 가져와야 모든 작업이 끝난다.
        #
        # 이 '다시 가져오는' 작업 또한 '하노이의 탑' 문제와 같다.
        # hanoi 함수를 다시 호출해서 해결하자.
        #
        # 현재 진행 상황이 2인 경우
        # source: A
        # auxiliary: C
        # target: B
        # hanoi(n-1, auxiliary, source, target)
        # -> "n-1개 원반을 auxiliary에서 target으로 옮겨줘. source는 잠시 보조 기둥으로 사용해."
        hanoi(n - 1, auxiliary, source, target)


# --- 실행 예시 ---
# 3개의 원반을 'A' 기둥에서 'C' 기둥으로 옮기기 ('B' 기둥을 보조로 사용)
number_of_disks = 3
hanoi(number_of_disks, 'A', 'B', 'C')