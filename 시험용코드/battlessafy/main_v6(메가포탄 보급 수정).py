import sys
import socket
import heapq
from collections import deque

##############################
# 메인 프로그램 통신 변수 및 함수
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
        return None

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
# 데이터 분석 및 전역 변수
##############################
map_data = []
my_allies = {}
enemies = {}
codes = []

def parse_data(game_data):
    if not game_data: return
    lines = game_data.split('\n')
    header = lines[0].split()
    if not header: return
    h, w, n_a, n_e, n_c = map(int, header[:5])
    
    global map_data
    map_data = [lines[1+i].split() for i in range(h)]
    
    idx = 1 + h
    my_allies.clear()
    for _ in range(n_a):
        row = lines[idx].split()
        my_allies[row[0]] = row[1:] # row[0]은 ID
        idx += 1
    
    enemies.clear()
    for _ in range(n_e):
        row = lines[idx].split()
        enemies[row[0]] = row[1:]
        idx += 1
        
    codes.clear()
    for _ in range(n_c):
        codes.append(lines[idx])
        idx += 1

##############################
# 기동 타격대 전략 및 유틸리티
##############################
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)] # 우, 하, 좌, 상
MOVE_CMDS = ["R A", "D A", "L A", "U A"]
FIRE_CMDS = ["R F", "D F", "L F", "U F"]
MEGA_FIRE_CMDS = ["R F M", "D F M", "L F M", "U F M"]

# 이동 불가 (모래 'S', 숲 'H'는 통과 가능하므로 제외)
IMPASSABLE = {'R', 'W', 'T', 'X', 'E1', 'E2', 'E3', 'M1', 'M2', 'M3', 'F'}

def get_ammo():
    """아군 탱크의 일반/메가 포탄 개수 반환 (인덱스 수정)"""
    if 'M' in my_allies:
        v = my_allies['M']
        # 매뉴얼 상: R[0], C[1], DIR[2], NORMAL[3], MEGA[4], HP[5]
        return int(v[3]), int(v[4])
    return 0, 0

def find_pos(symbol):
    for r in range(len(map_data)):
        for c in range(len(map_data[0])):
            if map_data[r][c] == symbol: return (r, c)
    return None

def get_tile_cost(r, c):
    """지형 가중치: 모래(S)는 회피, 숲(H)은 선호"""
    tile = map_data[r][c]
    if tile == 'S': return 20  # 모래는 매우 기피
    if tile == 'H': return 1   # 숲은 일반길과 동일하게 선호
    return 2 # 일반 평지는 숲보다 약간 높은 비용 (숲 우선 유도)

def bfs_weighted(start, targets):
    """다익스트라 기반 경로 탐색"""
    if not start or not targets: return []
    rows, cols = len(map_data), len(map_data[0])
    pq = [(0, start, [])]
    visited = {start: 0}

    while pq:
        cost, (r, c), path = heapq.heappop(pq)
        if (r, c) in targets: return path
        
        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and map_data[nr][nc] not in IMPASSABLE:
                new_cost = cost + get_tile_cost(nr, nc)
                if (nr, nc) not in visited or new_cost < visited[(nr, nc)]:
                    visited[(nr, nc)] = new_cost
                    heapq.heappush(pq, (new_cost, (nr, nc), path + [MOVE_CMDS[d]]))
    return []

def can_shoot_target(my_pos, target_pos, n_bomb, m_bomb):
    """사거리와 아군 보호를 고려한 사격 명령 생성"""
    r, c = my_pos
    for d, (dr, dc) in enumerate(DIRS):
        for step in range(1, 4): # 최대 3칸
            fr, fc = r + dr*step, c + dc*step
            if not (0 <= fr < len(map_data) and 0 <= fc < len(map_data[0])): break
            cell = map_data[fr][fc]
            if cell == 'R': break
            if cell in {'M1', 'M2', 'M3'}: break # 아군 오사 방지
            
            if (fr, fc) == target_pos:
                if step == 3: # 3칸은 메가 포탄만 가능
                    if m_bomb > 0: return MEGA_FIRE_CMDS[d]
                else: # 1~2칸
                    if m_bomb > 0: return MEGA_FIRE_CMDS[d] # 메가 우선
                    if n_bomb > 0: return FIRE_CMDS[d]
    return None

