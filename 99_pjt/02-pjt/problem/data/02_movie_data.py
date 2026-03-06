import csv
import json
import os
import django

# Django 설정 로드 (make_password 사용을 위해)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.contrib.auth.hashers import make_password

DEFAULT_PASSWORD = '1q2w3e4r!'

# Input file paths
MOVIES_CSV       = 'movies.csv'
DETAILS_CSV      = 'movie_details.csv'
CAST_CSV         = 'movie_cast.csv'
REVIEWS_CSV      = 'movie_reviews.csv'

# Output file paths
OUT_MOVIES   = 'movies_data.csv'
OUT_GENRES   = 'genres_data.csv'
OUT_CASTS    = 'casts_data.csv'
OUT_REVIEWS  = 'reviews_data.csv'
OUT_USERS    = 'users_data.csv'
OUT_USERS_FX    = 'users_fixture.json'


def read_csv(file_path):
    """CSV 파일을 읽어 dict 리스트로 반환"""
    with open(file_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(file_path, fieldnames, rows):
    """dict 리스트를 CSV 파일로 저장"""
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [저장] {file_path}  ({len(rows)}건)")


def write_json(file_path, data):
    """Django fixture JSON 파일로 저장"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  [저장] {file_path}  ({len(data)}건)")


def build_movies(movies_rows, details_rows):
    """
    movies.csv + movie_details.csv 를 movie_id 기준으로 병합.
    Movie 모델 필드: id, title, release_date, popularity,
                     budget, revenue, runtime
    """
    details_map = {row['movie_id']: row for row in details_rows}

    result = []
    for m in movies_rows:
        d = details_map.get(m['id'], {})
        result.append({
            'id':           m['id'],
            'title':        m['title'],
            'release_date': m['release_date'],
            'popularity':   m['popularity'],
            'budget':       d.get('budget', 0),
            'revenue':      d.get('revenue', 0),
            'runtime':      d.get('runtime', 0),
        })
    return result


def build_genres(details_rows):
    """
    movie_details.csv 의 genres 컬럼을 분리하여 고유 장르 목록 생성.
    Genre 모델 필드: id, name
    중간 테이블(movie-genre 관계)은 genre_movies_data.csv 로 별도 저장.
    """
    genre_set = {}  # name -> id
    genre_movie_links = []  # (genre_id, movie_id)
    genre_id = 1

    for row in details_rows:
        movie_id = row['movie_id']
        genres_str = row.get('genres', '').strip()
        if not genres_str:
            continue
        for g in genres_str.split(','):
            name = g.strip()
            if not name:
                continue
            if name not in genre_set:
                genre_set[name] = genre_id
                genre_id += 1
            genre_movie_links.append({
                'genre_id': genre_set[name],
                'movie_id': movie_id,
            })

    genres = [{'id': gid, 'name': name} for name, gid in sorted(genre_set.items(), key=lambda x: x[1])]
    return genres, genre_movie_links


def build_casts(cast_rows):
    """
    movie_cast.csv 를 Cast 모델 형식으로 변환.
    Cast 모델 필드: id, movie_id, name, character, order
    """
    result = []
    for row in cast_rows:
        result.append({
            'id':        row['cast_id'],
            'movie_id':  row['movie_id'],
            'name':      row['name'],
            'character': row['character'],
            'order':     row['order'],
        })
    return result


def build_users(review_rows):
    """
    movie_reviews.csv 에서 고유 작성자를 추출하여 User 목록 생성.
    User 모델 필드: id, username
    """
    seen = {}
    user_id = 1
    for row in review_rows:
        username = row['author']
        if username not in seen:
            seen[username] = user_id
            user_id += 1
    users = [{'id': uid, 'username': name} for name, uid in seen.items()]
    return users, seen  # seen: {username -> id}


def build_reviews(review_rows, username_to_id):
    """
    movie_reviews.csv 를 Review 모델 형식으로 변환.
    Review 모델 필드: id, movie_id, author_id, content, rating
    author 문자열 -> User FK(author_id) 로 변환
    """
    result = []
    for i, row in enumerate(review_rows, start=1):
        result.append({
            'id':        i,
            'movie_id':  row['movie_id'],
            'author_id': username_to_id[row['author']],
            'content':   row['content'],
            'rating':    row['rating'],
        })
    return result


def build_users_fixture(users):
    """
    users 목록을 Django fixture 형식(accounts.user)으로 변환.
    password는 DEFAULT_PASSWORD를 해싱하여 저장.
    """
    hashed_pw = make_password(DEFAULT_PASSWORD)
    fixture = []
    for u in users:
        fixture.append({
            "model": "accounts.user",
            "pk": u['id'],
            "fields": {
                "username": u['username'],
                "password": hashed_pw,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "groups": [],
                "user_permissions": [],
            }
        })
    return fixture


def main():
    # 스크립트 위치를 기준으로 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base_dir, 'new_data')
    os.makedirs(out_dir, exist_ok=True)

    def path(name):
        return os.path.join(base_dir, name)

    def out_path(name):
        return os.path.join(out_dir, name)

    print("=== CSV 데이터 파싱 시작 ===")

    # 1. 원본 CSV 읽기
    movies_rows  = read_csv(path(MOVIES_CSV))
    details_rows = read_csv(path(DETAILS_CSV))
    cast_rows    = read_csv(path(CAST_CSV))
    review_rows  = read_csv(path(REVIEWS_CSV))

    # 2. 데이터 가공
    movies          = build_movies(movies_rows, details_rows)
    genres, g_links = build_genres(details_rows)
    casts           = build_casts(cast_rows)
    users, u_map    = build_users(review_rows)
    reviews         = build_reviews(review_rows, u_map)

    users_fixture   = build_users_fixture(users)

    # 3. 출력 CSV 저장
    write_csv(out_path(OUT_MOVIES),
              ['id', 'title', 'release_date', 'popularity', 'budget', 'revenue', 'runtime'],
              movies)

    write_csv(out_path(OUT_GENRES),
              ['id', 'name'],
              genres)

    write_csv(out_path('genre_movies_data.csv'),
              ['genre_id', 'movie_id'],
              g_links)

    write_csv(out_path(OUT_CASTS),
              ['id', 'movie_id', 'name', 'character', 'order'],
              casts)

    write_csv(out_path(OUT_USERS),
              ['id', 'username'],
              users)

    write_csv(out_path(OUT_REVIEWS),
              ['id', 'movie_id', 'author_id', 'content', 'rating'],
              reviews)

    # 4. users fixture JSON 저장 (loaddata 용)
    write_json(out_path(OUT_USERS_FX), users_fixture)

    print("=== 파싱 완료 ===")


if __name__ == '__main__':
    main()
