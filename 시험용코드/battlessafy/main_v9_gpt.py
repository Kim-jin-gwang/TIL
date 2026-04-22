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

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
MOVE_CMDS      = {0: "R A", 1: "D A", 2: "L A", 3: "U A"}
FIRE_CMDS      = {0: "R F", 1: "D F", 2: "L F", 3: "U F"}
MEGA_FIRE_CMDS = {0: "R F M", 1: "D F M", 2: "L F M", 3: "U F M"}

# 이동 불가 셀
IMPASSABLE = {'R', 'W', 'T', 'E1', 'E2', 'E3', 'X', 'H', 'M1', 'M2', 'M3', 'F'}

# 숲(부시) 타일: 은폐 효과 - 우회 경로 탐색 시 선호
BUSH_TILES = {'S'}  # 모래 등 은폐 가능 지형 (맵에 따라 추가)

##############################
# 기본 유틸 함수
##############################

def get_ammo():
    normal, mega = 0, 0
    if 'M' in my_allies:
        v = my_allies['M']
        try:
            normal = int(v[2])
            mega   = int(v[3])
        except:
            pass
    return normal, mega

def get_my_hp():
    if 'M' in my_allies:
        try:
            return int(my_allies['M'][0])
        except:
            pass
    return 100

def find_all_positions(grid, symbol):
    positions = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == symbol:
                positions.append((r, c))
    return positions

def find_position(grid, symbol):
    pos = find_all_positions(grid, symbol)
    return pos[0] if pos else None

def get_enemy_targets():
    """
    우선순위: 체력 낮은 적 탱크(마무리) > 포탑(X)
    기동 타격대는 체력 낮은 적을 먼저 마무리하는 역할
    """
    targets = []

    # 적 탱크 (체력 낮은 순 우선 - 마무리 역할)
    for key in ['E1', 'E2', 'E3']:
        pos = find_position(map_data, key)
        if pos:
            hp = int(enemies.get(key, [9999])[0]) if key in enemies else 9999
            targets.append((hp, pos, key))

    # 포탑은 탱크 마무리 후
    turret = find_position(map_data, 'X')
    if turret:
        hp = int(enemies.get('X', [9999])[0]) if 'X' in enemies else 9999
        targets.append((hp + 5000, turret, 'X'))  # 탱크보다 낮은 우선순위

    targets.sort(key=lambda x: x[0])  # 체력 낮은 순
    return [(t[1], t[2]) for t in targets]

##############################
# 기동 타격대 핵심 함수
##############################

def get_all_enemy_positions():
    """맵에서 모든 적 위치 반환"""
    enemy_pos = set()
    for key in ['E1', 'E2', 'E3', 'X']:
        pos = find_position(map_data, key)
        if pos:
            enemy_pos.add(pos)
    return enemy_pos

def get_turret_danger_zone():
    rows, cols = len(map_data), len(map_data[0])
    danger = set()

    turret_pos = find_position(map_data, 'X')
    if not turret_pos:
        return danger

    tr, tc = turret_pos

    for dr, dc in DIRS:
        fr, fc = tr, tc
        for _ in range(3):  # 사거리 3칸
            fr += dr
            fc += dc

            if not (0 <= fr < rows and 0 <= fc < cols):
                break

            if map_data[fr][fc] == 'R':  # 바위만 막힘
                break

            danger.add((fr, fc))

    return danger

def get_enemy_danger_zone(enemy_positions, danger_range=3):
    """
    적의 사거리 3칸 내 위험 구역 반환.
    우회 경로 탐색 시 이 구역을 피함.
    """
    rows, cols = len(map_data), len(map_data[0])
    danger = set()
    for (er, ec) in enemy_positions:
        for dr, dc in DIRS:
            fr, fc = er, ec
            for _ in range(danger_range):
                fr += dr
                fc += dc
                if not (0 <= fr < rows and 0 <= fc < cols):
                    break
                if map_data[fr][fc] == 'R':
                    break
                danger.add((fr, fc))
    return danger

