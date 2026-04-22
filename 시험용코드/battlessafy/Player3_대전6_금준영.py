import sys
import socket
import heapq
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

# 메인 프로그램 연결 및 초기화
def init(nickname):
    try:
        print(f'[STATUS] Trying to connect to {HOST}:{PORT}...')
        sock.connect((HOST, PORT))
        print('[STATUS] Connected')
        init_command = f'INIT {nickname}'

        return submit(init_command)

    except Exception as e:
        print('[ERROR] Failed to connect. Please check if the main program is waiting for connection.')
        print(e)

# 메인 프로그램으로 데이터(명령어) 전송
def submit(string_to_send):
    try:
        send_data = ARGS + string_to_send + ' '
        sock.send(send_data.encode('utf-8'))

        return receive()
        
    except Exception as e:
        print('[ERROR] Failed to send data. Please check if connection to the main program is valid.')

    return None

# 메인 프로그램으로부터 데이터 수신
def receive():
    try:
        game_data = (sock.recv(1024)).decode()

        if game_data and game_data[0].isdigit() and int(game_data[0]) > 0:
            return game_data

        print('[STATUS] No receive data from the main program.')    
        close()

    except Exception as e:
        print('[ERROR] Failed to receive data. Please check if connection to the main program is valid.')

# 연결 해제
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
map_data = [[]]  # 맵 정보. 예) map_data[0][1] - [0, 1]의 지형/지물
my_allies = {}  # 아군 정보. 예) my_allies['M'] - 플레이어 본인의 정보
enemies = {}  # 적군 정보. 예) enemies['X'] - 적 포탑의 정보
codes = []  # 주어진 암호문. 예) codes[0] - 첫 번째 암호문

##############################
# 입력 데이터 파싱
##############################

# 입력 데이터를 파싱하여 각각의 리스트/딕셔너리에 저장
def parse_data(game_data):
    # 입력 데이터를 행으로 나누기
    game_data_rows = game_data.split('\n')
    row_index = 0

    # 첫 번째 행 데이터 읽기
    header = game_data_rows[row_index].split(' ')
    map_height = int(header[0]) if len(header) >= 1 else 0 # 맵의 세로 크기
    map_width = int(header[1]) if len(header) >= 2 else 0  # 맵의 가로 크기
    num_of_allies = int(header[2]) if len(header) >= 3 else 0  # 아군의 수
    num_of_enemies = int(header[3]) if len(header) >= 4 else 0  # 적군의 수
    num_of_codes = int(header[4]) if len(header) >= 5 else 0  # 암호문의 수
    row_index += 1

    # 기존의 맵 정보를 초기화하고 다시 읽어오기
    map_data.clear()
    map_data.extend([[ '' for c in range(map_width)] for r in range(map_height)])
    for i in range(0, map_height):
        col = game_data_rows[row_index + i].split(' ')
        for j in range(0, len(col)):
            map_data[i][j] = col[j]
    row_index += map_height

    # 기존의 아군 정보를 초기화하고 다시 읽어오기
    my_allies.clear()
    for i in range(row_index, row_index + num_of_allies):
        ally = game_data_rows[i].split(' ')
        ally_name = ally.pop(0) if len(ally) >= 1 else '-'
        my_allies[ally_name] = ally
    row_index += num_of_allies

    # 기존의 적군 정보를 초기화하고 다시 읽어오기
    enemies.clear()
    for i in range(row_index, row_index + num_of_enemies):
        enemy = game_data_rows[i].split(' ')
        enemy_name = enemy.pop(0) if len(enemy) >= 1 else '-'
        enemies[enemy_name] = enemy
    row_index += num_of_enemies

    # 기존의 암호문 정보를 초기화하고 다시 읽어오기
    codes.clear()
    for i in range(row_index, row_index + num_of_codes):
        codes.append(game_data_rows[i])

