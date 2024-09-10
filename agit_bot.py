import requests
import time
from datetime import datetime

# 파일에서 글이 올라간 횟수를 읽어오는 함수
def read_count():
    try:
        with open("count.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0  # 파일이 없으면 0회차로 시작

# 글이 올라간 횟수를 파일에 저장하는 함수
def save_count(count):
    with open("count.txt", "w") as f:
        f.write(str(count))

# 글을 아지트에 올리는 함수
def post_to_agit():
    url = "https://agit.in/webhook/94bcee46-e319-4163-b941-294c091e62c1"
    headers = {
        "Content-Type": "application/json"
    }

    # 오늘 날짜와 요일 확인
    today = datetime.now()
    current_day = today.weekday()  # 0 = 월요일, 6 = 일요일

    # 평일이 아닌 경우 종료
    if current_day >= 5:
        print("오늘은 주말입니다. 글을 올리지 않습니다.")
        return

    # 글이 올라갈 기간 설정 (샘플 기간: 2024년 9월 11일 ~ 2024년 9월 20일)
    start_date = datetime(2024, 9, 11)
    end_date = datetime(2024, 9, 20)

    if not (start_date <= today <= end_date):
        print("현재는 글을 올리는 기간이 아닙니다.")
        return

    # 글이 올라간 횟수를 읽어오고, 1 증가시킴
    count = read_count() + 1
    title = f"{count}회차 독서 시간"

    # 현재 시간을 Unix 타임스탬프로 변환
    now = int(time.time())  # 초 단위의 Unix 타임스탬프
    one_day_later = now + 86400  # 하루 후(24시간)

    payload = {
        "text": "오늘의 독서 일정을 입력하세요!",
        "schedule": {
            "title": title,           # 글이 올라간 횟수를 제목에 추가
            "is_allday": True,
            "color": "blue",
            "starts_at": now,
            "ends_at": one_day_later
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"성공적으로 {title} 글을 올렸습니다!")
        # 글이 성공적으로 올라갔다면 횟수 저장
        save_count(count)
    else:
        print(f"글 올리기 실패: {response.status_code}, {response.text}")

# 테스트로 바로 실행
post_to_agit()
