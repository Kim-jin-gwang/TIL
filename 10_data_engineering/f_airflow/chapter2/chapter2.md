## 10. EmailOperator 사용을 위한 SMTP 설정

> 설정 -> 모든 설정

> 계정 클릭 -> Google 계정관리 -> 보안 -> 2단계 인증 -> 앱 비밀번호 (검색창에 쳐서 생성)

Airflow에서 `EmailOperator`를 통해 Gmail SMTP로 메일을 보내기 위해서는 다음과 같은 환경변수를 설정해야 합니다.

| 환경 변수 키 | 설명 |
|---------------|------|
| `AIRFLOW__SMTP__SMTP_HOST` | 사용할 SMTP 서버의 호스트 주소입니다. Gmail을 사용할 경우 `smtp.gmail.com`을 입력합니다. |
| `AIRFLOW__SMTP__SMTP_USER` | 이메일을 보낼 Gmail 계정입니다. |
| `AIRFLOW__SMTP__SMTP_PASSWORD` | Gmail 계정의 **앱 비밀번호**입니다. 일반 비밀번호가 아닌, [2단계 인증](https://myaccount.google.com/security) 설정 후 발급된 16자리 앱 비밀번호를 사용해야 합니다. |
| `AIRFLOW__SMTP__SMTP_PORT` | SMTP 포트 번호입니다. TLS의 경우 보통 `587`번 포트를 사용합니다. |
| `AIRFLOW__SMTP__SMTP_MAIL_FROM` | 이메일 발송 시 표시될 '보낸 사람' 주소입니다. 보통 `SMTP_USER`와 동일하게 설정합니다. |

```yaml
    # docker-compose.yaml 파일의 AIRFLOW_CONFIG: '/opt/airflow/config/airflow.cfg' 아래에
    AIRFLOW__SMTP__SMTP_HOST: 'smtp.gmail.com'
    AIRFLOW__SMTP__SMTP_USER: '{내 Gmail 주소}' 
    AIRFLOW__SMTP__SMTP_PASSWORD: '{발급받은 앱 비밀번호}'
    AIRFLOW__SMTP__SMTP_PORT: 587
    AIRFLOW__SMTP__SMTP_MAIL_FROM: '{내 Gmail 주소}' 
```

## 11. shell script

- Airflow에서 Shell Script를 실행하려면 먼저 **실행 권한 (+x)** 부여 필요.
- 이는 어떤 스크립트 형태를 실행시키던 쓰던 마찬가지
```bash
cd /home/ssafy/ssafy_airflow
chmod +x ./plugins/shell/select_fruit.sh
```

-  줄바꿈 형태 Linux 포맷으로 변환
```bash
sudo apt install dos2unix
sudo dos2unix plugins/shell/select_fruit.sh
```
