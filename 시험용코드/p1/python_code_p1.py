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


    # ===================== 핵심 로직 시작 =====================

    # 1. 내 차례에 맞는 목적구 번호 설정
    # 선공(order=1): 1, 3, 8번 / 후공(order=2): 2, 4, 8번
    my_balls = [1, 3] if order == 1 else [2, 4]
    last_ball = 5 # 8번 공
    
    target_ball_idx = -1
    best_angle = 0
    best_power = 0
    min_total_dist = float('inf')
    ball_diameter = 5.73

    white_x, white_y = balls[0][0], balls[0][1]

    # 목적구 후보 리스트 생성 (8번 제외 남은 공들)
    remained_balls = [idx for idx in my_balls if balls[idx][0] >= 0]

    # 만약 내 공을 다 넣었다면 8번 공을 타겟으로 설정
    if not remained_balls:
        if balls[last_ball][0] >= 0:
            remained_balls = [last_ball]
    
    # 2. 모든 가능한 공과 모든 홀의 조합을 확인하여 최단 경로 탐색
    for b_idx in remained_balls:
        target_x, target_y = balls[b_idx][0], balls[b_idx][1]

        for hole in HOLES:
            hole_x, hole_y = hole[0], hole[1]

            # 목적구에서 홀까지의 거리 및 방향
            dx_hole = hole_x - target_x
            dy_hole = hole_y - target_y
            dist_hole = math.sqrt(dx_hole**2 + dy_hole**2)

            # 접점(Contact Point) 계산: 목적구 뒤편으로 공 지름만큼 떨어진 위치
            contact_x = target_x - (dx_hole / dist_hole) * ball_diameter
            contact_y = target_y - (dy_hole / dist_hole) * ball_diameter

            # 흰 공에서 접점까지의 거리
            dx_contact = contact_x - white_x
            dy_contact = contact_y - white_y
            dist_contact = math.sqrt(dx_contact**2 + dy_contact**2)

            # 3. 경로 유효성 및 최단 거리 검사
            # 벡터 내적을 활용해 흰 공이 목적구를 뒤에서 앞으로 밀 수 있는 각도인지 확인
            dot_product = dx_contact * dx_hole + dy_contact * dy_hole
            
            if dot_product > 0: # 유효한 각도(순방향)일 때
                total_dist = dist_contact + dist_hole
                
                # 전체 경로(흰공->접점->홀)가 가장 짧은 조합 선택
                if total_dist < min_total_dist:
                    min_total_dist = total_dist
                    target_ball_idx = b_idx
                    
                    # 각도 계산 (라디안 -> 도)
                    radian = math.atan2(dy_contact, dx_contact)
                    best_angle = math.degrees(radian)
                    
                    # 거리 기반 파워 조절 (상황에 맞게 0.5~0.8 사이 계수 조정 가능)
                    best_power = min(100, max(45, total_dist * 0.6))

    # 최종 각도 변환 (일타싸피 시스템: 북쪽 0도 기준 시계방향)
    if target_ball_idx != -1:
        angle = (90 - best_angle) % 360
        power = best_power
    else:
        # 타겟을 못 찾은 경우(비상상황) 앞을 향해 약하게 샷
        angle = 0
        power = 10

    # ===================== 핵심 로직 끝 =====================

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