# 파싱한 데이터를 화면에 출력
def print_data():
    print(f'\n----------입력 데이터----------\n{game_data}\n----------------------------')

    print(f'\n[맵 정보] ({len(map_data)} x {len(map_data[0])})')
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            print(f'{map_data[i][j]} ', end='')
        print()

    print(f'\n[아군 정보] (아군 수: {len(my_allies)})')
    for k, v in my_allies.items():
        if k == 'M':
            print(f'M (내 탱크) - 체력: {v[0]}, 방향: {v[1]}, 보유한 일반 포탄: {v[2]}개, 보유한 메가 포탄: {v[3]}개')
        elif k == 'H':
            print(f'H (아군 포탑) - 체력: {v[0]}')
        else:
            print(f'{k} (아군 탱크) - 체력: {v[0]}')

    print(f'\n[적군 정보] (적군 수: {len(enemies)})')
    for k, v in enemies.items():
        if k == 'X':
            print(f'X (적군 포탑) - 체력: {v[0]}')
        else:
            print(f'{k} (적군 탱크) - 체력: {v[0]}')

    print(f'\n[암호문 정보] (암호문 수: {len(codes)})')
    for i in range(len(codes)):
        print(codes[i])

##############################
# 닉네임 설정 및 최초 연결
##############################
NICKNAME = '대전_6반_금준영'
game_data = init(NICKNAME)

###################################
# 알고리즘 함수/메서드 부분 구현 시작
###################################
def get_positions(grid, symbols):
    positions = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if any(grid[r][c].startswith(s) for s in symbols):
                positions.append((r, c))
    return positions

def get_forbidden_zone(grid):
    """포탑(H, X) 주변 3x3 영역을 완벽한 이동 불가 구역으로 매핑"""
    forbidden = set()
    for pos in get_positions(grid, ['H', 'X']):
        pr, pc = pos
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = pr + dr, pc + dc
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                    forbidden.add((nr, nc))
    return forbidden

def check_los(grid, tank, target_symbols, max_range=3):
    """엄격한 사선 판별(Raycasting): 장애물(R, F, T) 조우 시 즉각 시야 차단 처리"""
    r0, c0 = tank
    for d, (dr, dc) in DIRS.items():
        for step in range(1, max_range + 1):
            r, c = r0 + dr * step, c0 + dc * step
            if not (0 <= r < len(grid) and 0 <= c < len(grid[0])): break
            
            cell = grid[r][c]
            
            # 사거리 내에 적(E, X)이 뚜렷이 포착되었을 때만 (방향, 타겟정보) 반환
            if any(cell.startswith(s) for s in target_symbols):
                return d, cell
                
            # 사선을 가로막는 모든 장애물 (아군, 벽, 시설, 나무) 조우 시 사격 불가
            if cell.startswith('M') or cell.startswith('H') or \
               cell in [WALL_SYMBOL, FACILITY_SYMBOL, TREE_SYMBOL]: 
                break
                
    return None, None

def get_firing_positions(grid, target_pos, forbidden_zone, max_range=3):
    """타겟을 직사로 쏠 수 있는 '안전한 빈 타일'들의 목록을 역산하여 반환"""
    valid_positions = []
    tr, tc = target_pos
    
    for dr, dc in DIRS.values():
        for step in range(1, max_range + 1):
            r, c = tr + dr * step, tc + dc * step
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                if (r, c) in forbidden_zone:
                    continue
                cell = grid[r][c]
                
                # 사격 위치는 평행이동이 가능한 땅(G)이거나 모래(S)만 허용 (나무 불허)
                if cell in ['G', SAND_SYMBOL]: 
                    valid_positions.append((r, c))
                
                # 타겟에서 뻗어나온 사선이 지형물에 가로막히면 그 뒤쪽은 사격 진지로 무효
                if cell in [WALL_SYMBOL, FACILITY_SYMBOL, TREE_SYMBOL] or \
                   cell.startswith('M') or cell.startswith('H'):
                    break
    return valid_positions

