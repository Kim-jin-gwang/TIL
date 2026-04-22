import sys, socket
from collections import deque

HOST, PORT = '127.0.0.1', 8747
ARGS = sys.argv[1] if len(sys.argv) > 1 else ''
sock = socket.socket()

def init(nickname):
    try: sock.connect((HOST, PORT)); return submit(f'INIT {nickname}')
    except: return None

def submit(s):
    try: sock.send((ARGS + s + ' ').encode('utf-8')); return receive()
    except: return None

def receive():
    try:
        data = sock.recv(2048).decode()  # 데이터 잘림 방지용 버퍼 확대
        return data if data and data[0].isdigit() else (close() or None)
    except: return None

def close(): 
    try: sock.close()
    except: pass

map_data, my_allies, enemies, codes = [], {}, {}, []
map_h, map_w = 0, 0
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # R, D, L, U
MOVE_CMDS = {0: 'R A', 1: 'D A', 2: 'L A', 3: 'U A'}
TURN_CMDS = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}
FIRE_CMDS = {0: 'R F', 1: 'D F', 2: 'L F', 3: 'U F'}
FIRE_MEGA_CMDS = {0: 'R F M', 1: 'D F M', 2: 'L F M', 3: 'U F M'}

def parse_data(gd):
    global map_h, map_w
    try:
        lines = gd.split('\n')
        h, w, na, ne, nc = map(int, lines[0].split()[:5])
        map_h, map_w = h, w
        map_data.clear()
        map_data.extend([lines[i + 1].split() for i in range(h)])
        my_allies.clear()
        enemies.clear()
        codes.clear()
        for i in range(h + 1, h + 1 + na):
            l = lines[i].split()
            my_allies[l[0]] = l[1:]
        for i in range(h + 1 + na, h + 1 + na + ne):
            l = lines[i].split()
            enemies[l[0]] = l[1:]
        for i in range(h + 1 + na + ne, h + 1 + na + ne + nc):
            codes.append(lines[i])
    except: pass

def find_pos(s):
    for r in range(map_h):
        for c in range(map_w):
            if map_data[r][c] == s: return (r, c)
    return None

def is_passable(r, c):
    if not (0 <= r < map_h and 0 <= c < map_w): return False
    cell = map_data[r][c]
    # 이동 불가능한 지형 및 유닛 (M은 나 자신이므로 통과 가능 판정 후 나중에 BFS에서 처리)
    if cell in {'R', 'W', 'T', 'F', 'X', 'H', 'E1', 'E2', 'E3'} or (cell in {'M1', 'M2', 'M3'}): return False
    return True

def bfs(start, target, exact=False):
    if not start or not target: return []
    q = deque([(start, [])])
    v = {start}
    # 시즈모드 이동 시(exact=True)에는 그 칸까지, 아니면 그 옆칸(adj)까지
    targets = [target] if exact else [(target[0] + dr, target[1] + dc) for dr, dc in DIRS]
    while q:
        (r, c), path = q.popleft()
        if (r, c) in targets: return path
        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if is_passable(nr, nc) and (nr, nc) not in v:
                v.add((nr, nc))
                q.append(((nr, nc), path + [MOVE_CMDS[d]]))
    return []

def can_fire(my_p, t_p):
    if not my_p or not t_p: return False, None
    mr, mc = my_p
    tr, tc = t_p
    if mr != tr and mc != tc: return False, None  # 직선 방향에서만 가능

    dist = abs(tr - mr) + abs(tc - mc)
    if dist > 3: return False, None  # 사거리 제한

    # 경로상 장애물 체크
    d = (0 if tc > mc else 2) if mr == tr else (1 if tr > mr else 3)  # 방향 계산
    for s in range(1, dist):  # 시작점부터 목표까지의 모든 칸을 검사
        nr, nc = mr + DIRS[d][0] * s, mc + DIRS[d][1] * s
        if not is_passable(nr, nc):  # 장애물 체크
            return False, None
    return True, d

def decode(c):
    res = ''
    for ch in c.strip():
        if ch.isalpha(): res += chr((ord(ch.upper()) - ord('A') + 9) % 26 + ord('A'))
        else: res += ch
    return 'G ' + res

NICKNAME = '대전6_이지석'
game_data = init(NICKNAME)
while game_data:
    parse_data(game_data)
    my_info = my_allies.get('M', [])
    my_pos = find_pos('M')
    if not my_info or not my_pos: game_data = submit('S'); continue
    my_mega = int(my_info[3])  # 메가 포탄 수
    supply = find_pos('F')
    if codes: game_data = submit(decode(codes[0])); continue

    # [1] 사격 우선
    fired = False
    if my_mega > 0:  # 메가 포탄이 있을 때만 사격
        for t_sym in ['E1', 'E2', 'E3', 'X']:
            t_pos = find_pos(t_sym)
            ok, d = can_fire(my_pos, t_pos)
            if ok:
                game_data = submit(FIRE_MEGA_CMDS[d] if my_mega > 0 else FIRE_CMDS[d])
                fired = True
                my_mega -= 1  # 메가 포탄 사용 후 감소
                break

    # 메가 포탄이 4개 이상이면 사격을 멈추고 상대 추적 시작
    if fired:
        if my_mega >= 4:  # 메가 포탄이 4개 이상이면 더 이상 쏘지 않음
            # 상대를 추적하러 가기
            for t_sym in ['E1', 'E2', 'E3']:
                t_pos = find_pos(t_sym)
                if t_pos:
                    path = bfs(my_pos, t_pos)
                    if path:
                        game_data = submit(path[0])
                        break
        else:
            # 적을 찾고 쏘지 않으면 계속 추적
            for t_sym in ['E1', 'E2', 'E3']:
                t_pos = find_pos(t_sym)
                if t_pos:
                    path = bfs(my_pos, t_pos)
                    if path:
                        game_data = submit(path[0])
                        break

    # [2] 가까운 보급소 (거리 4 이내)
    if supply and my_mega < 4:
        if (abs(my_pos[0] - supply[0]) + abs(my_pos[1] - supply[1])) <= 4:
            path = bfs(my_pos, supply)
            if path: game_data = submit(path[0]); continue

    # [3] 적 추격
    for t_sym in ['E1', 'E2', 'E3']:
        t_pos = find_pos(t_sym)
        if t_pos:
            path = bfs(my_pos, t_pos)
            if path: game_data = submit(path[0]); break
    else:
        game_data = submit('S')