def is_ally_at_supply(supply_pos):
    """
    보급 시설 인접 칸에 아군 탱크(M1~M3)가 이미 있는지 확인.
    있으면 해당 보급 시설은 사용하지 않음.
    """
    fr, fc = supply_pos
    for dr, dc in DIRS:
        ar, ac = fr + dr, fc + dc
        if 0 <= ar < len(map_data) and 0 <= ac < len(map_data[0]):
            if map_data[ar][ac] in {'M1', 'M2', 'M3'}:
                return True
    return False

import heapq

def bfs_flanking(start, target_pos, avoid_danger=True):
    if start is None or target_pos is None:
        return []

    rows, cols = len(map_data), len(map_data[0])
    enemy_positions = get_all_enemy_positions()
    danger_zone = get_enemy_danger_zone(enemy_positions) if avoid_danger else set()

    pq = [(0, start, [])]  # (cost, position, path)
    visited = {}

    while pq:
        cost, (r, c), path = heapq.heappop(pq)

        if (r, c) == target_pos:
            return path

        if (r, c) in visited and visited[(r, c)] <= cost:
            continue
        visited[(r, c)] = cost

        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            cell = map_data[nr][nc]


            turret_danger = get_turret_danger_zone()

            if cell in IMPASSABLE:
                continue

            if (nr, nc) in turret_danger:
                continue

            new_cost = cost + get_tile_cost(cell)

            # 위험지역 패널티
            if (nr, nc) in danger_zone:
                new_cost += 10

            heapq.heappush(pq, (new_cost, (nr, nc), path + [MOVE_CMDS[d]]))

    return []

def is_safe_position(pos):
    enemy_positions = get_all_enemy_positions()
    danger_zone = get_enemy_danger_zone(enemy_positions)

    return pos not in danger_zone

def bfs_to_shooting_spot_flanking(start, target_pos):
    """
    사격 가능 위치까지 우회 경로로 이동.
    위험 구역을 피해 측면에서 접근.
    """
    if start is None or target_pos is None:
        return []

    tr, tc = target_pos
    rows, cols = len(map_data), len(map_data[0])
    enemy_positions = get_all_enemy_positions()
    danger_zone = get_enemy_danger_zone(enemy_positions)

    # 타겟 사거리 3칸 내 사격 가능 위치
    shooting_spots = set()
    for d, (dr, dc) in enumerate(DIRS):
        fr, fc = tr, tc
        for step in range(1, 4):
            fr += dr
            fc += dc
            if not (0 <= fr < rows and 0 <= fc < cols):
                break
            cell = map_data[fr][fc]
            if cell == 'R':
                break
            if cell not in IMPASSABLE:
                shooting_spots.add((fr, fc))

    if not shooting_spots:
        return []

    # 안전한 사격 위치 우선
    safe_spots = shooting_spots - danger_zone
    preferred = safe_spots if safe_spots else shooting_spots

    queue = deque([(start, [], False)])
    visited = {start: False}
    best_unsafe = None

    while queue:
        (r, c), path, in_danger = queue.popleft()

        if (r, c) in preferred and not in_danger:
            return path
        if (r, c) in shooting_spots and best_unsafe is None:
            best_unsafe = path

        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            cell = map_data[nr][nc]
            if cell in IMPASSABLE:
                continue

            new_danger = in_danger or ((nr, nc) in danger_zone)
            prev = visited.get((nr, nc), None)
            if prev is None or (prev and not new_danger):
                visited[(nr, nc)] = new_danger
                queue.append(((nr, nc), path + [MOVE_CMDS[d]], new_danger))

    return best_unsafe if best_unsafe else []

def can_shoot_target(my_pos, target_pos, normal, mega):
    """사격 가능 여부 확인 + 페널티 방지"""
    r, c = my_pos
    rows, cols = len(map_data), len(map_data[0])

    for d, (dr, dc) in enumerate(DIRS):
        fr, fc = r, c
        for step in range(1, 4):
            fr += dr
            fc += dc
            if not (0 <= fr < rows and 0 <= fc < cols):
                break
            cell = map_data[fr][fc]
            if cell == 'R':
                break
            if (fr, fc) == target_pos:
                if mega > 0:
                    return MEGA_FIRE_CMDS[d]
                elif normal > 0:
                    return FIRE_CMDS[d]
                else:
                    return None
    return None

def get_tile_cost(cell):
    if cell == 'S':  # 모래
        return 5
    return 1

