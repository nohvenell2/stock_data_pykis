from dotenv import load_dotenv
from pykis.kis import PyKis, KisAccessToken
load_dotenv()
KIS = PyKis("secret.json")
KIS.token = KisAccessToken.load("token.json")