def get_targets():
    """체력(HP)이 낮은 적을 우선 타겟팅 (인덱스 수정)"""
    res = []
    for key in ['E1', 'E2', 'E3', 'X']:
        pos = find_pos(key)
        if pos:
            # HP는 리스트의 5번 인덱스
            hp = int(enemies[key][5]) if key in enemies else 999
            res.append((hp, pos, key))
    res.sort()
    return res

def caesar_decode(text):
    """보급소 암호 해독 (카이사르 +9)"""
    res = ""
    for c in text:
        if 'A' <= c.upper() <= 'Z':
            base = ord('A') if c.isupper() else ord('a')
            res += chr((ord(c) - base + 9) % 26 + base)
        else: res += c
    return res

##############################
# 메인 루프 시작
##############################
NICKNAME = '대전6_기동타격대'
game_data = init(NICKNAME)
parse_data(game_data)

actions = []
needs_supply = True # 초기 보급 모드 시작
MEGA_LIMIT = 2      # 메가 포탄 2개 보급 시 전투 돌입

while game_data:
    n_bomb, m_bomb = get_ammo()
    my_pos = find_pos('M')
    
    if not my_pos:
        game_data = submit('S'); parse_data(game_data); continue

    # [상태 머신] 보급 2개 완료 시 전투 / 모든 포탄 소진 시 보급
    if needs_supply and m_bomb >= MEGA_LIMIT:
        needs_supply = False
        actions = []
    elif not needs_supply and m_bomb == 0 and n_bomb == 0:
        needs_supply = True
        actions = []

    output = None
    targets = get_targets()

    # 1. 즉시 사격 (어느 모드에서나 사거리 내 적이 있으면 발사)
    for _, t_pos, _ in targets:
        cmd = can_shoot_target(my_pos, t_pos, n_bomb, m_bomb)
        if cmd:
            output = cmd; actions = []; break

    if not output:
        # 2. 보급 모드
        if needs_supply:
            f_pos = find_pos('F')
            if f_pos:
                dist = abs(my_pos[0]-f_pos[0]) + abs(my_pos[1]-f_pos[1])
                if dist == 1 and codes:
                    output = f'G {caesar_decode(codes[0].strip())}'
                elif not actions:
                    adj_spots = []
                    for dr, dc in DIRS:
                        nr, nc = f_pos[0]+dr, f_pos[1]+dc
                        if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]) and map_data[nr][nc] not in IMPASSABLE:
                            adj_spots.append((nr, nc))
                    actions = bfs_weighted(my_pos, adj_spots)
        
        # 3. 전투 모드 (기동 타격대 우회 기동)
        else:
            if not actions and targets:
                _, t_pos, _ = targets[0]
                fire_spots = []
                for d, (dr, dc) in enumerate(DIRS):
                    for s in range(1, 4): # 사거리 확보 가능한 평지/숲/모래 지점
                        sr, sc = t_pos[0]+dr*s, t_pos[1]+dc*s
                        if 0 <= sr < len(map_data) and 0 <= sc < len(map_data[0]):
                            if map_data[sr][sc] not in IMPASSABLE:
                                fire_spots.append((sr, sc))
                actions = bfs_weighted(my_pos, fire_spots)

    # 4. 최종 명령 결정 및 실시간 충돌 체크
    if not output:
        if actions:
            tmp_cmd = actions.pop(0)
            # 이동하려는 칸이 현재 비어있는지 마지막으로 확인
            if tmp_cmd in MOVE_CMDS:
                move_idx = MOVE_CMDS.index(tmp_cmd)
                nr, nc = my_pos[0]+DIRS[move_idx][0], my_pos[1]+DIRS[move_idx][1]
                if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]) and map_data[nr][nc] not in IMPASSABLE:
                    output = tmp_cmd
                else: # 아군이 길을 막았거나 맵 밖인 경우
                    actions = []; output = 'S'
            else: output = tmp_cmd
        else: output = 'S'

    game_data = submit(output)
    if game_data: parse_data(game_data)

close()