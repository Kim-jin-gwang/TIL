import sys
import socket
from collections import deque

##############################
# 메인 프로그램 통신 변수 정의
##############################
HOST = '127.0.0.1'
PORT = 8747
ARGS = sys.argv[1] if len(sys.argv) > 1 else ''
sock = socket.socket()

##############################
# 메인 프로그램 통신 함수 정의
##############################

def init(nickname):
    try:
        print(f'[STATUS] Trying to connect to {HOST}:{PORT}...')
        sock.connect((HOST, PORT))
        print('[STATUS] Connected')
        return submit(f'INIT {nickname}')
    except Exception as e:
        print('[ERROR] Failed to connect.')
        print(e)
    return None

def submit(string_to_send):
    try:
        send_data = ARGS + string_to_send + ' '
        sock.send(send_data.encode('utf-8'))
        return receive()
    except Exception as e:
        print('[ERROR] Failed to send data.')
    return None

def receive():
    try:
        game_data = (sock.recv(1024)).decode()
        if game_data and game_data[0].isdigit() and int(game_data[0]) > 0:
            return game_data
        print('[STATUS] No receive data from the main program.')
        close()
    except Exception as e:
        print('[ERROR] Failed to receive data.')
    return None

def close():
    try:
        if sock is not None:
            sock.close()
        print('[STATUS] Connection closed')
    except Exception as e:
        print('[ERROR] Network connection has been corrupted.')

##############################
# 데이터 변수 및 파싱 함수
##############################
map_data = [[]]
my_allies = {}
enemies = {}
codes = []

def parse_data(game_data):
    game_data_rows = game_data.split('\n')
    row_index = 0

    header = game_data_rows[row_index].split(' ')
    map_height  = int(header[0]) if len(header) >= 1 else 0
    map_width   = int(header[1]) if len(header) >= 2 else 0
    num_allies  = int(header[2]) if len(header) >= 3 else 0
    num_enemies = int(header[3]) if len(header) >= 4 else 0
    num_codes   = int(header[4]) if len(header) >= 5 else 0
    row_index += 1

    map_data.clear()
    map_data.extend([['' for _ in range(map_width)] for _ in range(map_height)])
    for i in range(map_height):
        col = game_data_rows[row_index + i].split(' ')
        for j in range(len(col)):
            map_data[i][j] = col[j]
    row_index += map_height

    my_allies.clear()
    for i in range(row_index, row_index + num_allies):
        ally = game_data_rows[i].split(' ')
        name = ally.pop(0)
        my_allies[name] = ally
    row_index += num_allies

    enemies.clear()
    for i in range(row_index, row_index + num_enemies):
        enemy = game_data_rows[i].split(' ')
        name = enemy.pop(0)
        enemies[name] = enemy
    row_index += num_enemies

    codes.clear()
    for i in range(row_index, row_index + num_codes):
        codes.append(game_data_rows[i])

##############################
# 방향 및 심볼 정의
##############################
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # R, D, L, U
MOVE_CMDS      = {0: 'R A', 1: 'D A', 2: 'L A', 3: 'U A'}
FIRE_CMDS      = {0: 'R F', 1: 'D F', 2: 'L F', 3: 'U F'}
FIRE_MEGA_CMDS = {0: 'R F M', 1: 'D F M', 2: 'L F M', 3: 'U F M'}

BLOCK_SYMBOLS      = {'R', 'W', 'T'} # 이동 불가
SHOT_BLOCK_SYMBOLS = {'R'}           # 포탄 통과 불가
ENEMY_TANK_SYMBOLS = {'E1', 'E2', 'E3'}
ENEMY_BASE_SYMBOL  = 'X'
MY_TANK_SYMBOL     = 'M'
ALLY_TANK_SYMBOLS  = {'M1', 'M2', 'M3'}
ALLY_BASE_SYMBOL   = 'H'
SUPPLY_SYMBOL      = 'F'

FIRE_RANGE  = 3
NORMAL_DMG  = 30
MEGA_DMG    = 70
MAX_HP      = 100

###################################
# 알고리즘 및 보조 함수
###################################

def find_position(symbol):
    for r in range(len(map_data)):
        for c in range(len(map_data[0])):
            if map_data[r][c] == symbol: return (r, c)
    return None

def find_all_positions(symbols):
    positions = []
    for r in range(len(map_data)):
        for c in range(len(map_data[0])):
            if map_data[r][c] in symbols: positions.append((r, c))
    return positions

def is_passable(r, c):
    rows, cols = len(map_data), len(map_data[0])
    if not (0 <= r < rows and 0 <= c < cols): return False
    cell = map_data[r][c]
    # 벽, 보급소, 모든 탱크 및 기지는 통과 불가
    if cell in BLOCK_SYMBOLS or cell == SUPPLY_SYMBOL: return False
    if cell in ENEMY_TANK_SYMBOLS or cell == ENEMY_BASE_SYMBOL: return False
    if cell in ALLY_TANK_SYMBOLS or cell == ALLY_BASE_SYMBOL: return False
    return True

def bfs_to_adjacent(start, target):
    """목적지 상하좌우 인접 칸까지의 최단 경로 계산"""
    rows, cols = len(map_data), len(map_data[0])
    adjacent = []
    for dr, dc in DIRS:
        nr, nc = target[0] + dr, target[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols and is_passable(nr, nc):
            adjacent.append((nr, nc))
    
    if not adjacent: return []
    if start in adjacent: return []

    queue = deque([(start, [])])
    visited = {start}
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) in adjacent: return path
        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and is_passable(nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [MOVE_CMDS[d]]))
    return []

