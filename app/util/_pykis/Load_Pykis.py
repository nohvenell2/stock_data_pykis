from dotenv import load_dotenv
#from pykis.kis import PyKis, KisAccessToken
from pykis import PyKis
load_dotenv()
KIS = PyKis("secret.json")
KIS.token.save("token.json")