def find_best_step(grid, start, goals, current_hp, forbidden_zone):
    """Dijkstra 탐색: 나무(Tree)를 벽(Wall)과 동등한 이동 불가 장벽으로 격상"""
    if not goals or start in goals: return None
    
    pq = [(0, start[0], start[1], [])]
    min_cost = {(start[0], start[1]): 0}
    
    while pq:
        cost, r, c, path = heapq.heappop(pq)
        
        if (r, c) in goals:
            return path[0] if path else None
            
        if cost > min_cost.get((r, c), float('inf')): continue
            
        for d, (dr, dc) in DIRS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                cell = grid[nr][nc]
                
                # 금지 구역 및 장애물(나무, 벽, 물, 시설, 포탑 등) 완전 차단
                if (nr, nc) in forbidden_zone: continue
                if cell in [WALL_SYMBOL, WATER_SYMBOL, FACILITY_SYMBOL, TREE_SYMBOL] or \
                   cell.startswith('H') or cell.startswith('X') or cell.startswith('M') or cell.startswith('E'):
                    continue
                
                move_cost = 1
                if cell == SAND_SYMBOL:
                    if current_hp <= 30: continue # 모래는 HP 페널티가 있으므로 체력 부족 시 차단
                    move_cost = 5 # 모래는 가중치를 크게 주어 최대한 우회 유도
                
                next_cost = cost + move_cost
                if next_cost < min_cost.get((nr, nc), float('inf')):
                    min_cost[(nr, nc)] = next_cost
                    heapq.heappush(pq, (next_cost, nr, nc, path + [d]))
    return None

def decrypt(secret):
    if not secret: return ""
    BASE = ord('A')
    return ''.join(chr(BASE + (ord(c) - BASE + 9) % 26) for c in secret)

# 전역 상수
DIRS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
MOVE_CMDS = {'U': "U A", 'D': "D A", 'L': "L A", 'R': "R A"}
FIRE_CMDS = {'U': "U F", 'D': "D F", 'L': "L F", 'R': "R F"}
MEGA_FIRE_CMDS = {'U': "U F M", 'D': "D F M", 'L': "L F M", 'R': "R F M"}

TANK_SYMBOL, ENEMY_SYMBOL, TARGET_SYMBOL = 'M', 'E', 'X'
WALL_SYMBOL, WATER_SYMBOL, TREE_SYMBOL = 'R', 'W', 'T'
FACILITY_SYMBOL, SAND_SYMBOL = 'F', 'S'

parse_data(game_data)

###################################
# 알고리즘 메인 루프 (Action Pipeline)
###################################

while game_data is not None:
    print_data()
    tank_list = get_positions(map_data, ['M'])
    if not tank_list: 
        game_data = receive()
        continue
        
    tank = tank_list[0]
    hp = int(my_allies['M'][0])
    mega_count = int(my_allies['M'][3])
    
    # 공통 데이터 갱신
    forbidden_zone = get_forbidden_zone(map_data)
    action = None

    # [1] 보급시설 인접 시 암호 해독
    if mega_count < 2 and len(codes) > 0:
        facilities = get_positions(map_data, ['F'])
        is_adjacent = any(abs(tank[0]-fr) + abs(tank[1]-fc) == 1 for fr, fc in facilities)
        if is_adjacent:
            word = decrypt(codes[0])
            if word: action = f"G {word}"
    
    # [2] 엄격한 사격 교전 (Target in Sight)
    if not action:
        los_dir, target_cell = check_los(map_data, tank, ['E', 'X'])
        if los_dir:
            if mega_count > 0 and (target_cell.startswith('X') or mega_count >= 2):
                action = MEGA_FIRE_CMDS[los_dir]
            else:
                action = FIRE_CMDS[los_dir]

    # [3] 최적의 사격 진지로 기동 (Pathfinding)
    if not action:
        enemy_turrets = get_positions(map_data, ['X'])
        enemy_tanks = get_positions(map_data, ['E'])
        
        targets = enemy_turrets if enemy_turrets else enemy_tanks
        if targets:
            # 모든 타겟에 대해 타격 가능한 모든 안전 진지를 큐에 넣고 최단 거리 탐색
            all_firing_positions = []
            for t in targets:
                all_firing_positions.extend(get_firing_positions(map_data, t, forbidden_zone))
            
            move_dir = find_best_step(map_data, tank, all_firing_positions, hp, forbidden_zone)
            if move_dir:
                action = MOVE_CMDS[move_dir]

    # [4] 할 일이 없거나 경로가 막혔을 때는 순수하게 대기 (오발 및 충돌 원천 차단)
    if not action:
        action = "S"

    game_data = submit(action)
    if game_data: parse_data(game_data)
    
close()
