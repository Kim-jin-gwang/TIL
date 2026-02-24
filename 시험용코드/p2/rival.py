
import socket
import math

NICKNAME = '대전6_백승효_박동규'
HOST = '127.0.0.1'
PORT = 1447
CODE_SEND = 9901
CODE_REQUEST = 9902
SIGNAL_ORDER = 9908
SIGNAL_CLOSE = 9909

TABLE_WIDTH = 254
TABLE_HEIGHT = 127
HOLES = [[0, 0], [127, 0], [254, 0], [0, 127], [127, 127], [254, 127]]


def get_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


sock = socket.socket()
sock.connect((HOST, PORT))
send_data = '%d/%s' % (CODE_SEND, NICKNAME)
sock.send(send_data.encode('utf-8'))

balls = [[0, 0] for i in range(6)]
order = 0

while True:
    recv_data = (sock.recv(1024)).decode()
    if not recv_data: break

    split_data = recv_data.split('/')
    idx = 0
    try:
        for i in range(6):
            for j in range(2):
                balls[i][j] = float(split_data[idx])
                idx += 1
    except:
        sock.send(('%d/%s' % (CODE_REQUEST, NICKNAME)).encode('utf-8'))
        continue

    if balls[0][0] == SIGNAL_ORDER:
        order = int(balls[0][1])
        continue
    elif balls[0][0] == SIGNAL_CLOSE:
        break

    white_x, white_y = balls[0]
    my_targets = [1, 3, 5] if order == 1 else [2, 4, 5]

    # 1. 8번 공(5번 인덱스) 제외 다른 공 유무 확인
    others_remain = any(balls[t][0] != -1 for t in my_targets if t != 5)

    best_target_idx = -1
    best_hole = HOLES[0]
    min_diff = float('inf')

    # 2. 최적의 공과 홀 조합 탐색
    for t_idx in my_targets:
        if balls[t_idx][0] == -1: continue
        if t_idx == 5 and others_remain: continue  # 8번 공은 나중에

        target_x, target_y = balls[t_idx]

        for hole in HOLES:
            # 홀-목적구-흰공의 각도가 180도에 가까울수록 넣기 쉬움
            angle_to_hole = math.atan2(hole[1] - target_y, hole[0] - target_x)
            angle_to_white = math.atan2(white_y - target_y, white_x - target_x)
            diff = abs(math.degrees(angle_to_hole - angle_to_white))

            # 굴절각이 너무 크면(직선이 아니면) 패스
            if diff < min_diff:
                min_diff = diff
                best_target_idx = t_idx
                best_hole = hole

    if best_target_idx == -1: continue  # 칠 공이 없음

    target_x, target_y = balls[best_target_idx]

    # 3. 충돌 지점(Virtual Ball) 계산
    # 목적구에서 홀 반대 방향으로 공 지름(약 5.73)만큼 떨어진 지점
    angle_hole = math.atan2(best_hole[1] - target_y, best_hole[0] - target_x)
    r = 5.6  # 공 지름보다 살짝 작게 보정 (5.73 -> 5.6)
    v_target_x = target_x - math.cos(angle_hole) * r
    v_target_y = target_y - math.sin(angle_hole) * r

    # 4. 최종 각도(상단 0도 기준 시계방향)
    dx = v_target_x - white_x
    dy = v_target_y - white_y
    angle = math.degrees(math.atan2(dx, dy))
    if angle < 0: angle += 360

    # 5. 거리 기반 파워 조절
    dist_v = get_dist([white_x, white_y], [v_target_x, v_target_y])
    dist_h = get_dist([target_x, target_y], best_hole)
    power = (dist_v * 0.4) + (dist_h * 0.2) + 20
    power = min(100, max(35, power))

    # 전송
    merged_data = '%f/%f/' % (angle, power)
    sock.send(merged_data.encode('utf-8'))
    print(f"Target: {best_target_idx} | Hole: {best_hole} | Power: {power:.1f}")

sock.close()