import csv
import os

# Input file paths
MOVIES_CSV       = 'movies.csv'
DETAILS_CSV      = 'movie_details.csv'
CAST_CSV         = 'movie_cast.csv'
REVIEWS_CSV      = 'movie_reviews.csv'

# Output file paths
OUT_MOVIES  = 'movies_data.csv'
OUT_GENRES  = 'genres_data.csv'
OUT_CASTS   = 'casts_data.csv'
OUT_REVIEWS = 'reviews_data.csv'


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


def build_reviews(review_rows):
    """
    movie_reviews.csv 를 Review 모델 형식으로 변환.
    Review 모델 필드: id, movie_id, author, content, rating
    """
    result = []
    for i, row in enumerate(review_rows, start=1):
        result.append({
            'id':       i,
            'movie_id': row['movie_id'],
            'author':   row['author'],
            'content':  row['content'],
            'rating':   row['rating'],
        })
    return result


def main():
    # 스크립트 위치를 기준으로 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))

    def path(name):
        return os.path.join(base_dir, name)

    print("=== CSV 데이터 파싱 시작 ===")

    # 1. 원본 CSV 읽기
    movies_rows  = read_csv(path(MOVIES_CSV))
    details_rows = read_csv(path(DETAILS_CSV))
    cast_rows    = read_csv(path(CAST_CSV))
    review_rows  = read_csv(path(REVIEWS_CSV))

    # 2. 데이터 가공
    movies         = build_movies(movies_rows, details_rows)
    genres, g_links = build_genres(details_rows)
    casts          = build_casts(cast_rows)
    reviews        = build_reviews(review_rows)

    # 3. 출력 CSV 저장
    write_csv(path(OUT_MOVIES),
              ['id', 'title', 'release_date', 'popularity', 'budget', 'revenue', 'runtime'],
              movies)

    write_csv(path(OUT_GENRES),
              ['id', 'name'],
              genres)

    write_csv(path('genre_movies_data.csv'),
              ['genre_id', 'movie_id'],
              g_links)

    write_csv(path(OUT_CASTS),
              ['id', 'movie_id', 'name', 'character', 'order'],
              casts)

    write_csv(path(OUT_REVIEWS),
              ['id', 'movie_id', 'author', 'content', 'rating'],
              reviews)

    print("=== 파싱 완료 ===")


if __name__ == '__main__':
    main()
