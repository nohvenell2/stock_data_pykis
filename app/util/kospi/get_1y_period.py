from datetime import datetime, timedelta
from typing import List,TypedDict
class Period_1y(TypedDict):
    start_date : str
    end_date : str


def generate_1y_periods(n:int) -> List[Period_1y]:
    """period 기간 1년 단위 List[시작일, 종료일]

    Args:
        n: 기간

    Returns:
        list: `[{start_date : 시작일, end_date : 종료일}, ... ]`
    """
    # 오늘 날짜
    end_date = datetime.now()
    # 결과 리스트 초기화
    periods = []
    
    for _ in range(n):
        # 시작 날짜는 1년 전 날짜로 설정
        start_date = end_date - timedelta(days=365)
        # 시작과 끝 날짜를 yyyymmdd 형식의 문자열로 변환하여 리스트에 추가
        periods.append({'start_date' : start_date.strftime('%Y%m%d'), 'end_date': end_date.strftime('%Y%m%d')})
        # 다음 기간을 위해 종료 날짜를 시작 날짜의 하루 전으로 갱신
        end_date = start_date - timedelta(days=1)
    
    return periods

if __name__ == '__main__' : # 예시로 5년 동안의 기간을 출력
    print(generate_1y_periods(20))