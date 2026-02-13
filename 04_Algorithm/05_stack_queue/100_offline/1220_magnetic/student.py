from collections import deque

def countMaterials(ar):
    # 순차적으로 탐색하면서 자성체를 구합니다.
    cur_materials = []

    # 1. '1'다음으로 '2'가 나와야 하나의 자성체를 구성할 수 있습니다.
    # 2. 이때, '12212' 와 같이 연속으로 나와서 하나의 자성체를 구성하는 경우가 있습니다. 이는 idx를 추적하면 될거 같습니다.
    stack = deque()
    for idx in range(len(ar)):
        if ar[idx] == '1':
            # N극은 아래로 향합니다. '2'를 만나기 전까지 스택에 넣어집니다. idx도 기록해서 최종 위치를 추적해서 변형시킬 준비합니다.
            stack.append([1, idx])
        if ar[idx] == '2':
            # '1'이 나온적 없으면 넘어갑니다.
            if len(stack) == 0 and len(cur_materials) == 0:
                continue

            # 기다리고 있는 '1'은 안나왔지만 자성체를 만든적이 있다면 바로 위에 붙입니다.
            elif len(stack) == 0 and len(cur_materials) >= 1:
                cur_materials[-1][1] += 1

            # 현재 대기중인 모든 '1'이 있다면 자성체를 만듭니다.
            elif len(stack) >= 1:
                _, last_1_idx = stack.pop()
                # 최종 위치 추적
                # 2----7 -> --45--
                move_idx = (idx - last_1_idx + 1) // 2  # 4

                last_1_idx = last_1_idx + move_idx
                last_2_idx = idx - move_idx
                if len(cur_materials) >= 1:
                    # 최종적으로 만든 자성체의 '1'이 이전에 만든 자성체의 '2'와 붙어있다면? 통합시킵니다.
                    if cur_materials[-1][1] - last_1_idx == 1:
                        cur_materials[-1][1] = last_2_idx
                    else:
                        # 아니면 자성체 하나 만들었다고 추가시킵니다.
                        cur_materials.append([last_1_idx, last_2_idx])
                else:
                    # 이전에 만든 자성체가 없으면 그냥
                    cur_materials.append([last_1_idx, last_2_idx])

                # 지금까지 나온적 있는 '1'들도 방금 만들어진 최종 자성체에 붙입니다.
                cur_materials[-1][0] += len(stack)
                stack = deque()

    return len(cur_materials)


for tc in range(1, 11):
    N = int(input())
    arr = [str(input()).split(' ') for _ in range(N)]

    # 책상의 위는 N극, 아래는 S극
    # 1은 N극, 2는 S극

    # 1. 세로 배열을 구합니다.
    materials = 0
    trans_arr = list(zip(*arr))

    # 2. 각 세로 배열을 순차적으로 탐색하면서 자성체를 구합니다.
    for tar in trans_arr:
        materials += countMaterials(tar)

    print(f'#{tc} {materials}')