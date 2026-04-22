import sys
import socket
from collections import deque

##############################
# 메인 프로그램 통신 설정
##############################
HOST = '127.0.0.1'
PORT = 8747
ARGS = sys.argv[1] if len(sys.argv) > 1 else ''
sock = socket.socket()

def init(nickname):
    try:
        sock.connect((HOST, PORT))
        init_command = f'INIT {nickname}'
        return submit(init_command)
    except Exception as e:
        print(f'[ERROR] Connection failed: {e}')

def submit(string_to_send):
    try:
        send_data = ARGS + string_to_send + ' '
        sock.send(send_data.encode('utf-8'))
        return receive()
    except:
        return None

def receive():
    try:
        game_data = (sock.recv(1024)).decode()
        if game_data and game_data[0].isdigit() and int(game_data[0]) > 0:
            return game_data
        close()
    except:
        return None

def close():
    try:
        if sock: sock.close()
    except:
        pass

##############################
# 데이터 파싱 및 전역 변수
##############################
map_data = [[]]
my_allies = {}
enemies = {}
codes = []

def parse_data(game_data):
    game_data_rows = game_data.split('\n')
    header = game_data_rows[0].split(' ')
    h, w, n_a, n_e, n_c = map(int, header[:5])
    
    map_data.clear()
    map_data.extend([game_data_rows[1+i].split(' ') for i in range(h)])
    
    idx = 1 + h
    my_allies.clear()
    for i in range(idx, idx + n_a):
        row = game_data_rows[i].split(' ')
        my_allies[row[0]] = row[1:]
    
    idx += n_a
    enemies.clear()
    for i in range(idx, idx + n_e):
        row = game_data_rows[i].split(' ')
        enemies[row[0]] = row[1:]
        
    idx += n_e
    codes.clear()
    codes.extend([game_data_rows[i] for i in range(idx, idx + n_c)])

##############################
# 전략 상수 및 유틸리티
##############################
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)] # R, D, L, U
MOVE_CMDS = ["R A", "D A", "L A", "U A"]
FIRE_CMDS = ["R F", "D F", "L F", "U F"]
MEGA_FIRE_CMDS = ["R F M", "D F M", "L F M", "U F M"]

# 이동 불가: 벽, 물, 덤불, 아군 탱크(팀배틀 충돌방지), 적 탱크/포탑(직접 통과 불가)
IMPASSABLE = {'R', 'W', 'T', 'X', 'E1', 'E2', 'E3', 'M1', 'M2', 'M3', 'F'}
BUSH_TILES = {'S'} # 은폐 가능한 모래/숲 지형

def get_ammo():
    if 'M' in my_allies:
        v = my_allies['M']
        return int(v[2]), int(v[3])
    return 0, 0

def find_pos(symbol):
    for r in range(len(map_data)):
        for c in range(len(map_data[0])):
            if map_data[r][c] == symbol: return (r, c)
    return None

##############################
# 기동 타격대 핵심 알고리즘
##############################

def get_weighted_distance(r, c, nr, nc):
    # 숲(S) 지형을 지나갈 때는 가중치를 낮게 주어 우선 선택하게 함
    return 1 if map_data[nr][nc] in BUSH_TILES else 2

def bfs_flanking(start, targets):
    """은신처(숲)를 선호하며 적의 시야를 피하는 우회 경로 탐색"""
    if not start or not targets: return []
    
    rows, cols = len(map_data), len(map_data[0])
    queue = [(0, start, [])] # (cost, position, path)
    visited = {start: 0}
    
    import heapq
    heapq.heapify(queue)

    while queue:
        cost, (r, c), path = heapq.heappop(queue)
        
        if (r, c) in targets: return path
        
        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and map_data[nr][nc] not in IMPASSABLE:
                new_cost = cost + get_weighted_distance(r, c, nr, nc)
                if nr == start[0] or nc == start[1]: # 직선 평지 노출 시 패널티
                    new_cost += 1
                
                if (nr, nc) not in visited or new_cost < visited[(nr, nc)]:
                    visited[(nr, nc)] = new_cost
                    heapq.heappush(queue, (new_cost, (nr, nc), path + [MOVE_CMDS[d]]))
    return []

