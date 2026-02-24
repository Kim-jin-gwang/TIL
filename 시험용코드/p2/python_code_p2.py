import socket
import time
import math

# 닉네임을 사용자에 맞게 변경해 주세요.
NICKNAME = 'JinGwang'

# 일타싸피 프로그램을 로컬에서 실행할 경우 변경하지 않습니다.
HOST = '127.0.0.1'

# 일타싸피 프로그램과 통신할 때 사용하는 코드값으로 변경하지 않습니다.
PORT = 1447
CODE_SEND = 9901
CODE_REQUEST = 9902
SIGNAL_ORDER = 9908
SIGNAL_CLOSE = 9909


# 게임 환경에 대한 상수입니다.
TABLE_WIDTH = 254
TABLE_HEIGHT = 127
NUMBER_OF_BALLS = 6
HOLES = [[0, 0], [127, 0], [254, 0], [0, 127], [127, 127], [254, 127]]

order = 0
balls = [[0, 0] for i in range(NUMBER_OF_BALLS)]

sock = socket.socket()
print('Trying to Connect: %s:%d' % (HOST, PORT))
sock.connect((HOST, PORT))
print('Connected: %s:%d' % (HOST, PORT))

send_data = '%d/%s' % (CODE_SEND, NICKNAME)
sock.send(send_data.encode('utf-8'))
print('Ready to play!\n--------------------')


