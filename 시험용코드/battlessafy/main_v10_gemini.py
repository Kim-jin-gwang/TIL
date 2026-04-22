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
        init_command = f'INIT {nickname}'
        return submit(init_command)
    except Exception as e:
        print('[ERROR] Failed to connect.')
        print(e)

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

def close():
    try:
        if sock is not None:
            sock.close()
        print('[STATUS] Connection closed')
    except Exception as e:
        print('[ERROR] Network connection has been corrupted.')

##############################
# 입력 데이터 변수 정의
##############################
map_data = [[]]
my_allies = {}
enemies = {}
codes = []

##############################
# 입력 데이터 파싱
##############################

def parse_data(game_data):
    game_data_rows = game_data.split('\n')
    row_index = 0

    header = game_data_rows[row_index].split(' ')
    map_height   = int(header[0]) if len(header) >= 1 else 0
    map_width    = int(header[1]) if len(header) >= 2 else 0
    num_of_allies   = int(header[2]) if len(header) >= 3 else 0
    num_of_enemies  = int(header[3]) if len(header) >= 4 else 0
    num_of_codes    = int(header[4]) if len(header) >= 5 else 0
    row_index += 1

    map_data.clear()
    map_data.extend([['' for c in range(map_width)] for r in range(map_height)])
    for i in range(0, map_height):
        col = game_data_rows[row_index + i].split(' ')
        for j in range(0, len(col)):
            map_data[i][j] = col[j]
    row_index += map_height

    my_allies.clear()
    for i in range(row_index, row_index + num_of_allies):
        ally = game_data_rows[i].split(' ')
        ally_name = ally.pop(0) if len(ally) >= 1 else '-'
        my_allies[ally_name] = ally
    row_index += num_of_allies

    enemies.clear()
    for i in range(row_index, row_index + num_of_enemies):
        enemy = game_data_rows[i].split(' ')
        enemy_name = enemy.pop(0) if len(enemy) >= 1 else '-'
        enemies[enemy_name] = enemy
    row_index += num_of_enemies

    codes.clear()
    for i in range(row_index, row_index + num_of_codes):
        codes.append(game_data_rows[i])

def print_data():
    print(f'\n[맵 정보] ({len(map_data)} x {len(map_data[0])})')
    for row in map_data:
        print(' '.join(row))

    print(f'\n[아군 정보]')
    for k, v in my_allies.items():
        if k == 'M':
            print(f'M (내 탱크) - 체력:{v[0]}, 방향:{v[1]}, 일반포탄:{v[2]}, 메가포탄:{v[3]}')
        else:
            print(f'{k} - 체력:{v[0]}')

    print(f'\n[적군 정보]')
    for k, v in enemies.items():
        print(f'{k} - 체력:{v[0]}')

    print(f'\n[암호문] {codes}')

##############################
# 전략 상수
##############################

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)] # R, D, L, U
MOVE_CMDS      = {0: "R A", 1: "D A", 2: "L A", 3: "U A"}
FIRE_CMDS      = {0: "R F", 1: "D F", 2: "L F", 3: "U F"}
MEGA_FIRE_CMDS = {0: "R F M", 1: "D F M", 2: "L F M", 3: "U F M"}

# 이동 가능한 타일 (확실하게 안전한 타일만 포함)
WALKABLE_TILES = {'0', 'S', 'H'} 

##############################
# 유틸리티 함수
##############################

def find_all_positions(grid, symbol):
    positions = []
    if not grid: return positions
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == symbol:
                positions.append((r, c))
    return positions

def find_position(symbol):
    pos_list = find_all_positions(map_data, symbol)
    return pos_list[0] if pos_list else None

def get_ammo():
    normal, mega = 0, 0
    if 'M' in my_allies:
        v = my_allies['M']
        try:
            normal = int(v[3]) if len(v) > 3 else 0
            mega   = int(v[4]) if len(v) > 4 else 0
        except: pass
    return normal, mega

def get_my_hp():
    if 'M' in my_allies:
        v = my_allies['M']
        try: return int(v[5]) if len(v) > 5 else 100
        except: pass
    return 100

def get_all_enemy_positions():
    enemy_pos = []
    for key in ['E1', 'E2', 'E3', 'X']:
        pos = find_position(key)
        if pos: enemy_pos.append(pos)
    return enemy_pos

##############################
# 긴급 회피 및 경로 탐색
##############################

import heapq

def get_predicted_danger_zone():
    danger = set()
    rows, cols = len(map_data), len(map_data[0])
    enemies_pos = get_all_enemy_positions()

    for (er, ec) in enemies_pos:
        # 적의 현재 위치 및 주변 1칸
        possible_spots = [(er, ec)]
        for dr, dc in DIRS:
            nr, nc = er + dr, ec + dc
            if 0 <= nr < rows and 0 <= nc < cols and map_data[nr][nc] in WALKABLE_TILES:
                possible_spots.append((nr, nc))
        # 사정거리 3칸
        for (sr, sc) in possible_spots:
            for dr, dc in DIRS:
                for step in range(1, 4):
                    fr, fc = sr + dr * step, sc + dc * step
                    if not (0 <= fr < rows and 0 <= fc < cols): break
                    if map_data[fr][fc] == 'R': break
                    danger.add((fr, fc))
    return danger

