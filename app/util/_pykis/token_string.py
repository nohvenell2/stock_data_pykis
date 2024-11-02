from .Load_Pykis import KIS
from pykis.kis import KisAccessToken
k = KIS # 키스 토큰 로드
token = KisAccessToken.load('token.json').token