while True:

    # Receive Data
    recv_data = (sock.recv(1024)).decode()
    print('Data Received: %s' % recv_data)

    # Read Game Data
    split_data = recv_data.split('/')
    idx = 0
    try:
        for i in range(NUMBER_OF_BALLS):
            for j in range(2):
                balls[i][j] = float(split_data[idx])
                idx += 1
    except:
        send_data = '%d/%s' % (CODE_REQUEST, NICKNAME)
        print("Received Data has been currupted, Resend Requested.")
        continue

    # Check Signal for Player Order or Close Connection
    if balls[0][0] == SIGNAL_ORDER:
        order = int(balls[0][1])
        print('\n* You will be the %s player. *\n' % ('first' if order == 1 else 'second'))
        continue
    elif balls[0][0] == SIGNAL_CLOSE:
        break

    # Show Balls' Position
    print('====== Arrays ======')
    for i in range(NUMBER_OF_BALLS):
        print('Ball %d: %f, %f' % (i, balls[i][0], balls[i][1]))
    print('====================')

    angle = 0.0
    power = 0.0

    ##############################
    # 이 위는 일타싸피와 통신하여 데이터를 주고 받기 위해 작성된 부분이므로 수정하면 안됩니다.
    #
    # 모든 수신값은 변수, 배열에서 확인할 수 있습니다.
    #   - order: 1인 경우 선공, 2인 경우 후공을 의미
    #   - balls[][]: 일타싸피 정보를 수신해서 각 공의 좌표를 배열로 저장
    #     예) balls[0][0]: 흰 공의 X좌표
    #         balls[0][1]: 흰 공의 Y좌표
    #         balls[1][0]: 1번 공의 X좌표
    #         balls[4][0]: 4번 공의 X좌표
    #         balls[5][0]: 마지막 번호(8번) 공의 X좌표

    # 여기서부터 코드를 작성하세요.
    # 아래에 있는 것은 샘플로 작성된 코드이므로 자유롭게 변경할 수 있습니다.

    # ===================== 여기부터 수정 =====================

    # 공의 지름 및 기본 설정
    ball_diameter = 5.73
    target_indexes = [1, 3, 5] if order == 1 else [2, 4, 5]
    
    target_ball_idx = -1
    for idx in target_indexes:
        if balls[idx][0] >= 0:
            target_ball_idx = idx
            break

    def is_blocked(start, end, obstacles):
        """두 지점 사이를 다른 공이 가로막고 있는지 확인하는 함수"""
        for obs_idx in obstacles:
            if balls[obs_idx][0] < 0: continue # 이미 들어간 공 제외
            
            # 장애물 공의 좌표
            ox, oy = balls[obs_idx][0], balls[obs_idx][1]
            # 선분(start-end)과 점(ox, oy) 사이의 최단 거리 계산
            dx, dy = end[0] - start[0], end[1] - start[1]
            if dx == 0 and dy == 0: continue
            
            t = ((ox - start[0]) * dx + (oy - start[1]) * dy) / (dx**2 + dy**2)
            t = max(0, min(1, t)) # 선분 범위로 한정
            
            closest_x = start[0] + t * dx
            closest_y = start[1] + t * dy
            dist = math.sqrt((ox - closest_x)**2 + (oy - closest_y)**2)
            
            if dist < ball_diameter * 0.9: # 공 지름보다 가까우면 충돌 위험
                return True
        return False

    if target_ball_idx != -1:
        white_pos = [balls[0][0], balls[0][1]]
        target_pos = [balls[target_ball_idx][0], balls[target_ball_idx][1]]
        
        # 내 목적구가 아닌 나머지 공들(장애물) 목록
        others = [i for i in range(1, 6) if i != target_ball_idx]

        found_path = False
        min_dist = float('inf')

        for hole in HOLES:
            dx_h, dy_h = hole[0] - target_pos[0], hole[1] - target_pos[1]
            d_h = math.sqrt(dx_h**2 + dy_h**2)
            
            # 목적구를 홀로 보내기 위한 접점(CP)
            cp_x = target_pos[0] - (dx_h / d_h) * ball_diameter
            cp_y = target_pos[1] - (dy_h / d_h) * ball_diameter
            cp_pos = [cp_x, cp_y]

            # 1. 직접 타격 시도
            if not is_blocked(white_pos, cp_pos, others):
                rad = math.atan2(cp_y - white_pos[1], cp_x - white_pos[0])
                angle = (90 - math.degrees(rad)) % 360
                power = min(100, max(45, d_h * 0.6 + math.sqrt((cp_x-white_pos[0])**2 + (cp_y-white_pos[1])**2) * 0.5))
                found_path = True
                break # 직접 칠 수 있으면 바로 결정

        # 2. 직접 타격이 불가능할 경우 쿠션(1쿠션) 계산
        if not found_path:
            # 4면 벽에 대한 가상 타겟(Virtual CP) 생성
            # 각 벽면: 0(좌), 1(하), 2(우), 3(상)
            virtual_targets = [
                [-cp_pos[0], cp_pos[1]],                   # Left
                [cp_pos[0], -cp_pos[1]],                   # Bottom
                [2 * TABLE_WIDTH - cp_pos[0], cp_pos[1]],  # Right
                [cp_pos[0], 2 * TABLE_HEIGHT - cp_pos[1]]  # Top
            ]
            
            for vt in virtual_targets:
                # 가상 타겟 방향으로 쳤을 때 실제 벽에 닿는 점(Impact Point) 계산 필요하나, 
                # 단순화를 위해 가상 타겟 방향의 각도만 사용
                rad = math.atan2(vt[1] - white_pos[1], vt[0] - white_pos[0])
                # 쿠션은 힘 손실이 크므로 파워를 약 1.5배 보정
                angle = (90 - math.degrees(rad)) % 360
                power = 85 
                found_path = True
                break # 첫 번째 유효한 쿠션 경로 선택

    # ===================== 여기까지 =====================


    # 주어진 데이터(공의 좌표)를 활용하여 두 개의 값을 최종 결정하고 나면,
    # 나머지 코드에서 일타싸피로 값을 보내 자동으로 플레이를 진행하게 합니다.
    #   - angle: 흰 공을 때려서 보낼 방향(각도)
    #   - power: 흰 공을 때릴 힘의 세기
    # 
    # 이 때 주의할 점은 power는 100을 초과할 수 없으며,
    # power = 0인 경우 힘이 제로(0)이므로 아무런 반응이 나타나지 않습니다.
    #
    # 아래는 일타싸피와 통신하는 나머지 부분이므로 수정하면 안됩니다.
    ##############################

    merged_data = '%f/%f/' % (angle, power)
    sock.send(merged_data.encode('utf-8'))
    print('Data Sent: %s' % merged_data)

sock.close()
print('Connection Closed.\n--------------------')