def get_safe_escape_move(my_pos):
    r, c = my_pos
    enemy_positions = get_all_enemy_positions()
    danger_zone = get_enemy_danger_zone(enemy_positions)

    for d, (dr, dc) in enumerate(DIRS):
        nr, nc = r + dr, c + dc

        if not (0 <= nr < len(map_data) and 0 <= nc < len(map_data[0])):
            continue
        if map_data[nr][nc] in IMPASSABLE:
            continue

        # 안전한 칸이면 이동
        if (nr, nc) not in danger_zone:
            return MOVE_CMDS[d]

    return None  # 전부 위험하면 None

def safe_move(my_pos, action_cmd):
    r, c = my_pos
    rows, cols = len(map_data), len(map_data[0])

    turret_danger = get_turret_danger_zone()

    dir_map = {
        'R A': (0, 1), 'D A': (1, 0),
        'L A': (0, -1), 'U A': (-1, 0)
    }

    if action_cmd not in dir_map:
        return action_cmd

    dr, dc = dir_map[action_cmd]
    nr, nc = r + dr, c + dc

    if not (0 <= nr < rows and 0 <= nc < cols):
        return 'S'
    if map_data[nr][nc] in IMPASSABLE:
        return 'S'

    # ⭐ 포탑 사거리 금지
    if (nr, nc) in turret_danger:
        return 'S'

    return action_cmd

def validate_command(cmd, my_pos, normal, mega):
    if cmd is None:
        return 'S'

    # 발사 관련
    if 'F' in cmd:
        if 'M' in cmd and mega <= 0:
            return 'S'
        if 'M' not in cmd and normal <= 0:
            return 'S'

    # 이동 관련
    if cmd in {'R A', 'L A', 'U A', 'D A'}:
        dir_map = {
            'R A': (0, 1), 'D A': (1, 0),
            'L A': (0, -1), 'U A': (-1, 0)
        }
        dr, dc = dir_map[cmd]
        nr, nc = my_pos[0] + dr, my_pos[1] + dc

        if not (0 <= nr < len(map_data) and 0 <= nc < len(map_data[0])):
            return 'S'
        if map_data[nr][nc] in IMPASSABLE:
            return 'S'

    return cmd

##############################
# 보급 관련 함수
##############################

def is_supply_reserved(supply_pos, my_pos):
    my_dist = abs(my_pos[0] - supply_pos[0]) + abs(my_pos[1] - supply_pos[1])

    for ally_key in ['M1', 'M2', 'M3']:
        ally_pos = find_position(map_data, ally_key)
        if ally_pos:
            ally_dist = abs(ally_pos[0] - supply_pos[0]) + abs(ally_pos[1] - supply_pos[1])

            if ally_dist <= my_dist + 1:
                return True

    return False

def caesar_decode(code):
    """카이사르 암호 해독 (shift +9 고정)"""
    code = code.strip()
    decoded = ''
    for ch in code:
        if ch.isalpha():
            decoded += chr((ord(ch.upper()) - ord('A') + 9) % 26 + ord('A'))
        else:
            decoded += ch
    return decoded

def try_decode_and_submit(code):
    """메가 포탄 10개 미만일 때만 해독 시도 (페널티 방지)"""
    _, mega = get_ammo()
    if mega >= 10:
        return None
    decoded = caesar_decode(code)
    return f'G {decoded}'

def find_supply_facility():
    """보급 시설(F) 위치 목록 반환"""
    return find_all_positions(map_data, 'F')

def is_adjacent_to_supply(my_pos):
    """현재 위치가 보급 시설에 인접해 있는지 확인"""
    r, c = my_pos
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]):
            if map_data[nr][nc] == 'F':
                return True
    return False

def move_to_supply(my_pos):
    """
    보급 시설 인접 칸으로 이동하는 최단 경로 반환.
    아군이 이미 사용 중인 보급 시설은 제외.
    """
    supply_positions = find_supply_facility()
    shortest = None

    for fp in supply_positions:
        # ★ 아군이 이미 해당 보급 시설 사용 중이면 스킵
        if is_ally_at_supply(fp):
            print(f'[SUPPLY] 아군 사용 중인 보급 시설 제외: {fp}')
            continue

        if is_supply_reserved(fp, my_pos):
            print(f'[SUPPLY] 예약된 보급소 제외: {fp}')
            continue

        fr, fc = fp
        for dr, dc in DIRS:
            ar, ac = fr + dr, fc + dc
            if 0 <= ar < len(map_data) and 0 <= ac < len(map_data[0]):
                if map_data[ar][ac] not in IMPASSABLE:
                    # 보급 시설 이동도 우회 경로 사용
                    path = bfs_flanking(my_pos, (ar, ac), avoid_danger=True)
                    if path is not None and (shortest is None or len(path) < len(shortest)):
                        shortest = path

    return shortest if shortest else []