def get_emergency_escape(my_pos, danger_zone):
    """현재 위치가 위험하거나 막힐 것 같으면 옆 칸으로 한 칸 피함"""
    r, c = my_pos
    for d, (dr, dc) in enumerate(DIRS):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]):
            if map_data[nr][nc] in WALKABLE_TILES and (nr, nc) not in danger_zone:
                return MOVE_CMDS[d]
    return None

def dijkstra_path(start, targets, avoid_danger=True):
    if not start or not targets: return []
    rows, cols = len(map_data), len(map_data[0])
    danger_zone = get_predicted_danger_zone() if avoid_danger else set()
    
    pq = [(0, start, [])]
    visited = {start: 0}

    while pq:
        cost, (r, c), path = heapq.heappop(pq)
        if (r, c) in targets: return path
        
        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # 맵 데이터 실시간 확인 (아군 탱크 'M1', 'M2' 등은 WALKABLE이 아니므로 자동 회피)
                if map_data[nr][nc] in WALKABLE_TILES:
                    tile_cost = 1
                    if map_data[nr][nc] == 'S': tile_cost += 5
                    if (nr, nc) in danger_zone: tile_cost += 50
                    
                    new_cost = cost + tile_cost
                    if (nr, nc) not in visited or new_cost < visited[(nr, nc)]:
                        visited[(nr, nc)] = new_cost
                        heapq.heappush(pq, (new_cost, (nr, nc), path + [MOVE_CMDS[d]]))
    return []

def can_shoot_target(my_pos, target_pos, normal, mega):
    r, c = my_pos
    for d, (dr, dc) in enumerate(DIRS):
        for step in range(1, 4):
            fr, fc = r + dr * step, c + dc * step
            if not (0 <= fr < len(map_data) and 0 <= fc < len(map_data[0])): break
            if map_data[fr][fc] == 'R': break
            if map_data[fr][fc] in {'M1', 'M2', 'M3'}: break
            if (fr, fc) == target_pos:
                return MEGA_FIRE_CMDS[d] if mega > 0 else (FIRE_CMDS[d] if normal > 0 else None)
    return None

def caesar_decode(code):
    res = ""
    for ch in code.strip():
        if 'A' <= ch.upper() <= 'Z':
            res += chr((ord(ch.upper()) - ord('A') + 9) % 26 + ord('A'))
        else: res += ch
    return res

##############################
# 메인 제어 루프
##############################

NICKNAME = '대전6_기동타격대'
game_data = init(NICKNAME)

enemies = {}
my_allies = {}
if game_data: parse_data(game_data)

actions = []
needs_supply = True
MEGA_LIMIT = 1 # 보급 기준 하향하여 더 빨리 공격 전환

while game_data:
    my_hp = get_my_hp()
    normal_bomb, mega_bomb = get_ammo()
    my_pos = find_position('M')
    danger_zone = get_predicted_danger_zone()

    if not my_pos:
        game_data = submit('S'); parse_data(game_data); continue

    output = None

    # 1. 즉시 사격 (공격이 최선의 방어)
    enemy_list = get_all_enemy_positions()
    for ep in enemy_list:
        cmd = can_shoot_target(my_pos, ep, normal_bomb, mega_bomb)
        if cmd:
            output = cmd; actions = []; break

    # 2. 긴급 회피 (가만히 있어서 패널티 받는 것 방지)
    if not output and (my_pos in danger_zone or my_hp <= 30):
        escape_move = get_emergency_escape(my_pos, danger_zone)
        if escape_move:
            output = escape_move; actions = []

    # 3. 보급 및 이동 전략
    if not output:
        needs_supply = (mega_bomb < MEGA_LIMIT)
        if needs_supply:
            # 보급소 인접 시 획득
            for dr, dc in DIRS:
                nr, nc = my_pos[0]+dr, my_pos[1]+dc
                if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]) and map_data[nr][nc] == 'F':
                    if codes: output = f'G {caesar_decode(codes[0])}'; break
            
            if not output and not actions:
                f_targets = []
                for fp in find_all_positions(map_data, 'F'):
                    for dr, dc in DIRS:
                        nr, nc = fp[0]+dr, fp[1]+dc
                        if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]) and map_data[nr][nc] in WALKABLE_TILES:
                            f_targets.append((nr, nc))
                actions = dijkstra_path(my_pos, f_targets, avoid_danger=True)
        else:
            if not actions and enemy_list:
                actions = dijkstra_path(my_pos, enemy_list, avoid_danger=True)

    # 4. 최종 명령 검증 (패널티 킬러)
    if not output:
        if actions:
            cmd = actions[0]
            if " A" in cmd:
                move_map = {"R A": (0,1), "D A": (1,0), "L A": (0,-1), "U A": (-1,0)}
                dr, dc = move_map[cmd]
                nr, nc = my_pos[0] + dr, my_pos[1] + dc
                
                # 가려는 칸이 막혔거나 위험하면 대기하지 말고 즉시 경로 재계산/회피
                if not (0 <= nr < len(map_data) and 0 <= nc < len(map_data[0])) or map_data[nr][nc] not in WALKABLE_TILES:
                    actions = []
                    # 주변에 갈 수 있는 다른 칸이 있는지 한 번 더 찾음
                    output = get_emergency_escape(my_pos, danger_zone) or 'S'
                else:
                    output = actions.pop(0)
            else:
                output = actions.pop(0)
        else:
            # 할 일 없으면 안전한 곳으로 한 칸이라도 움직임
            output = get_emergency_escape(my_pos, danger_zone) or 'S'

    game_data = submit(output)
    if game_data: parse_data(game_data)

close()