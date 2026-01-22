# CLI(명령줄 인터페이스) 기초 — Git Bash (Windows)

## CLI란?

- CLI(Command Line Interface)는 텍스트 명령어로 컴퓨터와 상호작용하는 인터페이스입니다.
- GUI(그래픽 인터페이스)와 달리 키보드로 명령을 직접 입력해 파일 관리, 프로그램 실행, 버전관리 등 작업을 빠르게 수행할 수 있습니다.

## Git Bash란?

- Git Bash는 Windows에서 유닉스(리눅스/맥) 스타일의 쉘을 제공하는 도구입니다. Git 설치 시 함께 제공되며, `bash` 환경을 통해 많은 표준 명령어를 사용할 수 있습니다.
- Windows 경로는 `/c/Users/YourName`처럼 나타납니다. 또한 `~`는 사용자의 홈 디렉터리를 가리킵니다.

## Git Bash 열기

- 시작 메뉴에서 "Git Bash" 검색 후 실행
- 파일 탐색기에서 빈 공간을 우클릭 → "Git Bash Here"로 해당 폴더에서 바로 열기

## 기본 명령어 모음

아래 명령어들은 Git Bash에서 자주 쓰이는 기본 명령들입니다. 예시는 간단하게 표시합니다.

### 파일/디렉터리 탐색

```
pwd              # 현재 경로 출력
ls               # 디렉터리 목록
ls -la           # 숨김 파일 포함, 자세히
cd path/to/dir   # 디렉터리 이동
cd ..            # 부모 디렉터리로 이동
```

### 파일/디렉터리 조작

```
mkdir mydir           # 디렉터리 생성
touch file.txt        # 빈 파일 생성
cp src.txt dest.txt   # 파일 복사
mv oldname newname    # 파일 이동 또는 이름 변경
rm file.txt           # 파일 삭제
rm -r mydir           # 디렉터리와 내용 삭제
```

### 파일 내용 확인 / 출력

```
cat file.txt          # 파일 내용 출력
less file.txt         # 페이지 단위로 보기 (q로 종료)
head -n 10 file.txt   # 앞 10줄
tail -n 10 file.txt   # 뒤 10줄
```

### 검색 · 파이프 · 리다이렉션

```
grep "검색어" file.txt        # 파일에서 문자열 검색
command1 | command2            # 파이프: command1 출력 -> command2 입력
echo "hello" > out.txt        # 출력 리다이렉션(덮어쓰기)
echo "new" >> out.txt         # 이어쓰기
```

### 권한/실행 관련

```
chmod +x script.sh    # 실행 권한 부여
./script.sh           # 스크립트 실행
```

### 시스템 정보 / 기타 유용한 명령

```
whoami                # 현재 사용자
date                  # 현재 날짜/시간
clear                 # 화면 지우기
history               # 이전 명령 기록
```

### Git 관련 기본 명령 (Git Bash에서 자주 사용)

```
git status            # 현재 저장소 상태 확인
git add file.txt      # 변경 파일 스테이징
git commit -m "msg"  # 커밋
git push              # 원격으로 푸시
git pull              # 원격에서 변경 가져오기
```

## Windows 사용 시 주의사항

- 관리자 권한이 필요한 작업(특정 포트 사용, 시스템 폴더 접근 등)은 Git Bash에서도 제한될 수 있습니다. 필요하면 PowerShell(관리자)로 작업하세요.
- 경로 표기: Windows의 `C:\\Users\\Name`는 Git Bash에서 `/c/Users/Name`처럼 보입니다.
- 일부 Windows 전용 명령(예: `dir`, `del`)도 동작하지만, 가능한 한 표준 유닉스 명령을 사용하는 것이 호환성에 좋습니다.

## 연습 예제

1. 새 폴더 만들고 파일 생성하기

```
mkdir practice
cd practice
touch hello.txt
echo "Hello, CLI" > hello.txt
cat hello.txt
```

2. 간단한 검색 파이프 연습

```
ls -la | grep ".txt"
```

---

필요하면 더 많은 명령어(네트워크, 프로세스 관리, 편집기 사용법 등)를 추가해 드릴게요.

작성자: 프로그래밍 강사