##############################
# 닉네임 설정 및 최초 연결
##############################
NICKNAME = '대전6_김진광'
game_data = init(NICKNAME)

##############################
# 상태 변수
##############################
actions     = []
MEGA_TARGET = 2   # 전투 시작 전 목표 메가 포탄 개수
needs_supply = True

START_SYMBOL  = 'M'
TARGET_SYMBOL = 'X'
WALL_SYMBOL   = 'R'

# 최초 데이터 파싱
parse_data(game_data)

##############################
# 메인 반복문
##############################
while game_data is not None:

    print_data()

    normal_bomb, mega_bomb = get_ammo()
    my_hp  = get_my_hp()
    my_pos = find_position(map_data, START_SYMBOL)

    if my_pos is None:
        output = 'S'
        game_data = submit(output)
        if game_data:
            parse_data(game_data)
        continue

    output = None

    # [핵심 로직] 보급 상태 업데이트
    if needs_supply:
        # 목표치만큼 다 모았으면 전투 모드로 전환
        if mega_bomb >= MEGA_TARGET:
            needs_supply = False
            actions = [] 
            print(f'[STATE] 보급 완료({mega_bomb}발)! 사냥을 시작합니다.')
    else:
        # 포탄을 모두 다 썼을 때만 보급 모드로 전환
        if mega_bomb == 0 and normal_bomb == 0:
            needs_supply = True
            actions = []
            print('[STATE] 포탄 소진! 보급하러 복귀합니다.')

    # [공통] 사거리 안에 적이 들어오면 모드 상관없이 즉시 사격
    targets = get_enemy_targets()
    for t_pos, t_key in targets:
        shot_cmd = can_shoot_target(my_pos, t_pos, normal_bomb, mega_bomb)
        if shot_cmd:
            output = shot_cmd
            actions = []  
            print(f'[INTERCEPT] 적 발견 사격: {output}')
            break

    # [보급 모드 실행]
    if output is None and needs_supply:
        if codes and is_adjacent_to_supply(my_pos):
            cmd = try_decode_and_submit(codes[0].strip())
            if cmd:
                output = cmd
                print(f'[SUPPLY] 암호 해독 중... (현재 {mega_bomb}발)')

        if output is None:
            if not actions:
                actions = move_to_supply(my_pos)
            print(f'[SUPPLY] 보급지로 이동 중...')

    # [전투 모드 실행]
    elif output is None and not needs_supply:
        if not actions:
            if targets:
                best_target_pos, best_target_key = targets[0]
                actions = bfs_to_shooting_spot_flanking(my_pos, best_target_pos)
                print(f'[FLANKER] 적 추적 중: {best_target_key}')

    # ============================================================
    # 실제 커맨드 결정
    # ============================================================
    if output is None:
        if actions:
            raw = actions.pop(0)
            output = safe_move(my_pos, raw)
            output = validate_command(output, my_pos, normal_bomb, mega_bomb)

            # ❗ 이동이 막혀서 S 되면 → 도망 시도
            if output == 'S':
                escape = get_safe_escape_move(my_pos)
                if escape:
                    output = escape

        else:
            # ❗ S 대신 무조건 안전 이동 시도
            escape = get_safe_escape_move(my_pos)
            if escape:
                output = escape
            else:
                output = 'S'  # 진짜 갈 데 없을 때만

    print(f'[ACTION] {output}')
    game_data = submit(output)

    if game_data:
        parse_data(game_data)

        # 메가 포탄 증가 확인 → 경로 재계획
        new_normal, new_mega = get_ammo()
        if new_mega > mega_bomb:
            print(f'[INFO] 메가 포탄 획득! {mega_bomb}개 → {new_mega}개')
            actions = []

close()