def can_fire_at(my_pos, target_pos):
    """사거리 내 직선상에 적이 있고 장애물(R)이 없는지 확인"""
    mr, mc = my_pos
    tr, tc = target_pos
    if mr != tr and mc != tc: return False, None
    
    d = (0 if tc > mc else 2) if mr == tr else (1 if tr > mr else 3)
    dist = abs(tr - mr) + abs(tc - mc)
    
    if dist > FIRE_RANGE: return False, None
    
    # 경로상 장애물 체크
    dr, dc = DIRS[d]
    for step in range(1, dist):
        if map_data[mr + dr * step][mc + dc * step] in SHOT_BLOCK_SYMBOLS:
            return False, None
    return True, d

def get_target_hp(target_pos):
    cell = map_data[target_pos[0]][target_pos[1]]
    if cell in ENEMY_TANK_SYMBOLS or cell == ENEMY_BASE_SYMBOL:
        return int(enemies.get(cell, [str(MAX_HP)])[0])
    return MAX_HP

def get_best_fire_cmd(fire_dir, target_pos, my_mega, my_missiles):
    target_hp = get_target_hp(target_pos)
    is_base = (map_data[target_pos[0]][target_pos[1]] == ENEMY_BASE_SYMBOL)
    
    if target_hp <= NORMAL_DMG and my_missiles > 0: return FIRE_CMDS[fire_dir]
    if my_mega > 0 and (is_base or my_mega >= 2 or my_missiles <= 0): return FIRE_MEGA_CMDS[fire_dir]
    return FIRE_CMDS[fire_dir] if my_missiles > 0 else (FIRE_MEGA_CMDS[fire_dir] if my_mega > 0 else None)

def caesar_decode(code):
    """카이사르 암호 해독 (shift +9 고정)"""
    code = code.strip()
    decoded = ''
    for ch in code:
        if ch.isalpha():
            decoded += chr((ord(ch.upper()) - ord('A') + 9) % 26 + ord('A'))
        else:
            decoded += ch
    return 'G ' + decoded

###################################
# 메인 루프 시작
###################################

NICKNAME = '대전6_이지석'
game_data = init(NICKNAME)
if game_data: parse_data(game_data)

actions = deque()

while game_data is not None:
    my_info = my_allies.get('M', [])
    if not my_info:
        game_data = submit('S')
        if game_data: parse_data(game_data)
        continue

    my_missiles = int(my_info[2]) if len(my_info) > 2 else 0
    my_mega = int(my_info[3]) if len(my_info) > 3 else 0
    my_pos = find_position(MY_TANK_SYMBOL)
    
    if not my_pos:
        game_data = submit('S')
        if game_data: parse_data(game_data)
        continue

    enemy_tanks = find_all_positions(ENEMY_TANK_SYMBOLS)
    enemy_base = find_position(ENEMY_BASE_SYMBOL)
    supply_pos = find_position(SUPPLY_SYMBOL)

    # 사격 대상 리스트 생성 (HP 낮은 탱크 우선 -> 그 다음 기지)
    enemy_tanks.sort(key=lambda p: get_target_hp(p))
    targets = enemy_tanks + ([enemy_base] if enemy_base else [])

    # ── 최우선 순위: 즉시 사격 (이동 중이라도 쏨) ──────────────────────
    fired = False
    for t_pos in targets:
        can_fire, f_dir = can_fire_at(my_pos, t_pos)
        if can_fire:
            cmd = get_best_fire_cmd(f_dir, t_pos, my_mega, my_missiles)
            if cmd:
                print(f'[ACTION] FIRE! Target={map_data[t_pos[0]][t_pos[1]]}')
                actions.clear() # 사격 후 상황 재판단을 위해 경로 초기화
                game_data = submit(cmd)
                if game_data: parse_data(game_data)
                fired = True
                break
    if fired: continue

    # ── 순위 1: 보급소 암호 해독 ──────────────────────────────────
    if codes and my_mega < 4:
        cmd = caesar_decode(codes[0])
        print(f'[ACTION] DECODE: {cmd}')
        game_data = submit(cmd)
        if game_data: parse_data(game_data)
        continue

    # ── 순위 2: 이동 로직 (보급소 또는 적 탐색) ────────────────────────
    if not actions:
        # 1) 메가탄 부족 시 보급소행
        if my_mega < 4 and supply_pos:
            path = bfs_to_adjacent(my_pos, supply_pos)
            if path: actions.extend(path)
        
        # 2) 보급 불필요하거나 보급소 없으면 가장 가까운 적 탱크 추격
        if not actions and enemy_tanks:
            path = bfs_to_adjacent(my_pos, enemy_tanks[0])
            if path: actions.extend(path)
            
        # 3) 적 탱크도 없으면 적 기지 파괴하러 이동
        if not actions and enemy_base:
            path = bfs_to_adjacent(my_pos, enemy_base)
            if path: actions.extend(path)

    if actions:
        game_data = submit(actions.popleft())
        if game_data: parse_data(game_data)
        continue

    # ── 순위 3: 행동 불가 시 대기 ──────────────────────────────────
    game_data = submit('S')
    if game_data: parse_data(game_data)

close()