def can_shoot_target(my_pos, target_pos, n_bomb, m_bomb):
    """아군 오사 방지 로직이 포함된 사격 판별"""
    r, c = my_pos
    for d, (dr, dc) in enumerate(DIRS):
        for step in range(1, 4):
            fr, fc = r + dr*step, c + dc*step
            if not (0 <= fr < len(map_data) and 0 <= fc < len(map_data[0])): break
            cell = map_data[fr][fc]
            if cell == 'R': break
            if cell in {'M1', 'M2', 'M3'}: break # 아군 보호
            
            if (fr, fc) == target_pos:
                if m_bomb > 0: return MEGA_FIRE_CMDS[d]
                if n_bomb > 0: return FIRE_CMDS[d]
    return None

def get_best_targets():
    """체력 낮은 적 및 배후를 노리기 위한 타겟 리스트"""
    res = []
    for key in ['E1', 'E2', 'E3', 'X']:
        pos = find_pos(key)
        if pos:
            hp = int(enemies[key][0]) if key in enemies else 9999
            # 포탑(X)은 탱크보다 우선순위를 낮게 둠 (기동 타격대 역할)
            priority = hp if key != 'X' else hp + 5000
            res.append((priority, pos, key))
    res.sort()
    return res

##############################
# 메인 루프
##############################
NICKNAME = '대전6_기동타격대'
game_data = init(NICKNAME)
parse_data(game_data)

actions = []
needs_supply = True
MEGA_TARGET = 2 # 포탄을 2발 모을 때까지 보급에 집중

while game_data:
    n_bomb, m_bomb = get_ammo()
    my_pos = find_pos('M')
    
    if not my_pos:
        game_data = submit('S')
        if game_data: parse_data(game_data)
        continue

    # 1. 상태 업데이트 (Hysteresis)
    if needs_supply and m_bomb >= MEGA_TARGET:
        needs_supply = False
        actions = []
    elif not needs_supply and m_bomb == 0 and n_bomb == 0:
        needs_supply = True
        actions = []

    output = None
    targets = get_best_targets()

    # 2. 공통: 사거리 내 적 발견 시 즉시 기습 (기회주의적 공격)
    for _, t_pos, t_key in targets:
        cmd = can_shoot_target(my_pos, t_pos, n_bomb, m_bomb)
        if cmd:
            output = cmd
            actions = [] # 사격 후 재위치 선정을 위해 초기화
            break

    # 3. 모드별 행동
    if not output:
        # 보급 모드
        if needs_supply:
            # 보급소 인접 시 암호 해독
            is_adj = False
            for dr, dc in DIRS:
                nr, nc = my_pos[0]+dr, my_pos[1]+dc
                if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]) and map_data[nr][nc] == 'F':
                    is_adj = True; break
            
            if is_adj and codes:
                code = codes[0].strip()
                decoded = "".join([chr((ord(c.upper()) - ord('A') + 9) % 26 + ord('A')) if c.isalpha() else c for c in code])
                output = f'G {decoded}'
            elif not actions:
                # 보급지 주변의 빈 공간 탐색
                f_pos = find_pos('F')
                if f_pos:
                    spots = []
                    for dr, dc in DIRS:
                        nr, nc = f_pos[0]+dr, f_pos[1]+dc
                        if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]) and map_data[nr][nc] not in IMPASSABLE:
                            spots.append((nr, nc))
                    actions = bfs_flanking(my_pos, spots)
        
        # 전투 모드 (Flanker)
        else:
            if not actions and targets:
                # 적의 사거리 밖(측면) 사격 지점 찾기
                _, t_pos, _ = targets[0]
                shoot_spots = []
                for d, (dr, dc) in enumerate(DIRS):
                    for s in range(1, 4):
                        sr, sc = t_pos[0]+dr*s, t_pos[1]+dc*s
                        if 0 <= sr < len(map_data) and 0 <= sc < len(map_data[0]) and map_data[sr][sc] not in IMPASSABLE:
                            shoot_spots.append((sr, sc))
                actions = bfs_flanking(my_pos, shoot_spots)

    # 4. 출력 및 실행
    if not output:
        if actions:
            cmd = actions.pop(0)
            # 안전 이동 검사
            dr, dc = DIRS[MOVE_CMDS.index(cmd)]
            nr, nc = my_pos[0]+dr, my_pos[1]+dc
            if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]) and map_data[nr][nc] not in IMPASSABLE:
                output = cmd
            else:
                actions = []
                output = 'S'
        else:
            output = 'S'

    game_data = submit(output)
    if game_data: parse_data(game_data)

close()