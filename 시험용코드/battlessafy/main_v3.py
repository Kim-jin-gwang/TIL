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
    map_height = int(header[0]) if len(header) >= 1 else 0
    map_width = int(header[1]) if len(header) >= 2 else 0
    num_of_allies = int(header[2]) if len(header) >= 3 else 0
    num_of_enemies = int(header[3]) if len(header) >= 4 else 0
    num_of_codes = int(header[4]) if len(header) >= 5 else 0
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
# 전략 함수
##############################

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
MOVE_CMDS  = {0: "R A", 1: "D A", 2: "L A", 3: "U A"}
FIRE_CMDS      = {0: "R F", 1: "D F", 2: "L F", 3: "U F"}
MEGA_FIRE_CMDS = {0: "R F M", 1: "D F M", 2: "L F M", 3: "U F M"}

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
    """현재 내 체력 반환"""
    if 'M' in my_allies:
        try:
            return int(my_allies['M'][0])
        except:
            pass
    return 100

def find_all_positions(grid, symbol):
    """심볼에 해당하는 모든 위치 반환"""
    positions = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == symbol:
                positions.append((r, c))
    return positions

def find_position(grid, symbol):
    """심볼의 첫 번째 위치 반환"""
    pos = find_all_positions(grid, symbol)
    return pos[0] if pos else None

def get_enemy_targets():
    """
    우선순위: 포탑(X) > 체력 낮은 적 탱크(E1~E3)
    맵에서 실제로 존재하는 대상만 반환
    """
    targets = []

    # 포탑 우선
    turret = find_position(map_data, 'X')
    if turret:
        hp = int(enemies.get('X', [9999])[0]) if 'X' in enemies else 9999
        targets.append((hp, turret, 'X'))

    # 적 탱크 (체력 낮은 순)
    for key in ['E1', 'E2', 'E3']:
        pos = find_position(map_data, key)
        if pos:
            hp = int(enemies.get(key, [9999])[0]) if key in enemies else 9999
            targets.append((hp, pos, key))

    targets.sort(key=lambda x: (x[2] != 'X', x[0]))  # 포탑 우선, 그다음 체력 낮은 순
    return [(t[1], t[2]) for t in targets]

def can_shoot_target(my_pos, target_pos, normal, mega):
    """
    사격 가능 여부 확인 + 페널티 방지
    - 허공 발사 방지: 경로에 타겟이 실제로 있는지 확인
    - 포탄 수량 확인
    """
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
            if cell == 'R':  # 바위 → 포탄 차단
                break
            if (fr, fc) == target_pos:
                # 메가 포탄 우선 (보유 시), 단 10개 미만일 때만
                if mega > 0:
                    return MEGA_FIRE_CMDS[d]
                elif normal > 0:
                    return FIRE_CMDS[d]
                else:
                    return None  # 포탄 없음 → 발사 안 함
            # 중간에 아무것도 없으면 계속 진행 (허공 발사 아님)
    return None  # 사거리 내 타겟 없음 → 발사 안 함 (허공 발사 방지)

def safe_move(my_pos, action_cmd):
    """
    이동 커맨드 실행 전 막다른 길 체크
    이동 불가하면 'S' (대기) 반환
    """
    r, c = my_pos
    rows, cols = len(map_data), len(map_data[0])

    IMPASSABLE = {'R', 'W', 'T', 'E1', 'E2', 'E3', 'X', 'H', 'M1', 'M2', 'M3', 'F'}

    dir_map = {
        'R A': (0, 1), 'D A': (1, 0),
        'L A': (0, -1), 'U A': (-1, 0)
    }
    if action_cmd not in dir_map:
        return action_cmd  # 이동 커맨드가 아니면 그대로

    dr, dc = dir_map[action_cmd]
    nr, nc = r + dr, c + dc

    if not (0 <= nr < rows and 0 <= nc < cols):
        return 'S'  # 맵 밖 → 대기
    if map_data[nr][nc] in IMPASSABLE:
        return 'S'  # 막힘 → 대기 (페널티 방지)

    return action_cmd

def bfs_to_target(start, target_pos, passable_extra=None):
    """
    BFS로 이동 경로 탐색.
    - 통과 불가: R(바위), W(물), 적 탱크 위치, 아군 탱크 위치
    - S(모래)는 통과 가능하나 체력 감소 고려
    - T(나무)는 이동 불가지만 인접 시 포탄으로 제거
    passable_extra: 추가로 통과 가능한 심볼 집합
    """
    if start is None or target_pos is None:
        return []

    rows, cols = len(map_data), len(map_data[0])
    IMPASSABLE = {'R', 'W', 'T', 'E1', 'E2', 'E3', 'X', 'H', 'M1', 'M2', 'M3', 'F'}
    if passable_extra:
        IMPASSABLE -= passable_extra

    queue = deque([(start, [])])
    visited = {start}

    while queue:
        (r, c), actions = queue.popleft()

        if (r, c) == target_pos:
            return actions

        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if (nr, nc) in visited:
                continue
            cell = map_data[nr][nc]
            if cell in IMPASSABLE:
                continue
            visited.add((nr, nc))
            queue.append(((nr, nc), actions + [MOVE_CMDS[d]]))

    return []

