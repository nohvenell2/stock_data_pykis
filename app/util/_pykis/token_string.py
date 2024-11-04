import os
import json
from .Load_Pykis import KIS
k = KIS # 토큰 기한 만료시 발급
def get_tokenString():
    folder_path = '/home/ubuntu/.pykis/cache/'
    file_list = os.listdir(folder_path)
    if not file_list: return None
    file_name = file_list[0]
    file_path = os.path.join(folder_path,file_name)
    if file_name in file_list:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # JSON 파일을 파이썬 딕셔너리로 변환
            return data['access_token']
    else:
        print(f"{file_name} 파일이 폴더에 없습니다.")
token = get_tokenString()