def bfs_adjacent_to_target(start, target_pos):
    """
    타겟에 인접한 칸까지 이동하는 BFS.
    사거리 내에 들어오기 위해 타겟 주변 3칸 이내 접근 경로 탐색.
    """
    if start is None or target_pos is None:
        return []

    tr, tc = target_pos
    rows, cols = len(map_data), len(map_data[0])

    # 타겟 사거리 3 이내의 칸들 (같은 행/열, 장애물 없는 칸)
    shooting_spots = []
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
            if cell not in {'W', 'T', 'E1', 'E2', 'E3', 'X', 'H', 'M1', 'M2', 'M3', 'F'}:
                shooting_spots.append((fr, fc))

    if not shooting_spots:
        return []

    # start에서 shooting_spots 중 하나까지 최단 BFS
    IMPASSABLE = {'R', 'W', 'T', 'E1', 'E2', 'E3', 'X', 'H', 'M1', 'M2', 'M3', 'F'}
    queue = deque([(start, [])])
    visited = {start}
    best = []

    while queue:
        (r, c), actions = queue.popleft()

        if (r, c) in shooting_spots:
            return actions  # 첫 번째 도달이 최단

        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if (nr, nc) in visited:
                continue
            cell = map_data[nr][nc]
            if cell in IMPASSABLE:
                continue
            visited.add((nr, nc))
            queue.append(((nr, nc), actions + [MOVE_CMDS[d]]))

    return []

def find_supply_facility():
    """보급 시설(F) 인접 위치 탐색"""
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

def caesar_decode(code):
    """카이사르 암호 해독 (shift 9 고정)"""
    code = code.strip()
    decoded = ''
    for ch in code:
        if ch.isalpha():
            decoded += chr((ord(ch.upper()) - ord('A') + 9) % 26 + ord('A'))
        else:
            decoded += ch
    return decoded

def try_decode_and_submit(code):
    """
    메가 포탄 10개 미만일 때만 해독 시도 (페널티 방지)
    """
    _, mega = get_ammo()
    if mega >= 10:
        return None  # 10개 이상이면 G 커맨드 사용 금지
    decoded = caesar_decode(code)
    return f'G {decoded}'

##############################
# 닉네임 설정 및 최초 연결
##############################
NICKNAME = '대전6_김진광'
game_data = init(NICKNAME)

##############################
# 상태 변수
##############################
actions = []          # 현재 이동/공격 액션 큐
decode_candidates = []  # 암호 해독 후보 큐
last_code = None      # 마지막으로 본 암호문
decode_success = False  # 이번 보급에서 해독 성공 여부
tried_shifts = set()  # 이번 보급에서 시도한 shift

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
    my_hp = get_my_hp()
    my_pos = find_position(map_data, START_SYMBOL)

    if my_pos is None:
        output = 'S'
        game_data = submit(output)
        if game_data:
            parse_data(game_data)
        continue

    output = None

    # ============================================================
    # 우선순위 1: 암호 해독 (보급 시설 인접 + 암호문 존재)
    # 메가 포탄이 0개일 때 또는 게임 초반에 보급 시설 방문
    # ============================================================
    if codes and is_adjacent_to_supply(my_pos):
        current_code = codes[0].strip()
        if not decode_success:
            output = try_decode_and_submit(current_code)

    # ============================================================
    # 우선순위 2: 현재 위치에서 타겟 사격 가능하면 즉시 발사
    # ============================================================
    if output is None:
        targets = get_enemy_targets()
        for t_pos, t_key in targets:
            shot_cmd = can_shoot_target(my_pos, t_pos, FIRE_CMDS, MEGA_FIRE_CMDS, normal_bomb, mega_bomb)
            if shot_cmd:
                output = shot_cmd
                actions = []  # 이동 계획 초기화 (사격 후 재계획)
                break

    # ============================================================
    # 우선순위 3: 메가 포탄 없고 보급 시설 근처에 있으면 보급 먼저
    # ============================================================
    if output is None and mega_bomb == 0 and not decode_success:
        supply_positions = find_supply_facility()
        if supply_positions:
            # 보급 시설에 인접한 칸으로 이동
            adj_supply = None
            shortest = None
            for fp in supply_positions:
                fr, fc = fp
                for dr, dc in DIRS:
                    ar, ac = fr + dr, fc + dc
                    if 0 <= ar < len(map_data) and 0 <= ac < len(map_data[0]):
                        if map_data[ar][ac] not in {'R', 'W', 'T', 'E1', 'E2', 'E3', 'X'}:
                            path = bfs_to_target(my_pos, (ar, ac))
                            if path is not None and (shortest is None or len(path) < len(shortest)):
                                shortest = path
                                adj_supply = (ar, ac)
            if shortest is not None and len(shortest) > 0:
                if not actions:
                    actions = shortest
                # actions 첫 번째 이동 실행은 아래에서

    # ============================================================
    # 우선순위 4: 사격 위치로 이동 (BFS)
    # ============================================================
    if output is None:
        # 매 턴 타겟 재설정 (맵이 바뀌므로)
        targets = get_enemy_targets()
        if targets:
            best_target_pos, best_target_key = targets[0]

            # 액션 큐가 비었거나 목표 도달 불가 시 재탐색
            if not actions:
                # 사격 가능 위치로 이동
                actions = bfs_adjacent_to_target(my_pos, best_target_pos)
                if not actions:
                    # 사격 위치 없으면 최대한 가까이
                    actions = bfs_to_target(my_pos, best_target_pos)

    # ============================================================
    # 실제 커맨드 결정
    # ============================================================
    if output is None:
        if actions:
            raw = actions.pop(0)
            output = safe_move(my_pos, raw)
        else:
            # 갈 곳 없으면 대기 (S)
            output = 'S'

    print(f'[ACTION] {output}')
    game_data = submit(output)

    if game_data:
        parse_data(game_data)

        # 메가 포탄이 생겼으면 해독 성공으로 간주
        new_normal, new_mega = get_ammo()
        if new_mega > mega_bomb:
            decode_success = True
            print('[INFO] 암호 해독 성공! 메가 포탄 획득')
            actions = []  # 경로 재계획

close()
